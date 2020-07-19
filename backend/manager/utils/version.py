import os


def read_version(version_file_path: str):
    if not os.path.isfile(version_file_path):
        return '未读取到版本信息!'
    with open(version_file_path, 'r') as f:
        text = f.read()
    return text


if __name__ == '__main__':
    print(read_version('../app/VERSION'))
