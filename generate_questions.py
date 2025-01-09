# from data.questions import question_1, question_2, question_3

# from data.questions import final_question_1_simple, final_question_1_medium, final_question_1_hard
# from data.questions import final_question_2_simple, final_question_2_medium, final_question_2_hard
# from data.questions import final_question_3_simple, final_question_3_medium, final_question_3_hard

from data.canGrasp import question_grasp_easy, question_grasp_medium, question_grasp_hard
from data.canLift import question_lift_easy, question_lift_medium, question_lift_hard
from data.canPush import question_push_easy, question_push_medium, question_push_hard
from data.canPerceive import question_perceive_easy, question_perceive_medium, question_perceive_hard

from data.examples import example_1, example_2, example_3, example_4
from data.prompts import prompt_test, prompt_rdf, prompt_with_ontology_explanations, prompt_without_ontology_explanations

from src.DataHandler import QuestionHandler
from src.ExampleHandler import ExampleHandler
from src.QuestionGenerator import QuestionGenerator, PromptGenerator

if __name__ == '__main__':
    print(" -- hellollama : generating questions -- ")
    examples_list = [example_1, example_2, example_3, example_4]
    example_handler = ExampleHandler(examples_list)

    # set the list of questions
    question_list = [question_grasp_easy, question_grasp_medium, question_grasp_hard,
                     question_lift_easy, question_lift_medium, question_lift_hard,
                     question_push_easy, question_push_medium, question_push_hard,
                     question_perceive_easy, question_perceive_medium, question_perceive_hard]

    prompt_generator = PromptGenerator(prompt_without_ontology_explanations)

    generator = QuestionGenerator(prompt_generator)
    
    saving_path = "/home/bdussard/inference_explanation/dataset"
    directory_name = "questions"
    data_saver = QuestionHandler(saving_path, directory_name)
 
    # ============== ADDING EXAMPLES TO GENERATOR ================
    for example in example_handler.examples_:
        generator.add_example(example)

    # ============== ADDING QUESTIONS TO GENERATOR ===============
    for question in question_list:
        generator.add_question(question, with_CoT=True, verbose = False)
    
    # # =============== GENERATE QUESTION VARIATIONS ===========
    generator.generate_question_variations()
    
     # ============== GENERATE QUESTION FILES AND SAVE TO FILE ===============
    for question in generator.questions_:
        data_saver.create_and_save_question_variation(question, generator)