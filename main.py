import json, os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from src.utils import (
    generate_quiz_from_pdf,
    RESPONSE_JSON,
    doc,
    first_template,
    second_template
)

# Load environment variables
load_dotenv()

# Initialize LangChain ChatOpenAI instance
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

# Define prompt templates
quiz_generation_prompt = PromptTemplate(
    input_variables=["vocab_handout", "number", "response_json"],
    template=first_template,
    )

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["quiz"], 
    template=second_template,
    )

# Define chains
quiz_chain = LLMChain(
    llm=llm, 
    prompt=quiz_generation_prompt, 
    output_key="quiz", 
    verbose=True,
    )

review_chain = LLMChain(
    llm=llm, 
    prompt=quiz_evaluation_prompt, 
    output_key="review", 
    verbose=True,
    )

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["vocab_handout", "number", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True,
    )


# Iterate over PDF files and generate quiz questions
for filename in os.listdir('pdf_files'):
    file = os.path.join('pdf_files', filename)
    # checking if it is a file
    if os.path.isfile(file):
        generate_quiz_from_pdf(file, "", 10, json.dumps(RESPONSE_JSON), generate_evaluate_chain)


# Save the Word document
doc.save('Science_Practice_Questions.docx')
