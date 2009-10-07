import os
def mixl_find_file(filename, paths=[]):
    """
        mixl_find_file(<filename str>, <paths list>)
            search for filename along all paths,
            return a string with the filename appended to
            the first path where it is found.
    """
    for path in paths:
        file_name = os.path.join(path, filename)
        if os.path.exists(file_name):
            return file_name
    return None

def mixl_open(filename, paths=[]):
    """
        mixl_open(<filename str>, <paths list>)
            looks for a file along the available paths,
            returns the files contents if found. 
    """
    found_file = mixl_find_file(filename, paths)
    if found_file is None:
        raise IOError()
    file = open(found_file)
    file_contents = ''.join([line for line in file])
    file.close()
    return file_contents 

def mixl_import(filename, paths, **kwargs):
    """
        mixl_import(<filename str>, <paths list>, **kwargs)
            attempts to locate a pickled copy of a parser object given 
            paths and a filename to search for.

            if no pickled copy is found, but a non-pickled css file is found,
            it'll parse that file and compile the resultant parser.

            kwargs will be passed along to the parser if one is created.

            returns parser on success, throws IOError on failure
    """
    from parser import Parser
    import pickle 
    found_file = mixl_find_file(filename, paths)
    if found_file is None:
        raise IOError()
    pickled_file = found_file + 'c'
    if os.path.exists(pickled_file):
        # if the source file is newer than the pickled copy,
        # rebuild the pickle
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
