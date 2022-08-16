import os

def mkdir_if_not_exists(root: str, dir: str) -> None:
    dirpath = os.path.join(root, dir)

    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

def init_dirs(root: str) -> None:
    mkdir_if_not_exists(root, 'logs')
    mkdir_if_not_exists(root, 'sessions')

def main():
    init_dirs('/')

if __name__ == '__main__':
    main()

