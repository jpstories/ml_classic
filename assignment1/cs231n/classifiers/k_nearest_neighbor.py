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

        # keepdims вернет матрицу (не вектор)
        X_squared = np.sum(X**2, axis=1, keepdims=True) # матрица (500, 1)
        X_train_squared = np.sum(self.X_train**2, axis=1) # вектор (5000,)
        X_X_train = 2 * np.dot(X, self.X_train.T) # (M × N) × (N × K) = (500 × 5000)

        # Original:     (500, 1)    (500, 5000)      (5000,)
        # Broadcasting: (500, 5000) (500, 5000) (500, 5000)

        # X_squared виртуально расширяется вправо до (500, 5000)
        # X_train_squared виртуально расширяется вниз до (500, 5000)
        dists = np.sqrt(X_squared - X_X_train + X_train_squared)
        return dists

    def predict_labels(self, dists, k=1):

        # Готовим место под ответы
        num_test = dists.shape[0]
        y_pred = np.zeros(num_test)

        # Цикл выполнится 500 раз
        for i in range(num_test):
            closest_y = []
            # Берем 5000 расстояний у 1 картинки 
            # np.argsort - возвращает индексы в порядке возрастания
            # [:k] берет первые k элементов
            closest_idxs = np.argsort(dists[i, :])[:k]
            # Получает классы соседей (тип картинки)
            closest_y = self.y_train[closest_idxs]
            # Считаем сколько раз встретился каждый класс среди соседей
            counts = Counter(closest_y)
            # Приоритет отдается максимальной частоте, выбирается класс-победитель
            most_common_label = min(counts.keys(), key=lambda x: (-counts[x], x))
            # Записываем победителя
            y_pred[i] = most_common_label

        return y_pred
