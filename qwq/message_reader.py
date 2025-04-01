import ast
import csv
import json 
import re

message_file = ""
def get_message(message_file):
    """ Reads the message from a file """
    content = ""
    with open(message_file, "r") as file:
        csv_reader = list(csv.reader(file))
        # Skip the header row
        content = csv_reader[-1][-1]
        # print(content)
        
    print(content)
    swap_quotes = str.maketrans({"'": '"', '"': "'"})
    content_fixed = content.translate(swap_quotes)
    print(content_fixed)
    messages = json.loads(content_fixed)
    print(messages)
    return messages

if __name__ == "__main__":

    message = get_message("./ctflogs/Redeemer_10.csv")
    print(message)
    print(message[0]['content'])
    print(type(message))