from builtins import range
from builtins import object
import numpy as np
from collections import Counter
import math


class KNearestNeighbor(object):
    """Алгоритм поиска ближайших соседей с разными методами"""

    def __init__(self):
        pass

    def train(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X, k=1, num_loops=0):
        # Гибкость тестирования методов
        if num_loops == 0:
            dists = self.compute_distances_no_loops(X)
        elif num_loops == 1:
            dists = self.compute_distances_one_loop(X)
        elif num_loops == 2:
            dists = self.compute_distances_two_loops(X)
        else:
            raise ValueError("Invalid value %d for num_loops" % num_loops)

        return self.predict_labels(dists, k=k)

    # 1. (slow)
    def compute_distances_two_loops(self, X):
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        for i in range(num_test):
            for j in range(num_train):
                # вычитаем r g b из r g b, смотрим разницу двух картинок
                dists[i, j] = math.sqrt(((X[i] - self.X_train[j])**2).sum())
        return dists
        
    # 2. (middle)
    def compute_distances_one_loop(self, X):
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        for i in range(num_test):
            dists[i, :] = np.sqrt(np.sum((self.X_train - X[i]) ** 2, axis=1))
        return dists

    # 3. (fast)
    def compute_distances_no_loops(self, X):
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        X_squared = np.sum(X**2, axis=1, keepdims=True)
        X_train_squared = np.sum(self.X_train**2, axis=1)
        two_X_X_train = 2 * np.dot(X, self.X_train.T)
        # сложнейший расчет за один шаг за счет keepdims=True
        dists = np.sqrt(X_squared - two_X_X_train + X_train_squared)
        return dists

    def predict_labels(self, dists, k=1):
        num_test = dists.shape[0]
        y_pred = np.zeros(num_test)
        for i in range(num_test):
            closest_y = []
            closest_idxs = np.argsort(dists[i, :])[:k]
            closest_y = self.y_train[closest_idxs]
            counts = Counter(closest_y)
            # приоритет отдается максимальной частоте
            most_common_label = min(counts.keys(), key=lambda x: (-counts[x], x))
            y_pred[i] = most_common_label

        return y_pred
