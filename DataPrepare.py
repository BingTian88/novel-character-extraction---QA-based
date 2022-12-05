import json
import os
import argparse

# def get_csv(data_path, out_path):
#     f = open(data_path) 
 
#     lines = f.readlines()
#     content_list = []
#     for line in lines:
#         content_list.append(json.loads(line))

#     df_train_toy = pd.DataFrame(content_list)
#     df_train_toy.to_csv(out_path, index=False,encoding='utf-8')
    
#     return df_train_toy

# import json
# ## modify the raw SQuAD json data to the model friendly format
# Inputdata = open("SQuAD_data/train-v1.1.json") #train-v1.1.json
# Inputdata = json.load(Inputdata)

# output_data = []
# for article in Inputdata['data']:
#     for p in article['paragraphs']:
#         for qas in p['qas']:
#             answers = {
#                 "text": [],
#                 "answer_start": []
#             }
#             for ans in qas['answers']:
#                 answers['text'].append(ans['text'])
#                 answers['answer_start'].append(ans['answer_start'])

#             output_data.append({
#                 "id": qas['id'],
#                 "context": p['context'],
#                 "question": qas['question'],
#                 "answers": answers
#             })
# data_dic = {}
# data_dic['data'] = output_data
# with open('SQuAD_data/data_new.json', 'w') as fp:
#     json.dump(data_dic, fp)


# def data_look(data_path):
#     f = open(data_path)
#     examples = f.readlines()
#     data = []
#     for exam in examples:  
#         ex = json.loads(exam)
#         ex['label'] = [ent for ent in ex['label']  if ent[-1] not in emotion]
#         data.append(ex)
#     return data


emotion = ['General', 'Whispering', 'Loudly', 'Surprise', 'Happy', 'Love/Hopeful', 'Angry', 'Disgust', 'Sad', 'Fear', 'ridicule']

def split_by_paragraph(txt_content):
    # input: txt
    # return: split by \n\n, then start, end position
    txt_ls = txt_content.split('\n\n') #split by paragraph
    start_str = 0
    start_ls = []
    end_ls = []
    for i in range(len(txt_ls)):
        start_ls.append(start_str)
        end = start_str+len(txt_ls[i])
        end_ls.append(end)
        start_str = end+2
    return txt_ls, start_ls, end_ls

def split_by_sentence(txt_content, start = 0):
    # input: txt
    # return: split by \n, then start, end position
    txt_ls = txt_content.split('\n') #split by paragraph
    start_str = start
    start_ls = []
    end_ls = []
    for i in range(len(txt_ls)):
        start_ls.append(start_str)
        end = start_str+len(txt_ls[i])
        end_ls.append(end)
        start_str = end+1
    return txt_ls, start_ls, end_ls

def split_by_paragraph_sentence(txt_content): #先按照\n\n 分割，再\n
    txt_ls, start_ls, end_ls = split_by_paragraph(txt_content)
    txt_res, start_res, end_res = [],[],[]
    for idx, text in enumerate(txt_ls):
        text_, text_s, text_e = split_by_sentence(text, start = start_ls[idx])
        txt_res.append(text_)
        start_res.append(text_s)
        end_res.append(text_e)
    txt_res = extend_all_part(txt_res)
    start_res = extend_all_part(start_res)
    end_res = extend_all_part(end_res)
    return txt_res, start_res, end_res  
    
    
# each segment contains 3 sentences
def merge_sentence_to_segment(txt_ls, start_ls, end_ls):
    txt_seg = []
    start_seg = []
    end_seg = []
    for i in range(len(txt_ls)-2):
        start_seg.append(start_ls[i])
        end_seg.append(end_ls[i+2])
        #确定原始分割符是\n 还是\n\n
        seg = txt_ls[i] + '\n' + txt_ls[i + 1] if (start_ls[i+1] - end_ls[i] == 1) else txt_ls[i] + '\n\n' + txt_ls[i + 1]
        seg = seg + '\n' + txt_ls[i + 2] if (start_ls[i+2] - end_ls[i+1] == 1) else seg + '\n\n' + txt_ls[i + 2]
        #seg = '\n'.join([x for x in txt_ls[i:i+3]])
        txt_seg.append(seg)
    return txt_seg, start_seg, end_seg

# each segment contains 5 sentences
def merge_5_sentence_to_segment(txt_ls, start_ls, end_ls):
    txt_seg = []
    start_seg = []
    end_seg = []
    for i in range(len(txt_ls)-4):
        start_seg.append(start_ls[i])
        end_seg.append(end_ls[i+4])
        #确定原始分割符是\n 还是\n\n
        seg = txt_ls[i] + '\n' + txt_ls[i + 1] if (start_ls[i+1] - end_ls[i] == 1) else txt_ls[i] + '\n\n' + txt_ls[i + 1]
        seg = seg + '\n' + txt_ls[i + 2] if (start_ls[i+2] - end_ls[i+1] == 1) else seg + '\n\n' + txt_ls[i + 2]

        seg = seg + '\n' + txt_ls[i + 3] if (start_ls[i+3] - end_ls[i+2] == 1) else seg + '\n\n' + txt_ls[i + 3]
        seg = seg + '\n' + txt_ls[i + 4] if (start_ls[i+4] - end_ls[i+3] == 1) else seg + '\n\n' + txt_ls[i + 4]
        #seg = '\n'.join([x for x in txt_ls[i:i+3]])
        txt_seg.append(seg)
    return txt_seg, start_seg, end_seg

# each segment contains 7 sentences
def merge_7_sentence_to_segment(txt_ls, start_ls, end_ls):
    txt_seg = []
    start_seg = []
    end_seg = []
    for i in range(len(txt_ls)-6):
        start_seg.append(start_ls[i])
        end_seg.append(end_ls[i+6])
        #确定原始分割符是\n 还是\n\n
        seg = txt_ls[i] + '\n' + txt_ls[i + 1] if (start_ls[i+1] - end_ls[i] == 1) else txt_ls[i] + '\n\n' + txt_ls[i + 1]
        seg = seg + '\n' + txt_ls[i + 2] if (start_ls[i+2] - end_ls[i+1] == 1) else seg + '\n\n' + txt_ls[i + 2]

        seg = seg + '\n' + txt_ls[i + 3] if (start_ls[i+3] - end_ls[i+2] == 1) else seg + '\n\n' + txt_ls[i + 3]
        seg = seg + '\n' + txt_ls[i + 4] if (start_ls[i+4] - end_ls[i+3] == 1) else seg + '\n\n' + txt_ls[i + 4]
        
        seg = seg + '\n' + txt_ls[i + 5] if (start_ls[i+5] - end_ls[i+4] == 1) else seg + '\n\n' + txt_ls[i + 5]
        seg = seg + '\n' + txt_ls[i + 6] if (start_ls[i+6] - end_ls[i+5] == 1) else seg + '\n\n' + txt_ls[i + 6]
        #seg = '\n'.join([x for x in txt_ls[i:i+3]])
        txt_seg.append(seg)
    return txt_seg, start_seg, end_seg

# each segment contains 10 sentences
def merge_10_sentence_to_segment(txt_ls, start_ls, end_ls):
    txt_seg = []
    start_seg = []
    end_seg = []
    for i in range(len(txt_ls)-9):
        start_seg.append(start_ls[i])
        end_seg.append(end_ls[i+9])
        #确定原始分割符是\n 还是\n\n
        seg = txt_ls[i] + '\n' + txt_ls[i + 1] if (start_ls[i+1] - end_ls[i] == 1) else txt_ls[i] + '\n\n' + txt_ls[i + 1]
        seg = seg + '\n' + txt_ls[i + 2] if (start_ls[i+2] - end_ls[i+1] == 1) else seg + '\n\n' + txt_ls[i + 2]

        seg = seg + '\n' + txt_ls[i + 3] if (start_ls[i+3] - end_ls[i+2] == 1) else seg + '\n\n' + txt_ls[i + 3]
        seg = seg + '\n' + txt_ls[i + 4] if (start_ls[i+4] - end_ls[i+3] == 1) else seg + '\n\n' + txt_ls[i + 4]
        
        seg = seg + '\n' + txt_ls[i + 5] if (start_ls[i+5] - end_ls[i+4] == 1) else seg + '\n\n' + txt_ls[i + 5]
        seg = seg + '\n' + txt_ls[i + 6] if (start_ls[i+6] - end_ls[i+5] == 1) else seg + '\n\n' + txt_ls[i + 6]
        
        seg = seg + '\n' + txt_ls[i + 7] if (start_ls[i+7] - end_ls[i+6] == 1) else seg + '\n\n' + txt_ls[i + 7]
        seg = seg + '\n' + txt_ls[i + 8] if (start_ls[i+8] - end_ls[i+7] == 1) else seg + '\n\n' + txt_ls[i + 8]
        seg = seg + '\n' + txt_ls[i + 9] if (start_ls[i+9] - end_ls[i+8] == 1) else seg + '\n\n' + txt_ls[i + 9]
        #seg = '\n'.join([x for x in txt_ls[i:i+3]])
        txt_seg.append(seg)
    return txt_seg, start_seg, end_seg

# each segment contains 13 sentences
def merge_13_sentence_to_segment(txt_ls, start_ls, end_ls):
    txt_seg = []
    start_seg = []
    end_seg = []
    for i in range(len(txt_ls)-12):
        start_seg.append(start_ls[i])
        end_seg.append(end_ls[i+12])
        #确定原始分割符是\n 还是\n\n
        seg = txt_ls[i] + '\n' + txt_ls[i + 1] if (start_ls[i+1] - end_ls[i] == 1) else txt_ls[i] + '\n\n' + txt_ls[i + 1]
        seg = seg + '\n' + txt_ls[i + 2] if (start_ls[i+2] - end_ls[i+1] == 1) else seg + '\n\n' + txt_ls[i + 2]

        seg = seg + '\n' + txt_ls[i + 3] if (start_ls[i+3] - end_ls[i+2] == 1) else seg + '\n\n' + txt_ls[i + 3]
        seg = seg + '\n' + txt_ls[i + 4] if (start_ls[i+4] - end_ls[i+3] == 1) else seg + '\n\n' + txt_ls[i + 4]
        
        seg = seg + '\n' + txt_ls[i + 5] if (start_ls[i+5] - end_ls[i+4] == 1) else seg + '\n\n' + txt_ls[i + 5]
        seg = seg + '\n' + txt_ls[i + 6] if (start_ls[i+6] - end_ls[i+5] == 1) else seg + '\n\n' + txt_ls[i + 6]
        
        seg = seg + '\n' + txt_ls[i + 7] if (start_ls[i+7] - end_ls[i+6] == 1) else seg + '\n\n' + txt_ls[i + 7]
        seg = seg + '\n' + txt_ls[i + 8] if (start_ls[i+8] - end_ls[i+7] == 1) else seg + '\n\n' + txt_ls[i + 8]
        seg = seg + '\n' + txt_ls[i + 9] if (start_ls[i+9] - end_ls[i+8] == 1) else seg + '\n\n' + txt_ls[i + 9]
        
        seg = seg + '\n' + txt_ls[i + 10] if (start_ls[i+10] - end_ls[i+9] == 1) else seg + '\n\n' + txt_ls[i + 10]
        seg = seg + '\n' + txt_ls[i + 11] if (start_ls[i+11] - end_ls[i+10] == 1) else seg + '\n\n' + txt_ls[i + 11]
        seg = seg + '\n' + txt_ls[i + 12] if (start_ls[i+12] - end_ls[i+11] == 1) else seg + '\n\n' + txt_ls[i + 12]
        #seg = '\n'.join([x for x in txt_ls[i:i+3]])
        txt_seg.append(seg)
    return txt_seg, start_seg, end_seg

def isPairStr(a, b):
    if len(a)>len(b) and a[:-2] ==b:
        return True
    if len(a) < len(b) and b[:-2] ==a:
        return True
    return False

def get_merge_label_list(label):
    res_label = []
    idx = 0
    while(idx < len(label) -1):
        if(isPairStr(label[idx][-1], label[idx+1][-1])):
            res_label.append((label[idx], label[idx+1]))
            idx+=2
        else:
            idx+=1
    return res_label


def judge_in_sentence(txt_seg, start_seg, end_seg, label_ls):
    res_label = [[] for j in range(len(txt_seg))]
    
    for i in range(len(txt_seg)):
        #print ("<<< i", i )
        cnt = 0
        for j in range(len(label_ls)):
            role_name = label_ls[j][1][-1] if label_ls[j][0][-1].endswith('_P') else label_ls[j][0][-1]
            role_start_offset = label_ls[j][0][0] if label_ls[j][0][-1].endswith('_P') else label_ls[j][1][0]
            role_end_offset = label_ls[j][0][1] if label_ls[j][0][-1].endswith('_P') else label_ls[j][1][1]
            
            conversation_start_offset = label_ls[j][1][0] if label_ls[j][0][-1].endswith('_P') else label_ls[j][0][0]
            conversation_end_offset = label_ls[j][1][1] if label_ls[j][0][-1].endswith('_P') else label_ls[j][0][1]
            # 判断 role_name 和 conversation 都在 txt_seg里
            if role_start_offset >=start_seg[i] and role_end_offset <=end_seg[i]:
                if conversation_start_offset >=start_seg[i] and conversation_end_offset <=end_seg[i]:
                    if(cnt == 0):
                        question_1 = "Find the conversation sentence."
                        question_2 = "Who said the conversation sentence?"
                        cnt +=1
                    else:
                        question_1 = "Find another conversation sentence."
                        question_2 = "Who said another conversation sentence?"
                    res_label[i].append({'role':role_name,
                                    'role_start_offset': role_start_offset - start_seg[i],
                                    'role_end_offset': role_end_offset - start_seg[i],
                                    'conversation_start_offset':conversation_start_offset - start_seg[i],
                                    'conversation_end_offset': conversation_end_offset - start_seg[i],
                                 'role_label':txt_seg[i][(role_start_offset - start_seg[i]):(role_end_offset - start_seg[i])],
                                'conversation_label':txt_seg[i][(conversation_start_offset - start_seg[i]):(conversation_end_offset - start_seg[i])],
                                        'question_1': question_1,
                                        'question_2': question_2})
                    
                        
    return res_label


def center_in_sentence(txt_seg, start_seg, end_seg, label_ls):
    samples = []
    flag = " center: "
    for i in range(len(txt_seg)):
        for j in range(len(label_ls)):
            label_dic = {}
            dict_res = {}
            
            role_name = label_ls[j][1][-1] if label_ls[j][0][-1].endswith('_P') else label_ls[j][0][-1]
            start_offset = label_ls[j][0][0] if label_ls[j][0][-1].endswith('_P') else label_ls[j][1][0]
            end_offset = label_ls[j][0][1] if label_ls[j][0][-1].endswith('_P') else label_ls[j][1][1]
            
            sentence_start = label_ls[j][1][0] if label_ls[j][0][-1].endswith('_P') else label_ls[j][0][0]
            
            # 判断 label 和 conversation 都在 txt_seg里
            
            if label_ls[j][0][0]>=start_seg[i] and label_ls[j][0][1]<=end_seg[i]:
                if label_ls[j][1][0]>=start_seg[i] and label_ls[j][1][1]<=end_seg[i]:
                    
                    sentence_start_inner = sentence_start - start_seg[i] 
                    sample_context = txt_seg[i][0:sentence_start_inner] + flag + txt_seg[i][sentence_start_inner:-1]
                    label_dic['text'] = [txt_seg[i][(start_offset - start_seg[i]):(end_offset - start_seg[i])]]
                    label_dic['answer_start'] = [start_offset - start_seg[i] if start_offset < sentence_start else start_offset - start_seg[i] + len(flag)]
                
                    dict_res = {'context': sample_context,
                            'question': 'Who said the center sentence?',
                            'answers': label_dic
                            }
                    samples.append(dict_res)
             
    return samples

def get_json(data_path, out_path):
    res_dic = {}
    f = open(data_path) 
    lines = f.readlines()
    content_list = []
    for line in lines:
        content_list.append(json.loads(line))
    res_dic['data'] =  content_list
    with open(out_path, 'w') as fp:
        json.dump(res_dic, fp)
        
def get_answers_label(res_item):
    res_dic = {'questions':[], 'answers':{}}
    res_dic['questions'] = [res_item['question_1'], res_item['question_2']]
    res_dic['answers']['input_text'] = [res_item['conversation_label'], res_item['role_label']]
    res_dic['answers']['answer_start'] = [res_item['conversation_start_offset'], res_item['role_start_offset']]
    res_dic['answers']['answer_end'] = [res_item['conversation_end_offset'], res_item['role_end_offset']]

    return res_dic

def write_back(raw_examples):
    res = []
    for i in range(len(raw_examples)):
        x1 = json.loads(raw_examples[i])
        txt_ls, start_ls, end_ls = split_by_paragraph_sentence(x1 ['text'])
        txt_seg, start_seg, end_seg = merge_sentence_to_segment(txt_ls, start_ls, end_ls)
        label_ls = [ent for ent in x1['label'] if ent[-1] not in emotion]
        label_ls = get_merge_label_list(label_ls)
        
        res_label = judge_in_sentence(txt_seg, start_seg, end_seg, label_ls)
        for j in range(len(txt_seg)):
            #only save content length larger than 10
            #only save the texts that have labels
            if len(txt_seg[j])>10 and len(res_label[j])>0:
                for res_label_item in res_label[j]:
                    label_dic = get_answers_label(res_label_item)
                    dict_res = {'context': txt_seg[j],
                                'question': label_dic['questions'],
                                'answers': label_dic['answers']
                                }
                    res.append(dict_res)
                    
        for idx, item in enumerate(res):
            item['id'] = str(idx)
    return res


def extend_all_part(part_content):
    all_content = []
    for part in part_content:
        all_content.extend(part)
    return all_content


def save_single_file(SampleMode, CenterFlag, input_path, output_folder):
    with open(input_path, "r", encoding="utf-8") as f:
        raw_examples = f.readlines()
        
    if CenterFlag == 1:
        samples = []
        for i in range(len(raw_examples)):
            data = json.loads(raw_examples[i])
            txt_ls, start_ls, end_ls = split_by_paragraph_sentence(data['text'])
            if SampleMode == 'short':
                txt_seg, start_seg, end_seg = txt_ls, start_ls, end_ls
            if SampleMode == 'long_3':
                txt_seg, start_seg, end_seg = merge_sentence_to_segment(txt_ls, start_ls, end_ls)
            if SampleMode == 'long_5':
                txt_seg, start_seg, end_seg = merge_5_sentence_to_segment(txt_ls, start_ls, end_ls)
            if SampleMode == 'long_7':
                txt_seg, start_seg, end_seg = merge_7_sentence_to_segment(txt_ls, start_ls, end_ls)
            if SampleMode == 'long_10':
                txt_seg, start_seg, end_seg = merge_10_sentence_to_segment(txt_ls, start_ls, end_ls)
            if SampleMode == 'long_13':
                txt_seg, start_seg, end_seg = merge_13_sentence_to_segment(txt_ls, start_ls, end_ls)
            label_ls = [ent for ent in data['label']  if ent[-1] not in emotion]
            label_ls = get_merge_label_list(label_ls)
            samples.append(center_in_sentence(txt_seg, start_seg, end_seg, label_ls))
        res = extend_all_part(samples)
        for idx, sample in enumerate(res):
            sample['id'] = str(idx)
    else:
        res = write_back(raw_examples)
        
    res_dic = {}
    res_dic['data'] =  res        
    with open(os.path.join(output_folder, input_path.split('/')[-1].split('.')[-2])+'.json', 'w', encoding="utf-8") as fp:
            json.dump(res_dic, fp)        
            
            
def main(SampleMode, CenterFlag, mode, input_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if mode=='single_file':
        save_single_file(SampleMode, CenterFlag, input_path, output_folder)
    elif mode=='folder':
        files = os.listdir(input_path)
        for i in files:
            if i!='.ipynb_checkpoints':
                save_single_file(SampleMode, CenterFlag, os.path.join(input_path,i), output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Training pipeline')
    parser.add_argument('--CenterFlag', type=int, default=0, help="have center flag in samples or not")
    parser.add_argument('--SampleMode', type=str, default='short', help="Samples with more sentences, other choices contain 'long_5' , 'long_7' and 'long_10'")
    parser.add_argument('--mode', type=str, default='single_file',
                        help="process single_file or folder")
    parser.add_argument('--input_path', type=str, default='./', help="input file or input folder path")
    parser.add_argument('--output_folder', type=str, default='./', help="output folder path")

    args = parser.parse_args()
    main(args.SampleMode, args.CenterFlag, args.mode, args.input_path, args.output_folder)