import re


def find_first_number(s):
    """

    @param s: string, example '50Mb'
    """
    numbers = re.findall('\d+', s)
    if len(numbers) > 0:
        return numbers[0]
    return None


if __name__ == '__main__':
    find_first_number('50M')
