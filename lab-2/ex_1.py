# Задание 1.1
import random
random.seed(42)

x_3 = [random.randint(1,100) for _ in range(3)]

print('Задание 1.1', min(x_3))

# Задание 1.2

range_1_100 = [random.randint(1,100) for _ in range(3)]
print('Задание 1.2', [num for num in range_1_100 if 1 <= num <= 50])

# Задание 1.3
from typing import List
def sequense_n(n: List, len_seq=10) -> List:
    result = []
    
    for i in range(1, len_seq+1):
        result.append(i*n)
    return result
print('Задание 1.3', sequense_n(10))

# Задание 1.4

list_for_1_4 = [random.randint(1,100) for _ in range(10)]
total = 0
i = 0
while i < len(list_for_1_4):
    total += list_for_1_4[i]
    i +=1
print('Задание 1.4', 'total_sum: ', total, 'total len: ', i)



# Задание 2.10

text = 'лабораторную выполнил юшков вадим'
print('Задание 2.10', text.title())