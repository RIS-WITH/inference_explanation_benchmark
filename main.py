import os

from src.QuestionGenerator import QuestionGenerator
from src.OllamaHandler import OllamaHandler
from src.DataHandler import DataHandler, AnswerHandler
from src.ExampleHandler import ExampleHandler

from data.examples import example_0, example_1

from data.questions import question_1, question_2


if __name__ == '__main__':
    print(" -- hellollama -- ")
    #models = ["llama3.2", "llama3.1", "gemma2:2b", "gemma2", "mistral", "phi3", "phi3:medium"]
    # set the list of examples
    examples_list = [example_0, example_1]
    example_handler = ExampleHandler(examples_list)

    # set the list of questions
    question_list = [question_1, question_2]

    generator = QuestionGenerator()
 
    # ============== ADDING EXAMPLES TO GENERATOR ================
    for example in example_handler.examples_:
        generator.add_example(example)

    # ============== ADDING QUESTIONS TO GENERATOR ===============
    for question in question_list:
        generator.add_question(question)

    # =============== GENERATE QUESTION VARIATIONS ===========
    generator.generate_question_variations(nb_var=10)

    model = "llama3.2"
    ollama = OllamaHandler(model)

    saving_path = "/home/bdussard/"
    directory_name = "dataset"

    data_saver = DataHandler(saving_path, directory_name)

    # ============== GENERATE QUESTION FILES AND SAVE TO FILE ===============
    for question in generator.questions_:
        data_saver.save_question(question, generator)

    #  ================ LOAD QUESTIONS FROM FILE =============
    questions_baseline = data_saver.load_questions(saving_path + directory_name, "baseline")
    questions_shuffle = data_saver.load_questions(saving_path + directory_name, "shuffle")
    questions_rule = data_saver.load_questions(saving_path + directory_name, "rule")

    saving_path_answers = "/home/bdussard/answer_results/"
    directory_name = model
    
    answer_saver = AnswerHandler(saving_path_answers, model)
    
    questions_dict = {'baseline': questions_baseline, 'shuffle': questions_shuffle, 'rule' :questions_rule}
    
    for question_key in questions_dict:
        print(" ===  evaluating questions ", question_key)
        answer_saver.create_answer_folder(question_key)
        for question in questions_dict[question_key]:
            id_question = question['id']
            filename_answer = answer_saver.create_answer_file(id_question, question_key, question)
            for question_var in question['questions']:
                formatted_question = ollama.build_question(question, question_var['question'])
                print(" -- question is : ", formatted_question[-2]['content'])
                answer = ollama.call(formatted_question)
                print(" -- answer is :", answer)
                answer_id = "a" + question_var['id'][1:]
        
                answer_saver.save_answer(filename_answer, answer_id, question_var['selected_classes'], answer)
                
    # Loop over questions :
    # for qu in questions_rule:
    #     print("qu is : ", qu)
    #     # Loop over variation of question :
    #     for var in qu['questions']:
    #         formatted_question = ollama.build_question(qu, var['question'])
    #         print("after format : ", formatted_question)
    #         # answer = ollama.call(formatted_question)
    #         # print("question is : ", var['question'])
    #         # print("answer is : ", answer, "\n")
    #         # answer_saver.save_answer(var, answer)
