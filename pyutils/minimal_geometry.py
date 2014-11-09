import math

def deCasteljau(x, y, pts, e):
    n = len(x)
    xs = [x]
    ys = [y]

    for i in range(1, n):
        xs.append([])
        ys.append([])
        for j in range(n-i):
            xs[i].append((xs[i-1][j] + xs[i-1][j+1]) / 2)
            ys[i].append((ys[i-1][j] + ys[i-1][j+1]) / 2)

    bx = xs[n-1][0]
    by = ys[n-1][0]

    mx = (x[0] + x[n-1]) / 2
    my = (y[0] + y[n-1]) / 2

    diff = math.sqrt((bx - mx)**2 + (by - my)**2)

    if diff < e:
        pts.append([bx, by])
        pts.append([x[n-1], y[n-1]])
    else:
        n1x = [xs[i][0] for i in range(len(x))]
        n1y = [ys[i][0] for i in range(len(y))]

        deCasteljau(n1x, n1y, pts, e)

        n2x = [0] * len(x)
        for i in range(len(x)):
            n2x[n-i-1] = xs[i][len(xs[i]) - 1]


        n2y = [0] * len(y)
        for i in range(len(y)):
            n2y[n-i-1] = ys[i][len(ys[i]) - 1]

        deCasteljau(n1x, n1y, pts, e)
