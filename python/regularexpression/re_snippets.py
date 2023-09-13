import re


def find_all_numbers(s):
    numbers = re.findall('\d+', s)
    if len(numbers) >0:
        print(numbers[0])


if __name__ == '__main__':
    find_all_numbers('50M')
