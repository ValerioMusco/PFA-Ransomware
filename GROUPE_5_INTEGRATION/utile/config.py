import json


def readConfig(file):

    directory = "../json/config." + file + ".json"
    with open(directory) as json_data:
        data_dict = json.load(json_data)

    data_str = json.dumps(data_dict, )

    return data_str
