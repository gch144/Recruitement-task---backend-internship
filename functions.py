import os
import csv
import re
import xml.etree.ElementTree as ET
import json
from collections import defaultdict
from datetime import datetime


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)


# Function to validate email based on criteria
def is_valid_email(email):
    # Email must contain only one "@" symbol.
    if email.count("@") != 1:
        return False
    # Split email into parts
    parts = email.split("@")
    # The part before "@" must be at least 1 character long.
    if len(parts[0]) < 1:
        return False
    # The part between "@" and "." must be at least 1 character long.
    if len(parts[1].split(".")[0]) < 1:
        return False
    # The part after the last "." must be between 1 and 4 characters long, containing only letters and/or digits.
    last_part = parts[1].split(".")[-1]
    if not (1 <= len(last_part) <= 4 and last_part.isalnum()):
        return False

    return True


def clean_and_store_telephone(telephone):
    cleaned_telephone = telephone[-9:]
    # print(cleaned_telephone)
    if len(cleaned_telephone) == 9:
        if cleaned_telephone.isdigit() and int(cleaned_telephone[0]) != 0:
            return cleaned_telephone
    return False


# Function to read and process CSV file
def process_csv(file_path, dataset):
    with open(file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for row in csv_reader:
            if is_valid_email(row["email"]) and clean_and_store_telephone(
                row["telephone_number"]
            ):
                # Clean and store telephone number
                row["telephone_number"] = clean_and_store_telephone(
                    row["telephone_number"]
                )

                row["created_at"] = datetime.strptime(
                    row["created_at"], "%Y-%m-%d %H:%M:%S"
                )

                children_str = row.get("children", "")
                if children_str:
                    children_list = [child.strip() for child in children_str.split(",")]
                    row["children"] = [
                        {
                            "name": extract_name_and_age(child)["name"],
                            "age": int(extract_name_and_age(child)["age"]),
                        }
                        for child in children_list
                    ]

                dataset.append(row)


def extract_name_and_age(name):
    match = re.search(r"^(.*?)\s*\((\d+)\)$", name)
    if match:
        return {"name": match.group(1).strip(), "age": match.group(2)}
    else:
        return {"name": name.strip(), "age": None}


# print(merged_dataset)


# Function to read and process XML file
def process_xml(file_path, dataset):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for user_elem in root.findall("user"):
        user_data = {
            "firstname": user_elem.find("firstname").text,
            "telephone_number": user_elem.find("telephone_number").text,
            "email": user_elem.find("email").text,
            "password": user_elem.find("password").text,
            "role": user_elem.find("role").text,
            "created_at": datetime.strptime(
                user_elem.find("created_at").text, "%Y-%m-%d %H:%M:%S"
            ),
            "children": [],
        }

        children_elem = user_elem.find("children")
        if children_elem is not None:
            for child_elem in children_elem.findall("child"):
                child_data = {
                    "name": child_elem.find("name").text,
                    "age": int(child_elem.find("age").text),
                }
                user_data["children"].append(child_data)

        email = user_data["email"]
        telephone = user_data["telephone_number"]
        if is_valid_email(email) and clean_and_store_telephone(telephone):
            # Clean and store telephone number
            user_data["telephone_number"] = clean_and_store_telephone(
                user_data["telephone_number"]
            )

            user_data["email"] = email
            dataset.append(user_data)


# print(merged_dataset)


# Function to process JSON file
def process_JSON(json_file_path, merged_dataset):
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    for user in data:
        email = user["email"]
        telephone = user["telephone_number"]

        if is_valid_email(email) and clean_and_store_telephone(telephone):
            # Convert child ages to integers
            children = user.get("children", [])
            for child in children:
                if "age" in child:
                    child["age"] = int(child["age"])

            entry = {
                "firstname": user["firstname"],
                "telephone_number": clean_and_store_telephone(user["telephone_number"]),
                "email": email,
                "password": user["password"],
                "role": user["role"],
                "created_at": datetime.strptime(
                    user["created_at"], "%Y-%m-%d %H:%M:%S"
                ),
                "children": children,
            }

            merged_dataset.append(entry)


def remove_duplicates(merged_dataset):
    unique_entries = defaultdict(dict)
    for entry in merged_dataset:
        entry_key = entry["telephone_number"] or entry["email"]
        existing_entry = unique_entries.get(entry_key)

        if not existing_entry or existing_entry["created_at"] < entry["created_at"]:
            unique_entries[entry_key] = entry

    unique_dataset = list(unique_entries.values())

    return unique_dataset


# Function to write dataset to a JSON file
def write_to_json(dataset, file_path):
    with open(file_path, "w") as json_file:
        json.dump(dataset, json_file, indent=2, cls=CustomEncoder)


# Function to import data recursively from folders
def import_data_recursive(root_folder, merged_dataset):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith((".json", ".xml", ".csv")):
                process_file(file_path, merged_dataset)


# Function to process a file based on its type
def process_file(file_path, merged_dataset):
    _, file_extension = os.path.splitext(file_path.lower())

    if file_extension == ".json":
        process_JSON(file_path, merged_dataset)
    elif file_extension == ".xml":
        process_xml(file_path, merged_dataset)
    elif file_extension == ".csv":
        process_csv(file_path, merged_dataset)
