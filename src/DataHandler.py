import json
import os
import random
import copy
    
class AnswerHandler:
    def __init__(self, folder_path, folder_name, model_name):
        self.folder_path_ = folder_path
        self.folder_name_ = folder_name
        self.model_name_ = model_name
        self.filename_b_ = None
        self.filename_s_ = None
        self.filename_r_ = None
        self.variation_types = ["baseline", "shuffle", "rule"]
        self.create_model_folder()
        
    def create_model_folder(self):
        
        answer_path = self.folder_path_ + self.folder_name_

        if not os.path.exists(answer_path):
            os.makedirs(answer_path)
        if not os.path.exists(os.path.join(answer_path, self.model_name_)):
            model_path = os.path.join(answer_path, self.model_name_)
            os.makedirs(model_path)
            for var_folder in self.variation_types:
                var_path = os.path.join(answer_path, self.model_name_, var_folder)
                os.mkdir(var_path)
        
    
    def create_variation_folder(self, variation_name):
        answer_path = self.folder_path_ + self.folder_name_
        model_path = answer_path + "/" + self.model_name_
        try:
            os.mkdir(model_path + "/" + variation_name)
            print(f"Directory '{variation_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{variation_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{variation_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def create_answer_file(self, id_question, id_var, question):
    
        id_answer =  "a" + id_question[1:] + "_" + id_var[0]
        filename_dir = self.folder_path_ + self.folder_name_ + "/" + self.model_name_
        filename_answer = filename_dir + "/" + id_var + "/" + id_answer + '.json'

        answer_dict = {"id": id_answer, "template": question['template'], "concepts" : question['concepts_rule'], "answers": []}
        json_object = json.dumps(answer_dict, indent=2)

        with open(filename_answer, "w") as file:
            file.write(json_object)
            
        return filename_answer
               
    def create_variation_file(self, question, path_folder, path_file):
    
        answer_dict = {"id": question.id_question_, "template": question.template_question_, "concepts" : question['concepts_rule'], "answers": []}
        json_object = json.dumps(answer_dict, indent=2)

        with open(path_folder + path_file + '.json', "w") as file:
            file.write(json_object)
    
    def write_to_file(self, path_file, saved_answer):
        with open(path_file, 'r') as infile:
                my_data = json.load(infile)
            
        my_data["answers"].append(saved_answer)

        with open(path_file, 'w') as outfile:
            json.dump(my_data, outfile, indent = 2)
              
    def save_answer(self, filename_answer, answer_id, selected_classes, question, answer):
        saving_path = filename_answer
        saved_answer = {"id" : answer_id, "selected_classes":  selected_classes, "question" : question,"answer" : answer}
        self.write_to_file(saving_path, saved_answer)
   
    def load_answers(self, path_to_folder, variation_name):
        res = []
        path_to_var = path_to_folder + "/" + variation_name + "/"
        for q in os.listdir(path_to_var):
            with open(path_to_var + q, 'r') as file:
                data = json.load(file)
                res.append(data)

        return res
    
    def load_questions(self, path_to_folder, variation_name):
        res = []
        path_to_var = path_to_folder + "/" + variation_name + "/"
        for q in os.listdir(path_to_var):
            with open(path_to_var + q, 'r') as file:
                data = json.load(file)
                res.append(data)

        return res
            
