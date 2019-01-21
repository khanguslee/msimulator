import multiprocessing
import time 
import argparse
import random

import pymongo
from chance import chance

import scenarios

# Setup argparser stuff
# TODO: --output To specify diagnostic.data output
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', action='help', help='show this help message and exit')
parser.add_argument("time", help="how long to run simulator in seconds", type=int)
parser.add_argument("-h", "--host", help="IP address of the mongoDB you want to connect to", default="localhost")
parser.add_argument("-p", "--port", help="port of the mongoDB you want to connect to", default=27017, type=int)
parser.add_argument("-m", "--minutes", help="change time to minutes", action="store_true")
parser.add_argument("-n", "--number", help="number of processes to spawn", default=1, type=int)


def sum_results(input_results_array):
    output_results = {}
    for result in input_results_array:
        for key,value in result.items():
            if key not in output_results:
                output_results[key] = value
            else:
                output_results[key] += value

    return output_results

def generate_data(input_names):
    # Mandatory data
    output_data = {}
    output_data["first_name"] = chance.pickone(input_names)
    output_data["last_name"] = chance.last()
    output_data["age"] = chance.age()
    output_data["email"] = chance.email()

    # Optional data
    optional_data = ["phone", "twitter", "country"]
    number_of_optional_data = random.randint(0, len(optional_data))
    for _ in range(number_of_optional_data):
        # Picks a random data to input
        random_index = random.randint(0, len(optional_data) - 1)
        random_choice = optional_data.pop(random_index)
        random_method = getattr(chance, random_choice)
        output_data[random_choice] = random_method()
    return output_data

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

def connect_to_test_collection(host, port, process_id):
    # TODO: Check if user already has this database and collection
    client = pymongo.MongoClient(host, port)
    db = client["msimulator"]
    collection = db["test-" + str(process_id)]
    return collection

def run(process_id, input_run_time, mongodb_ip_address, mongodb_port, queue):
    # Setup
    collection = connect_to_test_collection(mongodb_ip_address, mongodb_port, process_id)
    first_name_array = initialise_data(100)
    # Get all scenario functions
    test_scenarios = dir(scenarios)[9:]

    number_of_operations = {}
    initial_time = time.time()
    while True:
        chosen_scenario = chance.pickone(test_scenarios)
        # Increment count of number of times a scenario has been called
        if chosen_scenario not in number_of_operations:
            number_of_operations[chosen_scenario] = 1
        else:
            number_of_operations[chosen_scenario] += 1

        data = generate_data(first_name_array)
        scenario = getattr(scenarios, chosen_scenario)
        scenario(collection, data)

        # Calculate run time
        current_time = time.time()
        total_time = current_time - initial_time
        if (total_time > input_run_time):
            break
    cleanup_database(collection)

    # Store results
    queue.put(number_of_operations)

if __name__ == "__main__":
    # Get argument values
    args = parser.parse_args()
    input_run_time = args.time
    is_minutes = args.minutes

    if is_minutes:
        print("Running for " + str(input_run_time) + " minutes")
        input_run_time *= 60 
    else:
        print("Running for " + str(input_run_time) + " seconds")

    mongodb_ip_address = args.host
    mongodb_port = args.port

    processes = []
    queue = multiprocessing.Queue()
    number_of_processes = args.number
    for process_id in range(number_of_processes):
        process = multiprocessing.Process(target=run, args=(process_id,input_run_time, mongodb_ip_address,mongodb_port,queue,))
        processes.append(process)
        process.start()

    for proess in processes:
        process.join()

    results = [queue.get() for process in processes]
    results_sum = sum_results(results)
    print(results_sum)