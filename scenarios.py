from chance import chance

# TODO: Have these functions inherit from a scenario class

# Query a random entry
def query_data(input_collection, input_data):
    random_name = input_data["first_name"]
    input_collection.find({"first_name": random_name})

# Query a range of ages
def range_query_data(input_collection, input_data):
    greater_than_query = {"age": {"$gt": input_data["age"]}}
    less_than_query = {"age": {"$lt": input_data["age"]}}
    # Query either greater than or less than a random age
    query = greater_than_query if chance.boolean() else less_than_query
    input_collection.find(query)

# Delete a random entry with the same generated name
def delete_data(input_collection, input_data):
    random_name = input_data["first_name"]
    input_collection.delete_one({"first_name": random_name})

# Insert data
def insert_data(input_collection, input_data):
    input_collection.insert_one(input_data)

# Update age of a random entry
def update_data(input_collection, input_data):
    query = {"first_name": input_data["first_name"]}
    new_age = chance.age()
    new_values = {"$set": {"age": new_age}}
    input_collection.update_one(query, new_values)

# Ask for a count of collections
def count_data(input_collection, input_data):
    input_collection.count()