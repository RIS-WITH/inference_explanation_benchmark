from src.OllamaHandler import OllamaHandler
from src.DataHandler import AnswerHandler
import numpy as np
import copy

if __name__ == '__main__':
    print(" -- hellollama -- ")
    # "llama3.2", "llama3.1:8b", "gemma2:2b", "gemma2", "phi3", "phi3:medium", "gemma2:27b"
    # ========== 1.7GB ====== 5.0GB ====   1.6GB   ====  5.4GB =====   16GB === 2.2GB === 2.2GB ========14GB ======== 4.9GB =========  2GB  ==== ==    7.1GB    ===== 12GB =====
    # models = ["gemma:2b", "gemma:7b", "gemma2:2b", "gemma2:9b", "gemma2:27b", "phi3", "phi3.5", "phi3:medium", "llama3.1:8b", "llama3.2:3b", "mistral-nemo:12b", "mistral-small:22b", ""]
    #models = ["llama3.2:3b", "llama3.1:8b", "gemma2:2b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"] # "phi3", "phi3:medium", ]  "mistral-nemo:12b"
    # set the list of examples
    #models = ["mistral", "phi3:mini", "phi3:medium"]
    models = ["llama3.2:3b", "llama3.1:8b", "gemma2:2b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"]
    question_path = "/home/bdussard/inference_explanation/dataset_fix/"
    questions_folder = "questions"
    questions_without_answers = []
    #model = "gemma2:27b"
    for model in models:
        ollama = OllamaHandler(model)
    
        answer_path = "/home/bdussard/inference_explanation/dataset_fix/"
        answer_folder = "answers"
        answer_model = model
        
        answer_saver = AnswerHandler(answer_path, answer_folder, model)
        
        #  ================ LOAD QUESTIONS FROM FILE =============
        questions_baseline = answer_saver.load_questions(question_path + questions_folder, "baseline")
        questions_shuffle = answer_saver.load_questions(question_path + questions_folder, "shuffle")
        questions_rule = answer_saver.load_questions(question_path + questions_folder, "rule")
        
        questions_dict = {'baseline': questions_baseline, 'shuffle': questions_shuffle, 'rule' :questions_rule}
        #questions_dict = {'rule' :questions_rule}
        for question_key in questions_dict:
            print(" ===  evaluating questions ", question_key)
            answer_saver.create_variation_folder(question_key)
            for question in questions_dict[question_key]:
                id_question = question['id']
                filename_answer = answer_saver.create_answer_file(id_question, question_key, question)
                for question_var in question['questions']:
                    if(("q_push_medium_16" in question_var['id']) or ("q_push_easy_19" in question_var['id'])):
                    # =========== To evaluate the difference between CoT and no CoT =============
                    # print("========= new question ========")
                    # print("question is : ", question_var['question'])
                    # answer_without_cot = ollama.build_and_call(question['init_prompt'], question_var['question'], with_CoT=False)
                    # print("answer without COT is : ", answer_without_cot)
                    # answer_cot = ollama.build_and_call(question['init_prompt'], question_var['question'], with_CoT=True)
                    # print("answer COT is : ", answer_cot)
                    # print("========= ============= ========")

                        formatted_question = ollama.build_question(question['init_prompt'], question_var['question'], with_CoT=True)
                        print("========= new question with CoT ========")
                        print("question is : ", question_var['question'])
                        answer = ollama.call(formatted_question, False, False)
                        print("answer is : ", answer)
                        print("========================================")
                        
                        # if(answer == ""):
                        #     questions_without_answers.append(formatted_question)
                            
                        answer_id = "a" + question_var['id'][1:]
                        # adding question_var['question'] to improve readibility in file
                        answer_saver.save_answer(filename_answer, answer_id, question_var['selected_classes'], question_var['question'], answer)
                    
    # np.save(answer_path + "question_without_answers.npy", questions_without_answers)