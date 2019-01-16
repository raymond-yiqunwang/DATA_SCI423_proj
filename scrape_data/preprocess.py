import os

for filename in os.listdir("./data_raw"):
    content = open("./data_raw/"+filename, errors='ignore').read()
    new_cont = content.replace("\n@", " @")
    f = open("./data_raw/"+filename, 'w')
    f.write(new_cont)
    f.close()
