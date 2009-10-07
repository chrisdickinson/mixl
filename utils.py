import os
def mixl_find_file(filename, paths=[]):
    for path in paths:
        file_name = os.path.join(path, filename)
        if os.path.exists(file_name):
            return file_name
    return None

def mixl_open(filename, paths=[]):
    found_file = mixl_find_file(filename, paths)
    if found_file is None:
        raise IOError()
    file = open(found_file)
    file_contents = ''.join([line for line in file])
    file.close()
    return file_contents 

def mixl_import(filename, paths, **kwargs):
    """
        attempt to load a pickled version of a module when available
        returns a full parser object
    """
    from parser import Parser
    import pickle 
    found_file = mixl_find_file(filename, paths)
    if found_file is None:
        raise IOError()
    pickled_file = found_file + 'c'
    if os.path.exists(pickled_file):
        plain_mtime = os.path.getmtime(found_file)
        pickled_mtime = os.path.getmtime(pickled_file)
        if plain_mtime < pickled_mtime:
            pickled_file_object = open(pickled_file, 'rb')
            parser = pickle.load(pickled_file_object)
            pickled_file_object.close()
            return parser
    file = open(found_file)
    file_contents = ''.join([line for line in file])
    file.close()

    parser = Parser(file_contents, paths=paths, **kwargs)
    pickled_file_object = open(pickled_file, 'wb')
    pickle.dump(parser, pickled_file_object)
    pickled_file_object.close()
    return parser
