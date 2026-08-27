from sys import stdin

total = 0

for line in stdin:
    line = line.strip()
    number = [int(num) for num in line.split()]
    total += sum(number)

print(total)