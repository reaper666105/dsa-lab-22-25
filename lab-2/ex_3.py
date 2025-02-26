# Задание 3.10
import sys
from collections import Counter
def main():
    arr = list(map(int, sys.argv[1:]))

    original_arr = arr[:]
    counter = Counter(arr)
    duplicates = [x for x, count in counter.items() if count > 1]

    if duplicates:
        print('Повторяющиеся элементы:', duplicates)
    else:
        print('Дублей нет')
    
    for i in range(len(arr)):
        if arr[i] < 10:
            arr[i] = 0
        elif arr[i] > 20:
            arr[i] = 1
    
    print('Исходный массив:', original_arr)
    print('Преобразованный массив:', arr)

if main == '__main__':
    main