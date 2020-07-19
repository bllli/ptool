from xmlrpc.client import ServerProxy


def check_info():
    client = ServerProxy('http://{}:{}/RPC2'.format('127.0.0.1', 9001))
    return {
        'django': client.supervisor.getProcessInfo('django'),
        'celery': client.supervisor.getProcessInfo('celery'),
        'django_init': client.supervisor.getProcessInfo('django_init'),
    }


def restart_app(process):
    client = ServerProxy('http://{}:{}/RPC2'.format('127.0.0.1', 9001))
    if not process:
        processes = ['django', 'celery']
    else:
        processes = [process]
    for process in processes:
        client.supervisor.stopProcess(process)
        client.supervisor.startProcess(process)


if __name__ == '__main__':

    # check_django()
    print(1)
