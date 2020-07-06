from xmlrpc.client import ServerProxy


def check_info():
    client = ServerProxy('http://{}:{}/RPC2'.format('127.0.0.1', 9001))
    return {
        'django': client.supervisor.getProcessInfo('django'),
        'celery': client.supervisor.getProcessInfo('celery'),
        'django_init': client.supervisor.getProcessInfo('django_init'),
    }


if __name__ == '__main__':

    # check_django()
    print(1)
