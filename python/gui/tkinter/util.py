import re


def val_email_addr(result: dict) -> bool:
    pattern = re.compile(r'b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    try:
        addr = '' if result.get('address') is None else result.get('address')
        assert pattern.fullmatch(addr)
    except AssertionError:
        return False
    return True


def val_ip(result: dict) -> bool:
    pattern = re.compile(r'^((?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)$')
    try:
        addr = '' if result.get('ip') is None else result.get('ip')
        assert pattern.fullmatch(addr)
    except AssertionError:
        return False
    return True

if __name__ == '__main__':
    pass