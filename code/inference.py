## predict
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import json

def model_fn(model_dir):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForQuestionAnswering.from_pretrained(model_dir)
    
    return [model, tokenizer]


def input_fn(request_body, request_content_type):
#     print('[DEBUG] request_body:', type(request_body))
#     print('[DEBUG] request_content_type:', request_content_type)
    
    assert request_content_type=='application/json'
    data = json.loads(request_body)['inputs']
    questions = data['question']
    text = data['context']
    
    return [questions, text]


def predict_fn(input_object, model):
    trained_model = model[0]
    tokenizer = model[1]
    
    question = input_object[0]
    text = input_object[1]
    inputs = tokenizer(question, text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    outputs = trained_model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

        # Get the most likely beginning of answer with the argmax of the score
    answer_start = torch.argmax(answer_start_scores)
        # Get the most likely end of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1

    answer = tokenizer.convert_tokens_to_string(
            tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end])
        )

    return {'Question':question, 'answer':answer, 'Answer_start':int(answer_start)}

if __name__ == "__main__":
    data = {
    'inputs': {
        "question": "Who is the speaker?",
        "context": "We were halfway through our meal when Blair jumped up and did the potty dance, \"I really have to go! I'll meet you guys at the house.\"She starts running faster. "
    }
}
    sample = data['inputs']
    sample = [sample['question'],sample['context']]

    model = model_fn('model_save/cross_book/deepset-bert-base-cased-squad2_1961701_train')
    result = predict_fn(sample, model)
    print(result)
    
