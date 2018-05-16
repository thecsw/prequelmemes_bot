
# I don't want to write out the open files
# manually, so I would just prefer a simple
# anstract functions

def write_file(file_name, data):
    with open(file_name, "w") as w:
        w.write(str(data))
    w.close

def append_file(file_name, data):
    with open(file_name, "a") as a:
        a.write(str(data))
    a.close

def read_file(file_name):
    with open(file_name, "r") as r:
        data = r.read()
    r.close()
    return data
