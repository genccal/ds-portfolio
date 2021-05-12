import os
import json


def parse_to_json(file, out):
    """
    file: directory + filename to be parsed
    out: output directory
    """
    # open and read text
    f = open(file, "r")
    name = os.path.basename(f.name)
    contents = f.readlines()
    
    # parse the text into dict
    vehicle = dict()
    for line in contents:
        for part in line.split():
            key, value = part.split("=")
            vehicle[key] = value

    # dump json to directory 'parsed'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out + vehicle["id"] + ".json", "w") as outfile:
        json.dump(vehicle, outfile)


for file in os.listdir("logs"):
    parse_to_json("logs/" + file, "parsed/#")
    os.remove("logs/" + file)
print("Parsed 1000 files is done in ./parsed")
