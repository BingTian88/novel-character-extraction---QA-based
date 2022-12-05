## split the data
import json
import os
import random
class data_split_and_merge():

    def split_data(data_file):  #split_ratio = 8:2
        f = open(data_file)
        data = json.load(f)
        set_seed = 11
        random.Random(set_seed).shuffle(data['data'])
        int(0.8 * len(data['data']))
        res_dic_train = {}
        res_dic_eval = {}
        res_dic_train['data'] =  data['data'][:int(0.8 * len(data['data']))]
        res_dic_eval['data'] =  data['data'][int(0.8 * len(data['data'])):]   
        output_folder = data_file.split('/')[0]
        with open(os.path.join(output_folder, data_file.split('/')[-1].split('.')[-2])+'_train.json', 'w', encoding="utf-8") as fp:
                json.dump(res_dic_train, fp) 
        with open(os.path.join(output_folder, data_file.split('/')[-1].split('.')[-2])+'_eval.json', 'w', encoding="utf-8") as fp:
                json.dump(res_dic_eval, fp) 

    ## merge the data

    def merge_data(data_file_1, data_file_2):  
        f_1 = open(data_file_1)
        f_2 = open(data_file_2)
        data_1 = json.load(f_1)
        data_2 = json.load(f_2)
        data_1['data'].extend(data_2['data']) 
        for idx, sample in enumerate(data_1['data']):
                sample['id'] = str(idx)
        output_folder = data_file_1.split('/')[0]


        with open(os.path.join(output_folder, data_file_1.split('/')[-1].split('.')[-2]) + '+' + data_file_2.split('/')[-1].split('.')[-2] + '.json', 'w', encoding="utf-8") as fp:
                json.dump(data_1, fp) 
        return str(os.path.join(output_folder, data_file_1.split('/')[-1].split('.')[-2]) + '+' + data_file_2.split('/')[-1].split('.')[-2] + '.json')
    
        ## 处理新书的格式（2217876.jsonl）
    def process_new_books(input_path, out_path):
        with open(input_path, "r", encoding="utf-8") as f:
                raw_examples = f.readlines()
                examples_list = []

                for example in raw_examples:
                    data = json.loads(example)
                    entities = data['entities']
                    label_res = []
                    for label in entities:
                        item_list = [label['start_offset'], label['end_offset'], label['label']]
                        label_res.append(item_list)
                    data['label'] = label_res
                    examples_list.append(json.dumps(data))
                    examples_list.append('\n')
        with open(out_path, 'w') as f:
            f.writelines(examples_list)
            
    
    

    

    
