import json
from jsonschema import validate
import jsonschema
import sys

def get_schema(filename):
    """This function loads the given schema available"""
    with open(filename, 'r') as file:
        schema = json.load(file)
    return schema

def get_jsondata(filename):
    """This function loads the given schema available"""
    with open(filename, 'r') as file:
        jsondata = json.load(file)
    return jsondata


def validate_json(schema_data,json_data):
    try:
        validate(instance=json_data, schema=schema_data)
    except jsonschema.exceptions.ValidationError as err:
        #print(err)
        #err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message


if __name__ == "__main__":
    if len(sys.argv)==3:
        jsonData = get_jsondata(sys.argv[1])
        schema = get_schema(sys.argv[2])
        is_valid, msg = validate_json(schema,jsonData)
        print(msg)
    else:
        print("python3 test_schema.py ./joe_schema.json ./examples/joe_example.json")
