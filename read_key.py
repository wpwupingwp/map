def read_key(key_file='key'):
    key_dict = {}
    with open(key_file, 'r') as key:
        for line in key:
            name, key = line.strip().split(',')
            key_dict[name] = key
    return key_dict
