import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_text(prompt):
    '''
    GPT API 요청 함수
    '''
    response = openai.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=10,
        stop=None,
        temperature=0.7,
    )
    return response.choices

def generate_question(data):
    responses = generate_text(data)
    question_list = []
    for response in responses:
        question = dict()
        for line in response.text.strip().split('\n'):
            if 'question' in line:
                question['question'] = line.split(':')[-1].replace(',', '').replace('"', '')
            elif 'answer' in line:
                question['answer'] = line.split(':')[-1].replace(',', '').replace('"', '')
            elif 'intent' in line:
                question['intent'] = line.split(':')[-1].replace(',', '').replace('"', '')
            elif 'difficulty' in line:
                question['difficulty'] = line.split(':')[-1].replace(',', '').replace('"', '')
        question_list.append(question)
    return question_list

def generate_score(data):
    responses = generate_text(data)
    score = responses[0].text.strip().replace('점', '').replace('.', '').replace(',', '')
    score = int(score)
    return score

def generate_total_score(data):
    responses = generate_text(data)
    response = responses[0].text.split('\n')
    for line in response:
        if 'score' in line:
            score = int(line.split(':')[-1].strip().replace('점', '').replace('.', '').replace(',', ''))
        elif 'complement' in line:
            complement = line.split(':')[-1].strip().replace('점', '').replace('.', '').replace(',', '')
    return score, complement