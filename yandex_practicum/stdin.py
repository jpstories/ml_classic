from sys import stdin

# mean = 0
# count = 0

# for line in stdin:
#     height_old, height_current = line.strip().split()[1:]
#     print(height_old, height_current)
#     height_diff = int(height_current) - int(height_old)
#     print(height_diff)
#     mean += height_diff
#     count += 1

# mean = mean / count

# print(round(mean))
#==============================================================
# clean = [line.split("#")[0].rstrip("\n") for line in stdin if not line.startswith("#")]
# print(*clean, sep="\n")
#==============================================================
# text = [line.rstrip("\n") for line in stdin]
# output = [text[i] for i in range(0, len(text) - 1) if text[-1].lower() in text[i].lower()]
# print(*output, sep="\n")
#==============================================================
# words = [word for line in stdin for word in line.rstrip("\n").split()]
# palindromes = {word for word in words if word.lower() == word.lower()[::-1]}
# print(*sorted(palindromes), sep="\n")
#==============================================================