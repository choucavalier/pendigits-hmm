from scipy.cluster.vq import vq, kmeans, whiten

def get_digit_kmeans_centroids(digits, n_clusters):

    data = []
    for digit in digits:
        for curve in digit.curves:
            for point in curve:
                data.append(point)

    centroids, _ = kmeans(data, n_clusters)

    return centroids
