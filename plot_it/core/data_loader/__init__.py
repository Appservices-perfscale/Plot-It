import yaml, json

def load_yaml_file(filepath:str):
    '''Read contents of YAML file from a filepath.'''
    with open(filepath, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file.read())

def load_json_file(filepath:str):
    '''Read contents of JSON file from a filepath.'''
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.loads(file.read())
