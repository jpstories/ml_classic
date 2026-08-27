def only_even(numbers):
    for i, x in enumerate(numbers):
        if x % 2 != 0:
            return False, i
    return True

print(only_even([2, 4, 6]))
print(only_even([1, 2, 3]))

# Вывод программы:
# True
# (False, 0)
#===================================
def check_password(pwd):
    return pwd == password

password = "Python"
print(check_password("123"))

# Вывод программы:
# False
#===================================
def list_modify():
    del sample[-1]

sample = [1, 2, 3]
list_modify()
print(sample)
# Вывод программы:
# [1, 2]
#===================================
def list_modify_1(list_arg):
    # создаём новый локальный список, не имеющий связи с внешним
    list_arg = [1, 2, 3, 4]

def list_modify_2(list_arg):
    # меняем исходный внешний список
    # операция += модифицирует объект на месте.
    list_arg += [4]

sample_1 = [1, 2, 3]
sample_2 = [1, 2, 3]
list_modify_1(sample_1)
list_modify_2(sample_2)
print(sample_1)
print(sample_2)

# Вывод программы:
# [1, 2, 3]
# [1, 2, 3, 4]
#=================================== X
def inc():
    global x
    x += 1
    print(f"Количество вызовов функции равно {x}.")

x = 0
inc() # 1
inc() # 2
inc() # 3
#=================================== O
def f(count):
    count += 1
    print(f'Количество вызовов функции равно {count}.')
    return count

count_f = 0
count_f = f(count_f) # 1
count_f = f(count_f) # 2
count_f = f(count_f) # 3
