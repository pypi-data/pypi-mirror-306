from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


# 计算距离
def dtw_distance(x, y):
    distance, path = fastdtw(x, y, dist=euclidean)
    path_count = len(path)
    normalized_distance = distance / path_count
    return distance, normalized_distance
