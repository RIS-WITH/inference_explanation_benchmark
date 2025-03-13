# Data 
The template questions are created in this folder, with their complexity levels as well as the SWRL rule.
Each question is composed of a set of semantic triples, which represent the justifications used to validate the given SWRL rule.
Template are used to generate questions with variations on the concepts used, anonymise the individual names and variations on the numerical values.

The main prompt used is in the 'prompts.py' file.
The examples provided in Chain-of-Thought (CoT) to the models are in the 'examples.py' file.

# Generating Questions

The 'generate_questions.py' script allows to generate the questions according to the imported data.


# Running models on the questions

The 'generate_responses.py' script allows to query the models with the generated questions, and save the answers as well as the expected concepts into a new folder (answers).
You can choose the models you want to investigate with the list 'models', but you will first have to pull them according to ollama's guidelines.

# Evaluating Answers

The 'answers' folder is used for the annotator to browse through the models' answers and evaluate them based on correctness (True/False) and completeness (True/False for each expected concept). A new folder 'evaluations' will be created to save those evaluations with the question_id, the model's answer, their correctness and completeness scores, and the missing concepts in the answer according to the annotator's evaluation.

The annotation process goes as following:
- run the script ('evaluate.py')
- choose the model you want to annotate
- choose the condition
- choose the question

The annotations are automatically saved once you complete the annotation of a sample (question + condition + complexity).
