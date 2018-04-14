
file_name = "Star_Wars_Episode_II_:_Attack_of_the_Clones.srt"

with open(file_name, "r+", encoding="ISO-8859-1") as f:
    thing = f.read()
f.close()

print(thing)
thing.encode("utf-8")

with open(file_name, "w+") as f:
    f.write(thing)
f.close()
