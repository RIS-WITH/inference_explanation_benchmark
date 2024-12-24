from data.questions import question_1, question_2, question_3
from data.examples import example_0, example_1
from data.prompts import prompt_test

from src.DataHandler import QuestionHandler
from src.ExampleHandler import ExampleHandler
from src.QuestionGenerator import QuestionGenerator, PromptGenerator

if __name__ == '__main__':
    print(" -- hellollama : generating questions -- ")
    examples_list = [example_0, example_1]
    example_handler = ExampleHandler(examples_list)

    # set the list of questions
    question_list = [question_1, question_2, question_3]
    
    prompt_generator = PromptGenerator(prompt_test)

    generator = QuestionGenerator(prompt_generator)
    
    saving_path = "/home/bdussard/"
    directory_name = "dataset_q3"
    data_saver = QuestionHandler(saving_path, directory_name)
 
    # ============== ADDING EXAMPLES TO GENERATOR ================
    for example in example_handler.examples_:
        generator.add_example(example)

    # ============== ADDING QUESTIONS TO GENERATOR ===============
    for question in question_list:
        generator.add_question(question, with_CoT=True)

    # # =============== GENERATE QUESTION VARIATIONS ===========
    generator.generate_question_variations(nb_var=10)
    
     # ============== GENERATE QUESTION FILES AND SAVE TO FILE ===============
    for question in generator.questions_:
        data_saver.create_and_save_question_variation(question, generator)