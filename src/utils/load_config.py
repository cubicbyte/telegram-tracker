import yaml

def load_config(path: str, noprint: bool=False) -> dict:
    try:
        config = yaml.safe_load(open(path))
    except FileNotFoundError:
        if not noprint:
            print(f'ERROR: Can\'t read file {path}')
        config = {}

    return config

def main():
    import sys
    import json

    if len(sys.argv) < 2:
        filename = 'config.yml'
    else:
        filename = sys.argv[1]

    config = load_config(filename, noprint=True)
    config_json = json.dumps(config)
    print(config_json)

if __name__ == '__main__':
    main()