global __count # Директива глобальной переменной
# а не создавать новую локальную переменную внутри функции.
# Python автоматически найдет __count в глобальной области видимости.
# Приватность в модулях: Двойное подчеркивание __ в Python защищает переменную от случайного импорта



def number_length(n):
    return len(str(n).lstrip("-"))
result = number_length(-100500)
print(result)



def max2D(matrix):
    return max(num for arr in matrix for num in arr)
result = max2D([[-5, -43, 72, 89], [-40, 92, -1, -173], [30, -75, 23, 94]])
print(result)



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




# 2 =================================================================================================
# price, discount - позиционные аргументы
def final_price(price, discount):
    return price - price * discount / 100




# discount - значение по умолчанию, присваивается один раз — в момент объявления функции
def final_price(price, discount=1):
    return price - price * discount / 100




# list_arg - список по умолчанию
def add_value(x, list_arg=[]):
    list_arg += [x]
    return list_arg

print(add_value(0))
print(add_value(0, [1, 2, 3]))
print(add_value(1))
# [0]
# [1, 2, 3, 0]
# [0, 1] <- побочный эффект




# решение, передавать None вместо []
def add_value(x, list_arg=None):
    if list_arg is None:
        list_arg = []
    list_arg += [x]
    return list_arg
print(add_value(0))
print(add_value(0, [1, 2, 3]))
print(add_value(1))




# Именованные аргументы позволяют не соблюдать порядок 
def final_price(price, discount=1):
    return price - price * discount / 100

print(final_price(discount=10, price=1000)) # OK
# print(final_price(discount=10, 1000))       # ERROR
# позиционные аргументы всегда должны идти первыми, а именованные — после них




# любое кол-во позиционных аргументов
# -> кортеж *args
print(1,2,3,4,5)



# любое кол-во позиционных аргументов
# -> кортеж *args
def final_price(*prices, discount=1):
    return [price - price * discount / 100 for price in prices]
print(final_price(100, 200, 300, discount=5))
# [95.0, 190.0, 285.0]





# любое кол-во именованных аргументов
# -> словарь **kwargs
def final_price(*prices, discount=1, **kwargs):
    low = kwargs.get("price_low", min(prices))
    high = kwargs.get("price_high", max(prices))
    return [price - price * discount / 100 for price in prices if low <= price <= high]
print(final_price(100, 200, 300, 400, 500, discount=5, price_low=200))
print(final_price(100, 200, 300, 400, 500, discount=5, price_low=200, price_high=350))
# [190.0, 285.0, 380.0, 475.0]
# [190.0, 285.0]




#==========================================================================================
# функции высшего порядка -> Функция, которая принимает ссылку на другую функции/метод как аргумент

# filter()
def get_positive(x):
    return x > 0
result = filter(get_positive, [-1, 5, 6, -10, 0])
print(result) # iterator
print(", ".join(str(x) for x in result)) # 5, 6



# filter()
result = filter(str.isalpha, "123ABcd()")
print("".join(result)) # ABcd




# map()
def square(x):
    return x ** 2
result = map(square, range(5))
print(", ".join(str(x) for x in result))




# map()
result = map(str.lower, ["abCD", "EFGh", "IJkl"])
print("\n".join(result))




# map()
# numbers = list(map(int, input().split()))





#==========================================================================================
lambda x: x > 0
# x аргумент функции
# : возвращаемое значение (True)
# для простой логики



result = filter(lambda x: x > 0, [-1, 5, 6, -10, 0])
print(", ".join(str(x) for x in result)) # 5, 6




result = map(lambda x: x ** 2, range(5))
print(", ".join(str(x) for x in result)) # 0, 1, 4, 9, 16




lines = ["abcd", "ab", "abc", "abcdef"]
print(sorted(lines, key=lambda line: len(line)))
# ['ab', 'abc', 'abcd', 'abcdef']


# функция-ключ =============================================
# IN PROD
from typing import List, Tuple
# import pytest

def get_sort_attributes(text: str | None) -> Tuple[int, str]:
    if text is None:
        return 0, ""
    
    clean_text = text.strip().lower() 
    return len(clean_text), text

lines: List[str] = ["abcd", "ab", "ba", "acde"]
sorted_lines = sorted(lines, key=get_sort_attributes)

def test_get_sort_attributes():
    assert get_sort_attributes("abc") == (3, "abc")
    assert get_sort_attributes("") == (0, "")
#============================================================
# IN PROTOTYPE
lines = ["abcd", "ab", "ba", "acde"]
print(sorted(lines, key=lambda line: (-len(line), line)))
# ['abcd', 'acde', 'ab', 'ba']
#============================================================
# Для одного критерия - С!
lines = ["abcd", "ab", "ba", "acde"]
print(sorted(lines, key=len))
#============================================================




# min()
# самая длинная строка и лексикографически меньшую
lines = ["abcd", "ab", "ba", "acde"]
print(min(lines, key=lambda line: (-len(line), line))) # abcd




#=================================================================
#=================================================================
#=================================================================
# Альтернатива: генераторные выражения
# Часто то, что можно сделать с map() или filter(), проще выразить 
# через генераторные выражения — они более наглядны и читаемы
result = (x for x in [-1, 5, 6, -10, 0] if x > 0)
print(", ".join(str(x) for x in result)) # 5, 6
#=================================================================
#=================================================================
#=================================================================






#=================================================================
# reduce()
from functools import reduce
actions_users = [
    {1, 2, 3, 4, 5},  # Зарегистрировались
    {2, 3, 5, 8},  # Заполнили профиль
    {3, 5, 7, 9},  # Сделали покупку
]
loyal_users = reduce(lambda acc, current: acc.intersection(current), actions_users)
print(loyal_users)  # Выведет: {3, 5}






# PRACTICE =================================================================
def make_matrix(size, value=0):
    if isinstance(size, tuple):
        n, m = size
    else:
        n = m = size

        return [
            [value for _ in range(n)]
            for _ in range(m)
        ]

def gcd(*nums):
    current_gcd = nums[0]

    for num in nums[1:]:
        a, b = current_gcd, num
        while b != 0:
            a, b = b, a % b
        current_gcd = a
        
    return current_gcd


def to_string(*args, sep=" ", end="\n"):
    return sep.join(str(arg) for arg in args) + end

print(to_string(1, 2, 3, end="!"))


def get_operator(op):
    operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "//": lambda x, y: x // y,
        "**": lambda x, y: x ** y
    }
    return operations[op]


def grow(*args, **kwargs):
    # Превращаем в список для возможности изменения элементов
    modified_args = list(args)
    
    # Перебираем все именованные параметры
    for key, value in kwargs.items():
        key_len = len(key)
        
        # Проверяем ИНДЕКСЫ позиционных аргументов на кратность длине ключа
        for i in range(len(modified_args)):
            if i % key_len == 0:
                modified_args[i] += value
                
    # Возвращаем результат в виде кортежа
    return tuple(modified_args)



RECIPES = {
    "Эспрессо": {"coffee": 1, "milk": 0, "cream": 0},
    "Капучино": {"coffee": 1, "milk": 3, "cream": 0},
    "Макиато": {"coffee": 2, "milk": 1, "cream": 0},
    "Кофе по-венски": {"coffee": 1, "milk": 0, "cream": 2},
    "Латте Макиато": {"coffee": 1, "milk": 2, "cream": 1},
    "Кон Панна": {"coffee": 1, "milk": 0, "cream": 1}
}


def order(*preferences):
    global in_stock
    for drink in preferences:
        if drink in RECIPES:
            recipe = RECIPES[drink]
            
            if (in_stock.get("coffee", 0) >= recipe["coffee"] and
                    in_stock.get("milk", 0) >= recipe["milk"] and
                    in_stock.get("cream", 0) >= recipe["cream"]):
                
                in_stock["coffee"] -= recipe["coffee"]
                in_stock["milk"] -= recipe["milk"]
                in_stock["cream"] -= recipe["cream"]
                
                return drink
                
    return "К сожалению, не можем предложить Вам напиток"




print(*filter(lambda x: sum(int(digit) for digit in str(abs(x))) % 2 == 0, (1, 2, 3, 4, 5)))





def get_repeater(func, count):
    def repeated_func(x):
        result = x
        for _ in range(count):
            result = func(result)
        return result
    
    return repeated_func

repeater = get_repeater(lambda x: x + 1, 5)
print(repeater(2))




# Обратная связь, callbacks
def login(username, password, success, error):
    summary = sum(ord(char) for char in username)
    summary *= len(username)
    hex_string = hex(summary)[2:].upper()
    
    if hex_string == password[::-1]:
        return success(username)
    else:
        return error(username)
    
def hello(username):
    print(f'Здравствуйте, {username}!')

def alert(username):
    print(f'!!! Попытка взлома аккаунта {username} !!!')
    print('Блокировка системы через...', 5, 4, 3, 2, 1, 'ТРЕВОГА!', sep='\n')

login('оченьМаленькийРозовыйПони', 'EDE5A', hello, alert)






lambda x: isinstance(x[1], list) and any(num % 2 == 0 for num in x[1] if isinstance(num, int))



# Преобразование словаря
print(dict(map(
    lambda x: (''.join(c for c in x[0].lower() if c.isalpha()), sum(x[1]) if isinstance(x[1], (list, set, tuple)) else x[1]),
    {'First 1': 2, 'second:': (2, 1, 1), 'THIRD': [1, 2, 3]}.items()
)))
# {'first': 2, 'second': 4, 'third': 6}





def secret_replace(text, **kwargs):
    # Превращаем текст в список символов, чтобы его удобно модифицировать
    result = list(text)
    
    # Перебираем правила замен (символ-ключ и кортеж его вариантов замен)
    for target_char, replacements in kwargs.items():
        # Счетчик, чтобы циклически перебирать варианты замен
        replace_index = 0
        replacements_len = len(replacements)
        
        # Проходим по каждому символу исходного текста
        for i in range(len(result)):
            if result[i] == target_char:
                # Берем очередную замену по кругу
                result[i] = replacements[replace_index % replacements_len]
                replace_index += 1
                
    # Собираем символы обратно в строку
    return "".join(result)






from datetime import datetime
import re

database = []

def insert(*users):
    """Добавляет информацию об одном или нескольких пользователях в базу."""
    if not users:
        return False
    
    global database
    for user in users:
        database.append(user)
    return True


def select(condition=None):
    """Выбирает пользователей по критерию и сортирует их по возрастанию id."""
    if not condition:
        return sorted(database, key=lambda x: x['id'])
    
    # Регулярное выражение разбирает строку вида: name > B или birth >= 12.04.2001
    pattern = r"^([a-zA-Z_]+)\s*(==|!=|>=|<=|>|<)\s*(.+)$"
    match = re.match(pattern, condition.strip())
    
    if not match:
        return []
        
    field, operator, value = match.groups()
    value = value.strip()
    
    filtered_users = []
    
    for user in database:
        user_value = user.get(field)
        if user_value is None:
            continue
            
        # Приведение типов для сравнения
        if field == 'id':
            compare_value = int(value)
        elif field == 'birth':
            user_value = datetime.strptime(user_value, "%d.%m.%Y")
            compare_value = datetime.strptime(value, "%d.%m.%Y")
        else:
            compare_value = value
            
        # Вычисление условий сравнения
        if operator == '==':
            is_match = user_value == compare_value
        elif operator == '!=':
            is_match = user_value != compare_value
        elif operator == '>':
            is_match = user_value > compare_value
        elif operator == '<':
            is_match = user_value < compare_value
        elif operator == '>=':
            is_match = user_value >= compare_value
        elif operator == '<=':
            is_match = user_value <= compare_value
        else:
            is_match = False
            
        if is_match:
            filtered_users.append(user)
            
    return sorted(filtered_users, key=lambda x: x['id'])