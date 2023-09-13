import datetime


def with_token(username, password):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('username=', username)
            print('password=', password)
            print('I have gotten token')
            token = '12fasdf3456'
            result = func(token=token, *args, **kwargs)
            return result

        return wrapper

    return decorator


@with_token(username='shur', password='shur')
def get_content(self, token):
    print('I am getting content. token is', token)


if __name__ == '__main__':
    print('now is:', datetime.datetime.now())
    get_content()
