import configparser

def parse(file, section=None, key=None):
    config = configparser.ConfigParser()
    config.read('etc/'+file+'.config')
    if section and key:
        return config[section][key]
    elif key:
        return config['DEFAULT'][key]
    return config