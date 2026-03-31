from data_elements.canGrasp import grasp_manager
from data_elements.canLift import lift_manager
from data_elements.canPush import push_manager
from data_elements.canPerceive import perceive_manager

from data_elements.examples import question_1, question_2, question_3, question_4
from data_elements.prompts import prompt_without_ontology_explanations

from src.QuestionGenerator import QuestionGenerator

if __name__ == '__main__':

    examples_list = [question_1, question_2, question_3, question_4]
    for example in examples_list:
        example.generate()

    question_managers = [grasp_manager, lift_manager, push_manager, perceive_manager]
    for manager in question_managers:
        manager.generate(integrate_class_expressions_in_explanation=False, count=20)
    
    saving_path = "/home/gsarthou/Documents/LAAS/Code/inference_explanation_benchmark/dataset_2026"
    generator = QuestionGenerator(saving_path,
                                  prompt_without_ontology_explanations,
                                  examples_list,
                                  question_managers)
     
    generator.generateBaseline()
    generator.generateLabeled()