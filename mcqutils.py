import PyPDF2
import json
import traceback
import re
import numpy as np
import os
def parse_file(input_path):
    # if file.name.endswith(".pdf"):
    #     try:
    #         with open(file, 'r', encoding='utf-8') as file:
    #             content = file.read()

    #         # Use regex to find sentences
    #         sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', content)

    #         return sentences
            
    #     finally :
    #         raise Exception("Error reading the md file.")

    # if file.name.endswith(".md"):
    #     return file.read().decode("utf-8")
    if input_path !="":
        with open(input_path, 'r',encoding="utf-8") as file:
            return file.read()
    else:
        raise Exception(
            "Unsupported file format. Only .md files are supported."
        )

def process_directory(input_directory):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".md"):
                input_path = os.path.join(root, file)

                # Process the .md file
                processed_data = parse_file(input_path)

                # Output path in the same directory with ".json" extension
                output_path = os.path.join(root, f"{os.path.splitext(file)[0]}.json")

                # Write the processed data to the output file
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    json.dump(processed_data, output_file, ensure_ascii=False, indent=2)

def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        # Iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options =  {
                    f"{option}": f"{option_value}"
                    for option, option_value in value["options"].items()
                }
            
            dictionary = []
            # for i in range(len(value["options"].items())):
            #      dictionary[option[i]] = option_value[i]
                 
            # dic=[]
            # for option, option_value in value["options"].items():
            #     dic.append(option : option_value})

        
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False


RESPONSE_JSON = {
    "1": {
        "no": "1",
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "no": "2",
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "no": "3",
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}