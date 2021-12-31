import requests
import json
import time

mUrl = "discord webhook url"

poolurl = "signum pool url"


def getApiMiners():
    minersResponse = requests.get(poolurl + "/api/getMiners")
    minersList = json.loads(minersResponse.text).get("miners")

    apiMiners = []
    for entry in minersList:
        miner = {"address": entry.get("address"), "addressRS": entry.get("addressRS"), "name": entry.get("name")}
        apiMiners.append(miner)
    return apiMiners

def storeMiner(miners):
    jsonString = json.dumps(miners)
    jsonFile = open("miners.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def FileCheck(fn):
    try:
        open(fn, "r")
        return True
    except IOError:
        print("Error: File does not appear to exist.")
        return False


def getdbMiners():
    if FileCheck('miners.json'):
        with open('miners.json') as f:
            return json.load(f)
    else:
        newdb = []
        storeMiner(newdb)
        return newdb


# apiMiners comes from the api, dbMiners is what was store in the database
def findNewMiners(apiMiners, dbMiners):
    newMiner = []
    for apiMiner in apiMiners:
        apiMinerAddress = apiMiner.get("addressRS")
        if not any(dbMiner.get("addressRS") == apiMinerAddress for dbMiner in dbMiners):
            # new miner found
            newMiner.append(apiMiner)
    return newMiner


apiMiners = getApiMiners()
dbMiners = getdbMiners()

newMiners = findNewMiners(apiMiners, dbMiners)


if len(newMiners) > 0:
    newdbMiner = dbMiners
    for miner in newMiners:
        newdbMiner.append(miner)
        # do what you want for each new miner

        time.sleep(1)
        name = miner.get("name")
        address = miner.get("address")
        addressRS = miner.get("addressRS")
        print(name)
        print("address is " + address)
        if name == None:
            name = addressRS
        data = {
            "content": ":pick: " "New miner: [" + name + "](https://explorer.signum.network/address/" + address + ")" " has just been seen for the first time. Enjoy your stay!"
        }
        response = requests.post(mUrl, json=data)
        print(response.text)

    storeMiner(newdbMiner)


