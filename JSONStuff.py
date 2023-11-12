import json

filepath = "data.json"

def createIfNull():
    try:
        with open(filepath, 'r') as file:
            pass
    except FileNotFoundError:
        with open(filepath, 'w') as file:
            json.dump({}, file)

def save(username, date, data):
    createIfNull()

    # Read previous values
    with open(filepath, 'r') as file:
        existingData = json.load(file)

    # append new data
    existingData.setdefault(username, {})[date] = data

    # rewrite to json file
    with open(filepath, 'w') as file:
        json.dump(existingData, file)

def load(username, date):
    createIfNull()

    with open(filepath, 'r') as file:
        data = json.load(file)
        try: 
            litterVal = data[username][date]
            return litterVal
        except KeyError:
            return 0

def max_entry():
    createIfNull()

    with open(filepath, 'r') as file:
        data = json.load(file)
        max_score = 0
        max_entry_date = None
        max_score_user = ""

        for username, date_data in data.items():
            for date, score in date_data.items():
                if score > max_score:
                    max_score = score
                    max_entry_date = date
                    max_score_user = username

        return (max_score_user, max_score, max_entry_date)