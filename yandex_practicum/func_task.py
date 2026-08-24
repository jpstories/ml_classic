# def number_length(n):
#     return len(str(n).lstrip("-"))

# result = number_length(-100500)
# print(result)

# Использование global __count: Директива сообщает Python, что операция += 1 должна перезаписать значение именно в глобальной переменной, 
# а не создавать новую локальную переменную внутри функции.Чтение переменной в get_count(): 
# Так как внутри этой функции значение переменной не меняется, директива global не требуется — Python автоматически найдет __count в глобальной области видимости.

# Особенность приватности в модулях: Двойное подчеркивание __ на уровне модуля (вне классов) в Python защищает переменную от случайного импорта при использовании 
# конструкции from имя_модуля import *. При этом внутри самого файла она остается доступной для функций.

# def max2D(matrix):
#     return max(num for arr in matrix for num in arr)

# result = max2D([[-5, -43, 72, 89], [-40, 92, -1, -173], [30, -75, 23, 94]])
# print(result)


def fragments(numbers):
    if not numbers:
        return []

    result = [[numbers[0]]]

    for curr in numbers[1:]:
        if curr > result[-1][-1]:
            result[-1].append(curr)
        else:
            result.append([curr])

    return result

result = fragments([-4, -2, 5, 0, 3, 7, -8, -2, 6, 7, 6, 8, 10, 5, 7, 8])


def month(number, language):
    NAMES = {
        'ru': [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ],
        'en': [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    }
    return NAMES[language][number - 1]



def split_numbers(text):
    return tuple(int(num) for num in text.split())



def find_mountains(data):
    # Перебираем внутренние строки матрицы (соседи сверху и снизу есть у строк с 1 по предпоследнюю)
    return tuple(
        (r + 1, c + 1)
        for r in range(1, len(data) - 1)
        for c in range(1, len(data[r]) - 1)
        if data[r][c] > data[r-1][c]   # Больше соседа сверху
        and data[r][c] > data[r+1][c] # Больше соседа снизу
        and data[r][c] > data[r][c-1] # Больше соседа слева
        and data[r][c] > data[r][c+1] # Больше соседа справа
    )
result = find_mountains([
    [1, 1, 1, 1, 1, 1],
    [1, 2, 1, 5, 4, 1],
    [1, 1, 1, 3, 4, 3],
    [2, 3, 3, 1, 2, 3],
    [1, 2, 1, 3, 2, 1]
])
print(result)  # Выведет строго: ((2, 2), (2, 4))




arr = set()
def modern_print(text):
    if text not in arr:
        arr.add(text)
        print(text)

modern_print("Hello!")
modern_print("Hello!")
modern_print("How do you do?")
modern_print("Hello!")



def can_eat(horse, other):
    x, y = horse
    x1, y1 = other

    if (x1 - x == 2 and y1 - y == 1) or (x1 - x == 1 and y1 - y == 2):
        return True
        
    return False


result = can_eat((5, 5), (6, 6))
print(result)



def get_dict(text):
    d = {}
    chars = text.strip().split(";")
    for char in chars:
        k, v = char.split("=")
        d[k] = v
    return d

result = get_dict('id=3-76;ip=127.0.0.1;phone=+7-(123)-456-78-90')
print(result)



def is_palindrome(x):
    if isinstance(x, (list, tuple)):
        return x == x[::-1]

    if isinstance(x, (str, int, float)):
        s = str(x)
        return s == s[::-1]

    return False


print(is_palindrome(123))
print(is_palindrome([1, 2, 1, 2, 1]))