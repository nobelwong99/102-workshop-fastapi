from typing import Union
from fastapi import FastAPI
import json
import os

DATA_FILE = "db.json"

app = FastAPI()


# Load tasks from JSON file
def load_data_from_json():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"Error reading data from JSON file: {e}")
        return []


# Save tasks to JSON file
def save_data_to_json(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")


@app.get("/")
def read_root():
    return {"Hello": "World"}
