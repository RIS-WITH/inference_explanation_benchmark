from src.OllamaHandler import OllamaHandler
from src.DataHandler import AnswerHandler
import numpy as np
import copy

if __name__ == '__main__':
    # models in the paper
    models = ["llama3.2:3b", "llama3.1:8b", "gemma2:2b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"]  
  
    directory_path =  "/home/bdussard/inference_explanation/dataset_test/"
    questions_folder = "questions"

    for model in models:
        ollama = OllamaHandler(model)
    
        answer_folder = "answers"
        answer_model = model
        
        answer_saver = AnswerHandler(directory_path, answer_folder, model)
        
        #  ================ LOAD QUESTIONS FROM FILE =============
        questions_baseline = answer_saver.load_questions(directory_path + questions_folder, "baseline")
        questions_shuffle = answer_saver.load_questions(directory_path + questions_folder, "shuffle")
        questions_rule = answer_saver.load_questions(directory_path + questions_folder, "rule")
        
        #  ================ LINK CONDITIONS =============
        questions_dict = {'baseline': questions_baseline, 'shuffle': questions_shuffle, 'rule' :questions_rule}

        #  ================ EVALUATE QUESTIONS =============
        for question_key in questions_dict:
            print(" ===  evaluating questions ", question_key)
            answer_saver.create_variation_folder(question_key)
            for question in questions_dict[question_key]:
                id_question = question['id']
                filename_answer = answer_saver.create_answer_file(id_question, question_key, question)
                for question_var in question['questions']:
                    
                    formatted_question = ollama.build_question(question['init_prompt'], question_var['question'], with_CoT=True)
                    print("========= new question with CoT ========")
                    print("question is : ", question_var['question'])
                    answer = ollama.call(formatted_question, False, False)
                    print("answer is : ", answer)
                    print("========================================")
                    
                    answer_id = "a" + question_var['id'][1:]
                    # adding question_var['question'] to improve readibility in file
                    answer_saver.save_answer(filename_answer, answer_id, question_var['selected_classes'], question_var['question'], answer)