import os

ddir = "./data_raw/"
# modify filenames
for filename in os.listdir(ddir):
    newname = filename
    for ch in filename:
        if (ch in ['.', '_', '-']) or (47 < ord(ch) 58) or (64 < ord(ch) < 91) or (96 < ord(ch) < 123): continue
        else: newname = newname.replace(ch, "")
    newname = newname.replace("__", "_")
    os.rename(ddir+filename, ddir+newname)

# fix unwanted new lines and non-utf-8 encodings
for filename in os.listdir(ddir):
    content = open(ddir+filename, errors='ignore').read()
    new_cont = content.replace("\n@", " @")
    f = open(ddir+filename, 'w')
    f.write(new_cont)
    f.close()
import os

# fix feature name problems
str1 = "string_to_be_replaced"
str2 = "new_string"
for filename in os.listdir(ddir):
    content = open(ddir+filename, errors='ignore').read()
    new_cont = content.replace(str1, str2)
    f = open(ddir+filename, 'w')
    f.write(new_cont)
    f.close()
