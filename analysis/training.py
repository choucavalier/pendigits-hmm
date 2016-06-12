from scipy.cluster.vq import vq, kmeans, whiten

def get_digit_kmeans_centroids(digits, n_clusters):

    data = []
    for digit in digits:
        for curve in digit.curves:
            for point in curve:
                data.append(point)

    centroids, _ = kmeans(data, n_clusters)

    return centroids


def set_digit_observations(digits, centroids):

    for digit in digits:

        observations = []
        observations.append(254) # pen down

        i = 0
        while i < len(digit.curves):

            curve = digit.curves[i]

            curve_data = []
            for point in curve:
                curve_data.append(point)
            idx,_ = vq(curve_data, centroids)
            for value in idx:
                observations.append(value)

            i += 1
            if i < len(digit.curves):
                observations.append(255) # pen up
                observations.append(254) # pen down

        observations.append(255) # pen up
        digit.set_observations(observations)
