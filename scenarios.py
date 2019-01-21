from chance import chance

# TODO: Have these functions inherit from a scenario class

def query_data(input_collection, input_data):
    """Query a random entry

    Arguments:
        input_collection {collection} -- mongoDB collection to connect to
        input_data {object} -- Random data to query with a first name
    """

    random_name = input_data["first_name"]
    input_collection.find({"first_name": random_name})

def range_query_data(input_collection, input_data):
    """Query a range of ages

    Arguments:
        input_collection {collection} -- mongoDB collection to connect to
        input_data {object} -- Random data to get a random age to query from
    """

    greater_than_query = {"age": {"$gt": input_data["age"]}}
    less_than_query = {"age": {"$lt": input_data["age"]}}
    # Query either greater than or less than a random age
    query = greater_than_query if chance.boolean() else less_than_query
    input_collection.find(query)

def delete_data(input_collection, input_data):
    """Delete a random entry with the same generated name

    Arguments:
        input_collection {collection} -- mongoDB collection to connect to
        input_data {object} -- Used to grab the first name to delete from the collection
    """

    random_name = input_data["first_name"]
    input_collection.delete_one({"first_name": random_name})

def insert_data(input_collection, input_data):
    """Insert input data into the specified collection

    Arguments:
        input_collection {collection} -- mongoDB collection to connect to
        input_data {object} -- Input data to insert into the mongoDB collection
    """

    input_collection.insert_one(input_data)

def update_data(input_collection, input_data):
    """Update age of a random entry

    Arguments:
        input_collection {collection} -- mongoDB collection to connect to
        input_data {object} -- Used to grab the first name specified to update
    """

    query = {"first_name": input_data["first_name"]}
    new_age = chance.age()
    new_values = {"$set": {"age": new_age}}
    input_collection.update_one(query, new_values)

def count_data(input_collection, input_data):
    """Ask for a count of the number of documents in the collection

    Arguments:
        input_collection {collection} -- mongoDB collection to connect to
        input_data {bbject} -- Not used
    """
    input_collection.count()
