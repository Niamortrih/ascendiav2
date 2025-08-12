from functions import *
from scipy.stats import skew, kurtosis



def make_dataspr(connection, node):
    data = []

    data.append(0)
    r = connection.command(line="show_effective_stack")
    startstack = float(r[0])
    r = connection.command(line="show_tree_params")
    startpot = float(r[1].split()[-1])
    bb = 20

    bets = node.split(":")
    bet = 0
    lastbet = 0
    lastbethero = 0
    if bets[-1][0] == "b":
        bet = float(bets[-1][1:])
    if bets[-2][0] == "b":
        lastbet = float(bets[-2][1:])
        bet -= lastbet
    if len(bets) > 2 and bets[-3][0] == "b":
        lastbethero = float(bets[-2][1:])
    if bets[-1][0] == "c":
        bet = 0
    effstack = startstack - lastbet
    pot = startpot + 2 * lastbet
    spr = effstack / pot
    data.append(spr)
    bpr = bet / pot
    bpr = bpr
    data.append(bpr)
    minbet = max(bet - lastbet, bb)
    minbet = minbet / pot
    data.append(minbet)

    end = 0
    data.append(end)
    return data



def make_result(connection, node, taboop, tabip, eqs, list_hands, scaler, model):
    inputs = []
    dataspr = make_dataspr(connection,node)
    inputs += dataspr

    if sum(taboop) < 0.1:
        taboop = np.full(1326, 1.0, dtype=float)

    eqhero = get_calc_eq(connection, "OOP")
    eqvln = get_calc_eq(connection, "IP")
    inter = get_intersection_matrix(list_hands)
    ponderhero, pondervln = get_ponder(eqs, eqhero, tabip, taboop, inter)
    sephero = split_range(taboop, ponderhero, 5)
    sepvln = split_range(tabip, pondervln, 5)
    for i in range(5):
        for j in range(5):
            res = range_vs(eqs, sephero[i], sepvln[j], inter)
            inputs.append(res)

    rivers = get_rivers(connection, 500, "OOP")
    riversvln = get_rivers(connection, 500, "IP")

    moy, std = get_std_rivers(rivers.T)
    inputs.append(moy)
    inputs.append(std)
    moy, std = get_std_rivers(riversvln.T)
    inputs.append(moy)
    inputs.append(std)

    sepvln = split_range(tabip, pondervln, 12)
    lines = []
    for num in range(1326):
        datahand = []

        for i in range(len(sepvln)):
            res = hand_vs_range(eqs, num, sepvln[i], inter)
            datahand.append(res)
            block = blocker(num,sepvln[i],inter)
            datahand.append(block)

        handrivers = rivers[:, num]
        datahand.append(np.nanmean(handrivers))
        datahand.append(np.nanstd(handrivers))
        for i in range(5, 100, 5):
            datahand.append(np.nanpercentile(handrivers, i))
        datahand.append(skew(handrivers, nan_policy='omit'))
        datahand.append(kurtosis(handrivers, nan_policy='omit'))


        lines.append(inputs+datahand)

    X = np.array(lines, dtype=float)
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)  # shape: (n_samples,)
    print(y_pred)
    # for i in range(1326):
    #     print(node, list_hands[i], y_pred[i])
    return y_pred