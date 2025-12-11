def learn_theta(data, colors):
    max_blue = None
    min_red = None
    for x, c in zip(data, colors):
        if c == 'blue':
            if max_blue is None or x > max_blue:
                max_blue = x
        else:
            if min_red is None or x < min_red:
                min_red = x
    # theta anywhere between max_blue and min_red works
    return (max_blue + min_red) / 2


def compute_ell(data, colors, theta):
    loss = 0
    for x, c in zip(data, colors):
        if c == 'red' and x <= theta:
            loss += 1
        elif c == 'blue' and x > theta:
            loss += 1
    return loss


def minimize_ell(data, colors):
    paired = sorted(zip(data, colors), key=lambda p: p[0])
    values = [p[0] for p in paired]
    n = len(values)
    candidates = []
    candidates.append(values[0] - 1.0)
    for i in range(n - 1):
        candidates.append((values[i] + values[i + 1]) / 2)
    candidates.append(values[-1] + 1.0)

    best_theta = candidates[0]
    best_loss = compute_ell(data, colors, best_theta)
    for theta in candidates[1:]:
        loss = compute_ell(data, colors, theta)
        if loss < best_loss:
            best_loss = loss
            best_theta = theta
    return best_theta


def minimize_ell_sorted(data, colors):
    n = len(data)
    total_blue = sum(1 for c in colors if c == 'blue')
    blue_left = 0
    red_left = 0

    best_theta = data[0] - 1.0
    best_loss = red_left + (total_blue - blue_left)

    for i in range(n - 1):
        # move boundary to the right of data[i]
        if colors[i] == 'blue':
            blue_left += 1
        else:
            red_left += 1
        theta = (data[i] + data[i + 1]) / 2
        loss = red_left + (total_blue - blue_left)
        if loss < best_loss:
            best_loss = loss
            best_theta = theta

    # consider boundary after the largest point
    if colors[-1] == 'blue':
        blue_left += 1
    else:
        red_left += 1
    loss = red_left + (total_blue - blue_left)
    if loss < best_loss:
        best_theta = data[-1] + 1.0

    return best_theta


# if __name__ == "__main__":
#     # basic separation where all blues < all reds
#     pts = [5, 1, 3, 10]
#     cols = ['red', 'blue', 'blue', 'red']
#     t = learn_theta(pts, cols)
#     print("learn_theta:", t, "loss:", compute_ell(pts, cols, t))

#     # overlap case. expect minimal loss of 1
#     pts2 = [0, 2, 4, 6]
#     cols2 = ['blue', 'red', 'blue', 'red']
#     t2 = minimize_ell(pts2, cols2)
#     print("minimize_ell (unsorted) theta:", t2, "loss:", compute_ell(pts2, cols2, t2))

#     # sorted data, equal red/blue counts, smallest is blue. expect loss 0
#     pts3 = [0, 1, 2, 3, 4, 5]
#     cols3 = ['blue', 'blue', 'blue', 'red', 'red', 'red']
#     t3 = minimize_ell_sorted(pts3, cols3)
#     print("minimize_ell_sorted theta:", t3, "loss:", compute_ell(pts3, cols3, t3))
