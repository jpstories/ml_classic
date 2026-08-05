import gc
import logging
import os
from typing import Tuple
import numpy as np
import psutil
from cs231n.data_utils import load_CIFAR10

logger = logging.getLogger(__name__)

"""
1. Инкапсуляция (Локальный Scope): Код обернут в функцию, все очищается
2. Тайп-хинтинг (Type Hinting): линтерам (mypy) проверять строгость типов.
3. Строгая документация (Docstrings): Написан стандарт Google Docstring. 
4. Вместо assert используются ValueError и FileNotFoundError. Эта валидация сработает со 100% гарантией при любых флагах оптимизации Python.
"""

def get_memory_usage_mb() -> float:
    """Возвращает текущее потребление RAM процессом в Мегабайтах."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024**2)

def load_and_validate_cifar10(data_dir: str,) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Загружает датасет CIFAR-10 и проводит его строгую валидацию.
    Args:
        data_dir: Путь к директории с батчами датасета.
    Returns:
        Кортеж из четырех NumPy массивов: (X_train, y_train, X_test, y_test).
    Raises:
        FileNotFoundError: Если директория с данными не существует.
        ValueError: Если загруженные данные не прошли проверку размерности.
    """
    # 1. Защита на входе, проверяем существование папки
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found at: {data_dir}")

    logger.info(
        "Starting CIFAR-10 loading pipeline, Current RAM: %.2f MB",
        get_memory_usage_mb(),
    )

    # 2. Загрузка данных
    try:
        X_train, y_train, X_test, y_test = load_CIFAR10(data_dir)
    except Exception as e:
        logger.error("Failed to execute load_CIFAR10: %s", e)
        raise

    logger.info(
        "Data loaded into RAM. Current RAM: %.2f MB", get_memory_usage_mb()
    )

    # 3. Индустриальный Fail-Fast (Проверка качества данных, которая НЕ отключится в проде)
    if X_train.shape[0] != 50000:
        raise ValueError(
            f"Dataset corruption: expected 50000 train images, got {X_train.shape[0]}"
        )

    if X_test.shape[0] != 10000:
        raise ValueError(
            f"Dataset corruption: expected 10000 test images, got {X_test.shape[0]}"
        )

    if X_train.shape[0] != y_train.shape[0]:
        raise ValueError(
            f"Shape mismatch: Train images ({X_train.shape[0]}) don't match labels ({y_train.shape[0]})"
        )

    logger.info(
        "Data validation successful. Shapes: Train %s, Test %s",
        X_train.shape,
        X_test.shape,
    )

    return X_train, y_train, X_test, y_test