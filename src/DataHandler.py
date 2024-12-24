import json
import os
import random
import copy

class QuestionHandler:
    def __init__(self, folder_path, folder_name):
        self.folder_path_ = folder_path
        self.folder_name_ = folder_name
        self.variation_types_  = ["baseline", "shuffle", "rule"]
        self.create_dataset_folders()
    
    def create_dataset_folders(self):
        question_path = self.folder_path_ + self.folder_name_
        try:
            os.mkdir(question_path)
            for var_folder in self.variation_types_:
                os.mkdir(question_path + "/" + var_folder)
            print(f"Directory '{question_path}' created successfully.")
        except FileExistsError:
            print(f"Directory '{question_path}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{question_path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
             
    def create_and_save_question_variation(self, question, generator):
        saving_path = self.folder_path_ + self.folder_name_
        
        filename_b = question.id_question_ + "_baseline"
        self.create_variation_file(question, saving_path + "/baseline/", filename_b)

        filename_s = question.id_question_ + "_shuffle"
        self.create_variation_file(question, saving_path + "/shuffle/", filename_s)

        filename_r = question.id_question_ + "_rule"
        self.create_variation_file(question, saving_path + "/rule/", filename_r, with_rule=True)

        # loop over variations of the question (indiv names and classes)
        for var_question in question.generated_questions_:

            # random names, with example, without rule
            baseline_question = generator.create_question(var_question, with_rule = False)
            saved_data = {"id" : var_question.id_question_ + "b", "selected_classes" : var_question.selected_classes_, "question" : baseline_question}
            self.write_to_file(saving_path + "/baseline/" + filename_b, saved_data)

            # random names, shuffled_explanations, with example, without rule
            var_question_shuffled = copy.deepcopy(var_question)
            random.shuffle(var_question_shuffled.explanations_)
            shuffled_question = generator.create_question(var_question_shuffled, with_rule = False)
            saved_data = {"id" : var_question.id_question_ + "s", "selected_classes" : var_question.selected_classes_, "question" : shuffled_question}
            self.write_to_file(saving_path + "/shuffle/" + filename_s, saved_data)

            # random names, with example, with rule
            rule_question = generator.create_question(var_question, with_rule = True)
            saved_data = {"id" : var_question.id_question_ + "r", "selected_classes" : var_question.selected_classes_, "question" : rule_question}
            self.write_to_file(saving_path + "/rule/" + filename_r, saved_data)   

    def write_to_file(self, path_file, saved_question):
        
        with open(path_file + '.json', 'r') as infile:
                my_data = json.load(infile)
            
        my_data["questions"].append(saved_question)

        with open(path_file + '.json', 'w') as outfile:
            json.dump(my_data, outfile, indent = 2)

    def create_variation_file(self, question, path_folder, path_file, with_rule = False):
        init_prompt = []
        if(with_rule == True):
            init_prompt = question.init_prompt_rule_
            rule = question.rule_
        else:
            init_prompt = question.init_prompt_
            rule = None

        question_dict = {"id": question.id_question_, "template": question.template_question_, 'rule': rule, "init_prompt" : init_prompt, "questions": []}
        json_object = json.dumps(question_dict, indent=2)

        with open(path_folder + path_file + '.json', "w") as file:
            file.write(json_object)

    def load_questions(self, path_to_folder, variation_name):
        res = []
        path_to_var = path_to_folder + "/" + variation_name + "/"
        for q in os.listdir(path_to_var):
            with open(path_to_var + q, 'r') as file:
                data = json.load(file)
                res.append(data)

        return res
    
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
        model_path = answer_path + "/" + self.model_name_
        try:
            os.mkdir(answer_path)
            for var_folder in self.variation_types:
                os.mkdir(model_path + "/" + var_folder)
            print(f"Directory '{model_path}' created successfully.")
        except FileExistsError:
            print(f"Directory '{model_path}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{model_path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        os.mkdir(model_path)
    
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

        answer_dict = {"id": id_answer, "template": question['template'], "answers": []}
        json_object = json.dumps(answer_dict, indent=2)

        with open(filename_answer, "w") as file:
            file.write(json_object)
            
        return filename_answer
               
    def create_variation_file(self, question, path_folder, path_file):
    
        answer_dict = {"id": question.id_question_, "template": question.template_question_, "answers": []}
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
            
