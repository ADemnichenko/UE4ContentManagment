import os
pack_path = "./NBA_pak/"
unpacker_path = "ue4/Engine/Binaries/Win64" #full path to UnrealPak.exe
BUILD_PATH = "./NBA_pak/" #full path to the build content


def extract():
    for d, subdir, files in os.walk(pack_path):
        for f in files:
            os.system(
                "{0}/UnrealPak.exe {1} -Extract {2}".format(
                    unpacker_path,
                    os.path.join(d, f),
                    os.path.join(os.path.abspath(d), f.replace(".pak", ""))
                ))


def pak():

    # list_of_packages = ["temp"]
    subdir = "Characters/Models/Npc"
    for d, s, f in os.walk(os.path.join(BUILD_PATH, subdir)):
        list_of_packages = s
        break

    for l in list_of_packages:
        os.system(
            "{0}/UnrealPak.exe {1} -Create={2} -Compress".format(
                unpacker_path,
                os.path.abspath(os.path.join("./NBA_pak/temp", "{0}.pak".format(l))),
                os.path.abspath(os.path.join(BUILD_PATH,subdir,l))
            )
        )

def get_size():
    for d, s, f in os.walk(os.path.join(pack_path, "temp")):
        for file in f:
            print(str(os.path.getsize(os.path.join(d, file)) / 1000000).replace(".", ","))
            # print("{0} - {1}".format(file.split(".")[0], str(os.path.getsize(os.path.join(d, file)) / 1000000)).replace(".", ","))

extract()
# pak()
# get_size()
