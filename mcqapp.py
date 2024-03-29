import json
#from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
import streamlit as st
import traceback
import pandas as pd
from langchain.callbacks import get_openai_callback
from mcqutils import parse_file, get_table_data, RESPONSE_JSON
import os
#load_dotenv()

# This is an LLMChain to create 10-20 multiple choice questions from a given piece of text.
llm = OpenAI(api_key="yourapikey",model_name="gpt-3.5-turbo-16k", temperature=0, max_tokens=-1)

template = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to\
create a quiz of {number} multiple choice questions in {tone} tone.
Make sure that questions are not repeated and check all the questions to be conforming to the text as well.
Make sure to format your response like the RESPONSE_JSON below and use it as a guide.\
Ensure to make the {number} MCQs.
### RESPONSE_JSON
{response_json}
"""
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "tone", "response_json"],
    template=template,
)
quiz_chain = LLMChain(
    llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True
)

# This is an LLMChain to evaluate the multiple choice questions created by the above chain
llm = OpenAI(api_key="yourapikey",model_name="gpt-3.5-turbo", temperature=0)
template = """You are an expert english grammarian and writer. Given a multiple choice quiz\
You need to evaluate complexity of the questions and give a complete analysis of the quiz if the students 
will be able to understand the questions and answer them. Only use at max 50 words for complexity analysis.
If quiz is not at par with the cognitive and analytical abilities of the students,\
update the quiz questions which need to be changed and change the tone {tone}such that it perfectly fits the students abilities. 
Quiz MCQs:
{quiz}
Critique from an expert english writer of the above quiz:"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=[ "tone", "quiz"], template=template
)
review_chain = LLMChain(
    llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True
)

# This is the overall chain where we run these two chains in sequence.
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "tone",  "response_json"],
    # Here we return multiple variables
    output_variables=["quiz", "review"],
    verbose=True,
)

st.title("🦜⛓️ Langchain: MCQ Generation")

# Create a form using st.form
with st.form("user_inputs"):
    # File upload
    #uploaded_file = st.file_uploader("select a directory file")
    input_directory="/Users/rachana/Rachana_Python_VS/MCQ_Generator/system-design"

    # Input fields
    mcq_count = st.number_input("No of MCQs", min_value=3, max_value=20)
    #grade = st.number_input("Insert Grade", min_value=1, max_value=10)
    tone = st.text_input("Insert Complexity ", max_chars=100, placeholder="easy/medium /complex /very complex")
 
    button = st.form_submit_button("Create quiz")

# Check if the button is clicked and all fields have inputs
if button and input_directory is not None and mcq_count and tone :
    with st.spinner("Loading..."):
        try:
            for root, dirs, files in os.walk(input_directory):
                for file in files:
                    if file.endswith(".md"):
                        input_path = os.path.join(root, file)

                        # Process the .md file
                        text = parse_file(input_path)

                        # count tokens and cost of api call
                        with get_openai_callback() as cb:
                            response = generate_evaluate_chain(
                                {
                                    "text": text,
                                    "number": mcq_count,
                                    #"grade": grade,
                                    "tone": tone,
                                    "response_json": json.dumps(RESPONSE_JSON),
                                }
                            )
                        if isinstance(response, dict):
                            # Extract quiz data from the response
                            quiz = response.get("quiz", None)
                            if quiz is not None:
                                table_data = get_table_data(quiz)
                                if table_data is not None:
                                    df = pd.DataFrame(table_data)
                                    df.index = df.index + 1
                                    #st.table(df)
                                                            # with open('/Users/rachana/Rachana_Python_VS/MCQ_Generator/system-design/001-service-oriented-architecture/02-scenario-excercise.json', 'w', encoding='utf-8') as json_output:
                                                            #     json.dump(table_data, json_output, ensure_ascii=False, indent=2)
                                                            # Display the review in a text box
                                                            #st.text_area(label="Review", value=response["review"])
                                                            # Output path in the same directory with ".json" extension
                                    output_path = os.path.join(root, f"{os.path.splitext(file)[0]}.json")

                                    # Write the processed data to the output file
                                    with open(output_path, 'w', encoding='utf-8') as json_output:
                                        json.dump(table_data, json_output, ensure_ascii=False, indent=2)
                                else:
                                    st.error("Error in table data")
                        #else:
                            #st.write(response)

                        
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error")
        else:
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")

            