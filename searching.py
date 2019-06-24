import os
import shutil
import xlsxwriter
import pprint
import json
import datetime
from collections import defaultdict, OrderedDict

SOURCE_PATH = "./NBA/"
BUILD_PATH = "./NBA_pak/" #full path to build content
EXTENSIONS = (".ubulk", ".uasset", ".uexp")


def json_out(path="./", data={}, name="default"):
    if isinstance(data, dict):
        json_path = os.path.join(path, "{0}".format(datetime.date.today()))
        os.makedirs(json_path, exist_ok=True)
        with open(os.path.join(json_path, "{0}.json".format(name)), "w") as out:
            json.dump(data, out)
    else:
        print("data is {0}, need {1}".format(data.__class__.__name__, dict.__name__))


def json_load(path=""):
    if path:
        with open(path, "r") as data:
            return json.load(data, object_pairs_hook=OrderedDict)
    else:
        print("You need to enter the path to json file!")


def check_asset_by_filter(file, filter=""):
    with open(file, "r") as txt:
        for line in txt:
            if filter in line:
                return True


def get_all_assets_ue4(path="./", asset_type="", filter=""):
    directory = os.path.join(path, asset_type, "Game")
    data = defaultdict(dict)
    data["data"]["size"] = 0
    i = 0
    for dir_path, subdir_path, files in os.walk(directory):
        if files:
            for file in files:
                asset_path = dir_path.replace(os.path.join(path, asset_type), "")
                filename = file.split(".")
                if filter:
                    if check_asset_by_filter(os.path.join(dir_path, file), filter):
                        data["assets"][i] = {
                            "name": filename[0],
                            "path": "{0}/{1}".format(asset_path.replace("\\", "/"), filename[0])}
                        data["data"]["amount"] = + i
                        data["data"]["size"] += os.path.getsize(os.path.join(dir_path, file)) / 1000000
                        i += 1
                else:
                    data["assets"][i] = {
                        "name": filename[0],
                        "path": "{0}/{1}".format(asset_path.replace("\\", "/"), filename[0])}
                    data["data"]["amount"] = + i
                    data["data"]["size"] += os.path.getsize(os.path.join(dir_path, file)) / 1000000
                    i += 1
    return data


def get_all_cooked_assets(path="./"):
    """Get a dictionary of assets, consist of their game paths and asset names, that have been cooked"""
    data = defaultdict(dict)
    data["data"]["size"] = 0
    i = 0
    if path:
        for dir_path, subdir_path, files in os.walk(path):
            if files:
                asset_path = dir_path.replace(path, "Game")
                for file in files:
                    data["assets"][i] = {"size": 0, "path": "", "name": ""}
                    if file.endswith(EXTENSIONS):
                        filename = file.split(".")
                        data["data"]["size"] += os.path.getsize(os.path.join(dir_path, file))
                        if file.endswith(".uasset"):
                            data["assets"][i]["name"] = filename[0]
                            data["assets"][i]["path"] = "/{0}/{1}".format(asset_path.replace("\\", "/"), filename[0])
                            data["assets"][i]["size"] += os.path.getsize(os.path.join(dir_path, file)) / 1000000
                            data["data"]["amount"] = + i
                            i += 1
        return data
    else:
        print("Path or package name is empty!")


# def search_by_word(path="", package_name="", search_by=""):
#     """Get a dictionary of assets, consist of their game paths and asset names, that have been searched by word"""
#     if path and package_name:
#         if search_by:
#             assets = defaultdict(list)
#             amount = 0
#             directory = os.path.join(path, package_name, "Game")
#             for dir_path, subdir_path, files in os.walk(directory):
#                 if files:
#                     for file in files:
#                         with open(os.path.join(dir_path, file)) as txt:
#                             for line in txt:
#                                 if search_by in line:
#                                     game_package = dir_path.replace(directory, ".")
#                                     filename = file.split(".")
#                                     assets[game_package].append(filename[0])
#                                     amount += 1
#                                     break
#             return assets, amount
#         else:
#             print("You need to enter search word!")
#     else:
#         print("Path or package name is empty!")
#
#
# def search_by_parent_material(path="", package_name="", search_by="Parent=Material"):
#     """Get a dictionary of assets, consist of their game paths and asset names, that have been searched by parent material"""
#     if path and package_name:
#         if search_by:
#             assets = defaultdict(list)
#             amount = 0
#             directory = os.path.join(path, package_name)
#             for dir_path, subdir_path, files in os.walk(os.path.join(directory, "Game")):
#                 if files:
#                     for file in files:
#                         with open(os.path.join(dir_path, file)) as txt:
#                             for line in txt:
#                                 if search_by in line:
#                                     parent_package = line.split("\"")
#                                     pack = parent_package[1].split(".")
#                                     instance_package = dir_path.replace(directory, "")
#                                     filename = file.split(".")
#                                     assets[pack[0]].append([filename[0], instance_package.replace("\\", "/")])
#                                     amount += 1
#                                     break
#
#
#             json_path = os.path.join("./", "NBA_jsons", str(datetime.date.today()))
#             os.makedirs(json_path, exist_ok=True)
#             with open(os.path.join(json_path, "InstanceMaterials.json"), "w") as out:
#                 json.dump({"assets": assets, "amount": amount}, out)
#             # return assets, amount
#         else:
#             print("You need to enter search word!")
#     else:
#         print("Path or package name is empty!")
#
#
# def xls_out(json_path="", parents={}):
#     with open(json_path) as js:
#         assets = json.load(js)
#     wb = xlsxwriter.Workbook("./NBA_xls/InstanceMeshes.xlsx")
#     ws = wb.add_worksheet("InstanceMeshes")
#     counter = 1
#     form = wb.add_format()
#     form.set_bg_color("#de8a8a")
#     for asset in parents:
#         if asset in assets["assets"]:
#             ws.write("A{0}".format(counter), asset, form)
#             for obj in assets["assets"][asset]:
#                 ws.write("B{0}".format(counter), "{0}/{1}".format(obj[1], obj[0]))
#                 counter += 1
#         else:
#             ws.write("A{0}".format(counter), asset, form)
#             counter += 1
#     wb.close()


if __name__ == '__main__':

#Для сбора размеров текстур персонажей
    # total_size = 0
    # with open("./NBA_jsons/list_of_textures_original.txt", "r") as dirs:
    #     for el in dirs:
    #         path = "{0}.{1}".format(el.replace("/Game/", "").strip(), "ubulk")
    #         path_match = os.path.join(BUILD_PATH, path)
    #         try:
    #             total_size += os.path.getsize(path_match)
    #             shutil.copyfile(path_match, "./NBA_pak/temp/{0}".format(os.path.basename(path_match)))
    #         except FileNotFoundError as msg:
    #             print(msg)
    #
    # print("Total Size: {0}Mb".format(total_size/1000000))

#Для сравнения списков материалов
    cooked_assets = get_all_cooked_assets(BUILD_PATH)
    source_materials_new = get_all_assets_ue4(SOURCE_PATH, "Materials")
    source_materials_old = get_all_assets_ue4(SOURCE_PATH, "Materials_07")

    list_of_cooked = [cooked_assets["assets"][id]["path"] for id in cooked_assets.get("assets", 0)]
    list_of_materials_new = [source_materials_new["assets"][id]["path"] for id in source_materials_new.get("assets", 0)]
    list_of_materials_old = [source_materials_old["assets"][id]["path"] for id in source_materials_old.get("assets", 0)]

    materials_coocked = set(list_of_materials_new).intersection(list_of_cooked)
    for el in materials_coocked:
        print(el)
    print(len(materials_coocked))

    # difference = set(list_of_materials_new).difference(list_of_materials_old)
    #
    # for el in difference:
    #     print(el)

    # result = []
    # with open("./NBA_jsons/temp_list.txt", "r") as temp:
    #     for el in temp:
    #         result.append(el.strip())
    #
    # res = set(materials_coocked).difference(result)
    # for el in res:
    #     print(el)