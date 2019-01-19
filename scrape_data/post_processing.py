import os

# modify filenames
for filename in os.listdir("./data_raw"):
    newname = filename
    for ch in filename:
        if (ch in ['.', '_', '-']) or (47 < ord(ch) 58) or (64 < ord(ch) < 91) or (96 < ord(ch) < 123): continue
        else: newname = newname.replace(ch, "")
    newname = newname.replace("__", "_")
    os.rename("./data_raw/"+filename, "./data_raw/"+newname)

# fix unwanted new lines and non-utf-8 encodings
for filename in os.listdir("./data_raw"):
    content = open("./data_raw/"+filename, errors='ignore').read()
    new_cont = content.replace("\n@", " @")
    f = open("./data_raw/"+filename, 'w')
    f.write(new_cont)
    f.close()
import os

str1 = "Charpy Impact "
str2 = "Charpy Impact"
# fix feature name problems
for filename in os.listdir("./data_raw"):
    content = open("./data_raw/"+filename, errors='ignore').read()
    new_cont = content.replace(str1, str2)
    f = open("./data_raw/"+filename, 'w')
    f.write(new_cont)
    f.close()
