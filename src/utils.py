
# I don't want to write out the open files
# manually, so I would just prefer a simple
# anstract functions

def write_file(file_name, data):
    with open(file_name, "w") as w:
        w.write(str(data))
    w.close
    return True
    
def append_file(file_name, data):
    with open(file_name, "a") as a:
        a.write(str(data))
    a.close
    return True

def read_file(file_name):
    with open(file_name, "r") as r:
        data = r.read()
    r.close()
    return data

def write_array(file_name, arr):
    with open(file_name, "w") as w:
        for i in arr:
            w.writelines(f"{str(i)}\n")
    w.close
    return True
    
def read_array(file_name):
    arr = []
    with open(file_name, "r") as r:
        arr = r.readlines()
        arr = [x.replace("\n", "") for x in arr]
        r.close()
    return arr
