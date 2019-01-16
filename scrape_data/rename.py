import os

for filename in os.listdir("./data_raw"):
    newname = filename
    for ch in filename:
        if (ch is '.') or (ch is '_') or (ch is '-') or (ord(ch) > 47 and ord(ch) < 58) or (ord(ch) > 64 and ord(ch) < 91) or (ord(ch) > 96 and ord(ch) < 123): continue
        else: newname = newname.replace(ch, "")
    newname = newname.replace("__", "_")
    os.rename("./data_raw/"+filename, "./data_raw/"+newname)
