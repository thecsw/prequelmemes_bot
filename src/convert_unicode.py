
# The following scripts will just go to the ./subtitles directory and
# make all the files in it UTF-8 enconding compatible
# Pretty messy, but hey, It Just Works!

import sys, os

folder = "./subtitles/"

for (root, dirs, files) in os.walk(folder):   

    for file_name in files:
        
        subtitle_name = folder + file_name;
        print("File name: {}".format(subtitle_name))
        
        with open(subtitle_name, "r+", encoding="ISO-8859-1") as f:
            try:
                thing = f.read()
            except Exception as e:
                print("Failed to read the file.\n\t{}\n".format(e))
            finally:
                f.close()
                print("\tSuccessfully read the file!")

        try:
            thing.encode("utf-8")
            print("\tSuccessfully encoded to UTF-8!")
        except Exception as e:
            print("Failed at encoding the file to UTF-8.\n\t{}\n".format(e))
                
        with open(subtitle_name, "w+") as f:
            try:
                f.write(thing)
            except Exception as e:
                print("Failed at writing the contents to the file.\n\t{}\n".format(e))
            finally:
                f.close()
                print("\tSuccessfully wrote the file!\n")

    
