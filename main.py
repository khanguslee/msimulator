import time 

import pymongo
from chance import chance

def connect_to_test_collection(host, port):
    client = pymongo.MongoClient(host, port)
    db = client["msimulator"]
    collection = db["test"]
    return collection

if __name__ == "__main__":
    input_run_time = 10
    collection = connect_to_test_collection("localhost", 27017)

    initial_time = time.time()
    while True:
        scenarios = ["insert", "delete", "update", "query"]
        chosen_scenario = chance.pickone(scenarios)
        print(chosen_scenario)
        # Calculate run time
        current_time = time.time()
        total_time = current_time - initial_time
        if (total_time > input_run_time):
            break



