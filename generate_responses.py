from src.OllamaHandler import OllamaHandler
from src.DataHandler import AnswerHandler

if __name__ == '__main__':
    print(" -- hellollama -- ")

    #models = ["llama3.2", "llama3.1", "gemma2:2b", "gemma2", "mistral", "phi3", "phi3:medium"]
    # set the list of examples

    model = "gemma2:27b"

    ollama = OllamaHandler(model)
 
    question_path = "/home/bdussard/"
    questions_folder = "dataset_q3"
    
    answer_path = "/home/bdussard/"
    answer_folder = "answer_folder_noCoT"
    answer_model = model
    
    answer_saver = AnswerHandler(answer_path, answer_folder, model)
    
     #  ================ LOAD QUESTIONS FROM FILE =============
    questions_baseline = answer_saver.load_questions(question_path + questions_folder, "baseline")
    questions_shuffle = answer_saver.load_questions(question_path + questions_folder, "shuffle")
    questions_rule = answer_saver.load_questions(question_path + questions_folder, "rule")
    
    questions_dict = {'baseline': questions_baseline, 'shuffle': questions_shuffle, 'rule' :questions_rule}
    
    for question_key in questions_dict:
        print(" ===  evaluating questions ", question_key)
        answer_saver.create_variation_folder(question_key)
        for question in questions_dict[question_key]:
            id_question = question['id']
            filename_answer = answer_saver.create_answer_file(id_question, question_key, question)
            for question_var in question['questions']:
                formatted_question = ollama.build_question(question, question_var['question'], with_CoT=True)
                print(" -- question is : ", formatted_question[-2]['content'])
                answer = ollama.call(formatted_question)
                print(" -- answer is :", answer)
                answer_id = "a" + question_var['id'][1:]
                # adding question_var['question'] to improve readibility in file
                answer_saver.save_answer(filename_answer, answer_id, question_var['selected_classes'], question_var['question'], answer)