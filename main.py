import time 
import argparse
import random

import pymongo
from chance import chance

# Setup argparser stuff
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', action='help', help='show this help message and exit')
parser.add_argument("time", help="how long to run simulator in seconds", type=int)
parser.add_argument("-h", "--host", help="IP address of the mongoDB you want to connect to", default="localhost")
parser.add_argument("-p", "--port", help="port of the mongoDB you want to connect to", default=27017, type=int)

def generate_data(input_names):
    # Mandatory data
    output_data = {}
    output_data["first_name"] = chance.pickone(input_names)
    output_data["last_name"] = chance.last()
    output_data["age"] = chance.age()
    output_data["email"] = chance.email()
    
    optional_data = ["phone", "twitter", "country"]
    number_of_optional_data = random.randint(0, len(optional_data))
    for _ in range(number_of_optional_data):
        # Picks a random data to input
        random_index = random.randint(0, len(optional_data) - 1)
        random_choice = optional_data.pop(random_index)
        random_method = getattr(chance, random_choice)
        output_data[random_choice] = random_method()
    return output_data

    
# Delete a random entry with the same generated name
def delete_data(input_collection, input_data):
    random_name = input_data["first_name"]
    input_collection.delete_one({"first_name": random_name})

# Insert data
def insert_data(input_collection, input_data):
    input_collection.insert_one(input_data)

# Delete all data on database
def cleanup_database(input_collection):
    input_collection.delete_many({})

# Create a list of finite first names so we can query this
def initialise_data(number_of_names):
    output_name_array = []
    for _ in range(number_of_names):
        generated_name = chance.first()
        output_name_array.append(generated_name)
    return output_name_array

def connect_to_test_collection(host, port):
    client = pymongo.MongoClient(host, port)
    db = client["msimulator"]
    collection = db["test"]
    return collection

if __name__ == "__main__":
    # Get argument values
    args = parser.parse_args()
    input_run_time = args.time
    mongodb_ip_address = args.host
    mongodb_port = args.port

    collection = connect_to_test_collection(mongodb_ip_address, mongodb_port)
    first_name_array = initialise_data(100)

    initial_time = time.time()
    while True:
        scenarios = [insert_data, delete_data]
        chosen_scenario = chance.pickone(scenarios)
        data = generate_data(first_name_array)
        chosen_scenario(collection, data)

        # Calculate run time
        current_time = time.time()
        total_time = current_time - initial_time
        if (total_time > input_run_time):
            break

    cleanup_database(collection)



