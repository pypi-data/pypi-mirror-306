#!/usr/bin/env python
# *_* coding: utf-8 *_*

"""csv2ies"""

import os
import csv
import sys
import json
import string
import secrets
import smtplib

from email.message import EmailMessage

import requests


example_config = {
    "CSV": "accounts.csv",
    "CSV-DELIMITER": "\t",
    "IES-URL": "https://ies.middleearth.com",
    "X-IES-SESSION": "84111108107105101110",
    "ROOT-ANCHOR": "users.middleearth",
    "ZONE-TO-ANCHOR": {
        "Wizards": "users.abracadrabra",
        "Hobbits": "users.bagginses",
        "Elves": "users.pointyears",
    },
    "SEND-EMAIL": True,
    "EMAIL-OUT": "something@sitepark.de",
    "PASSWORD-LENGTH": 10,
}

import_fields = {
    "nutzername": "login",
    "login": "login",
    "vorname": "firstname",
    "name": "lastname",
    "nachname": "lastname",
    "email": "email",
    "e-mail": "email",
    "geschlecht": "gender",
    "anrede": "gender",
    "notiz": "note",
    # "gültigkeit": "validity",
    # "identitäten": "identityList",
    "rolle": "roleList",
    "bereich": "zones",
    "passwort": "password",
}

roles = {
    "redakteur": "USER",
    "nutzer": "USER",
    "admin": "ADMINISTRATOR",
    "gast": "EXTERNAL",
    "guest": "EXTERNAL",
    "extern": "EXTERNAL",
}


def send_mail_to_user(user, config):
    """Send the user an e-mail with his new login credentials.

    Keyword Arguments:
    user -- User object
    config -- Configuration dictionary"""
    headline = ["Hallo"]
    match user["gender"]:
        case "MALE":
            headline.append("Herr")
        case "FEMALE":
            headline.append("Frau")
        case _:
            headline.append(user["firstname"])
    headline.append(user["lastname"])
    headline = " ".join(headline) + ",\n\n"
    body = f"""Ihr Nutzerkonte wurde erstellt:

Nutzername: {user['login']}
Passwort: {user['password']['clearText']}

Sie können sich nun unter {config['IES-URL']} einloggen.

Mit freundlichen Grüßen
Ihr Sitepark Team"""
    message = EmailMessage()
    message.set_content(headline + body)
    message["Subject"] = "Ihr InfoSite Konto wurde erstellt!"
    message["From"] = config["EMAIL-OUT"]
    message["To"] = user["email"]

    smtp_server = smtplib.SMTP("localhost:25")
    smtp_server.send_message(message)
    smtp_server.quit()


def generate_secure_password(length):
    """Generate a secure password

    Keyword Arguments:
    length -- Password's target length"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password


def write_users_to_ies(config):
    """Connects to IES Rest API and creates/updates user records

    Keyword Arguments:
    config -- Configuration dictionary"""
    url = config["IES-URL"] + "/api/rest/v1/users"
    header = {"X-IES-SESSION": config["X-IES-SESSION"]}
    users = config["USERS"]
    for user in users:
        check = requests.get(url=url + f'/{user["anchor"]}', headers=header)
        if check.ok:
            stored = json.loads(check.content.decode())
            stored_s = dict(stored)
            del stored_s["id"]
            del stored_s["validity"]
            user_s = dict(user)
            if "password" in user_s.keys():
                del user_s["password"]
            stored_s["roleList"] = set(stored_s["roleList"])
            user_s["roleList"] = set(user_s["roleList"])
            same_data = stored_s == user_s
            if same_data:
                print(f'Account already up to date for user {user["login"]}')
            else:
                print(f'Data needs an update for user {user["login"]}')
                update_user(config, stored_s, user_s)
        else:
            print(f'Importing new account for : {user["login"]}')
            response = requests.post(url=url, json=user, headers=header)
            if not response.ok:
                print(response.content.decode())
            else:
                print(
                    f"Added user {user['login']} with password {user['password']['clearText']}"
                )
                if config["SEND-EMAIL"]:
                    send_mail_to_user(user, config)


def update_user(config, user_old, user_new):
    """Compares saved records to imported records and updates records in case of changes

    Keyword Arguments:
    config -- Configuration dictionary
    user_old -- The saved data fetched from IES REST API
    user_new -- The data imported from the csv file"""
    user_old["roleList"] = sorted(list(user_old["roleList"]))
    user_new["roleList"] = sorted(list(user_new["roleList"]))
    for key in user_new.keys():
        if user_new[key] != user_old[key]:
            url = config["IES-URL"] + "/api/rest/v1/users/" + user_old["anchor"]
            header = {
                "X-IES-SESSION": config["X-IES-SESSION"],
                "Content-Type": "application/json-patch+json",
            }
            json_patch = [{"op": "replace", "path": "/" + key, "value": user_new[key]}]
            response = requests.patch(url, json=json_patch, headers=header)
            if response.ok:
                print(f"Updated {key} for user {user_old['login']}...")


def get_csv_schema(filepath, delimiter=","):
    """Reads csv file and build schema from the first line

    Keyword Arguments:
    filepath -- Path to csv file
    delimiter -- Character that separates fields inside a row"""
    with open(filepath, "r", encoding="utf-8", newline="") as csvfile:
        data = csv.reader(csvfile, delimiter=delimiter, quotechar="|")
        head = next(data)
    schema = []
    for f in head:
        if f.lower() in import_fields.keys():
            schema.append(import_fields[f.lower()])
        elif f.lower() in import_fields.values():
            schema.append(f.lower())
        else:
            print(f"Found unknown column name: {f}")
            print(
                f"Known case-insensitive values are: {', '.join(import_fields.keys())}"
            )
            print("Please adjust the column name and try again.")
            return None
    if len(schema) != len(set(schema)):
        print("Your columns are not uniquely named.")
    return schema


def import_users_from_csv(config):
    """Building user objects from csv table data

    Keyword Arguments:
    config -- Configuration dictionary"""
    if not os.path.exists(config["CSV"]):
        print(f'Could not find file "{config["CSV"]}". Please check your config.')
        sys.exit()
    with open(config["CSV"], "r", encoding="utf-8", newline="") as csvfile:
        schema = config["SCHEMA"]
        user_data = []
        user_reader = csv.reader(
            csvfile, delimiter=config["CSV-DELIMITER"], quotechar="|"
        )
        for i, row in enumerate(user_reader):
            if i != 0:
                user = {"roleList": [f'REF({config["ROOT-ANCHOR"]})']}
                for i in range(len(schema)):
                    if schema[i] == "zones":
                        zones = row[i].split(";")
                        while "" in zones:
                            zones.remove("")
                        for zone in zones:
                            zone = zone.strip()
                            if zone in config["ZONE-TO-ANCHOR"]:
                                user["roleList"].append(
                                    f'REF({config["ZONE-TO-ANCHOR"][zone]})'
                                )
                            else:
                                print(f"Found unknown Zone: {zone}")
                                print(
                                    f'Please add this zone to your config.json ZONE-TO-ANCHOR and point to its anchor (i.e. "{zone}":"some.pool.anchor")'
                                )
                    elif schema[i] == "roleList":
                        role = row[i].lower().strip()
                        if role in roles.keys():
                            user["roleList"].insert(0, roles[role])
                        elif role.upper() in roles.values():
                            user["roleList"].insert(0, role.upper())
                        else:
                            print(f"Found unknown role: {role}")
                            sys.exit()
                    elif schema[i] == "gender":
                        if row[i].lower().strip().startswith("h"):
                            user["gender"] = "MALE"
                        elif row[i].lower().strip().startswith("m"):
                            user["gender"] = "MALE"
                        elif row[i].lower().strip().startswith("f"):
                            user["gender"] = "FEMALE"
                        elif row[i].lower().strip().startswith("w"):
                            user["gender"] = "FEMALE"
                        elif row[i].lower().strip().startswith("d"):
                            user["gender"] = "DIVERSE"
                        elif row[i].lower().strip().startswith("n"):
                            user["gender"] = "DIVERSE"
                    elif schema[i] == "password":
                        user["password"] = {}
                        user["password"]["clearText"] = row[i].strip()
                    else:
                        user[schema[i]] = row[i].strip()
                        if schema[i] == "login":
                            user["anchor"] = "usr." + row[i].lower().strip()
                if "gender" not in user.keys():
                    user["gender"] = "UNKNOWN"
                if "password" not in user.keys():
                    user["password"] = {}
                    user["password"]["clearText"] = generate_secure_password(
                        config["PASSWORD-LENGTH"]
                    )
                user_data.append(user)
    return user_data


def create_config():
    """If no config.json is present, it will create an example file"""
    if not os.path.exists("config.json"):
        print(
            "Creating sample config.json file. After adjusting the config use `csv2ies run` to start the import."
        )
        with open("config.json", "w", encoding="utf-8") as config_file:
            json.dump(example_config, config_file, indent=4)
    else:
        print(
            "You already created a config.json, please delete it if you want to start with the default template."
        )
        sys.exit()


def main():
    """Entry point of csv2ies"""
    if len(sys.argv) == 2:
        if sys.argv[1] == "config":
            create_config()
            sys.exit()
        if sys.argv[1] == "run":
            if not os.path.exists("config.json"):
                print(
                    'Could not find "config.json" file. Run "csv2ies config" to create an example config. '
                )
                sys.exit()
            with open("config.json", "r", encoding="utf-8") as config_file:
                config = json.load(config_file)
                config["SCHEMA"] = get_csv_schema(
                    config["CSV"], config.get("CSV-DELIMITER", ",")
                )
            if config["SCHEMA"]:
                config["USERS"] = import_users_from_csv(config)
            else:
                sys.exit()
            print(
                f"This will import/update the following users into {config['IES-URL']}:"
            )
            for user in config["USERS"]:
                print(
                    user["anchor"],
                    user["firstname"],
                    user["lastname"],
                    user["email"],
                    user["login"],
                    user["password"]["clearText"],
                    sep=" | ",
                )
            user_answer = input("Do you want to continue? [y/N]")
            if user_answer.lower().startswith("y"):
                write_users_to_ies(config)
                print("Operation finished.")
            else:
                print("Aborted.")
            sys.exit()
    print("csv2ies expects to get exactly one of the following arguments: config, run")


if __name__ == "__main__":
    main()
