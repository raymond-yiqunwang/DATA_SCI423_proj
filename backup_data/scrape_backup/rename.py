import os

for filename in os.listdir("./data_raw"):
    newname = filename.replace("__", "_")
    os.rename("./data_raw/"+filename, "./data_raw/"+newname)
