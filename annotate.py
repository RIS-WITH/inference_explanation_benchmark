import json
import os
import sys

def print_progress_bar(current, total, bar_length=40):
    progress = current / total
    arrow = '\033[92m' + '=' * int(progress * bar_length) + '\033[0m'
    spaces = ' ' * (bar_length - len(arrow))
    print(f"\rProgress: |{arrow}{spaces}| {current}/{total} ({int(progress * 100)}%)")

def evaluate_answers(json_file_path, target_file):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        evaluations = []
        current_index = 0
        total_answers = len(data['answers'])
        concepts = data['concepts']

        while current_index < total_answers:

            answer_data = data['answers'][current_index]
            question_id = answer_data['id']
            question = answer_data['question']
            answer_parts = answer_data['answer'].split("\n")
            answer = ""
            for part in answer_parts:
                if len(part) > 20: 
                    answer = part
                    break
            selected_classes = answer_data['selected_classes']
            missing_concepts =  []

            os.system('cls' if os.name == 'nt' else 'clear')
            print_progress_bar(current_index + 1, total_answers)

            print("\033[1m\033[94mQuestion ID:\033[0m", f"\033[92m{question_id}\033[0m")
            print("\033[1m\033[94mQuestion:\033[0m", f"\033[93m{question}\033[0m")
            print("\033[1m\033[94mAnswer:\033[0m", f"\033[95m{answer}\033[0m\n")

            # Validate the answer
            correct = input("\033[1mIs the answer correct? (y/n): \033[0m").strip().lower()
            while correct not in ['y', 'n']:
                correct = input("\033[1mInvalid input. Please type 'y' or 'n': \033[0m").strip().lower()

            # Count selected classes in the answer
            matched_classes = 0
            total_classes = len(selected_classes) + len(concepts)

            for value in selected_classes:
                if value.lower() in answer.lower():
                    matched_classes += 1
                else:
                    print(f"\033[93mThe selected class '{value}' was not found in the answer.\033[0m")
                    verify = input(f"\033[1mDoes '{value}' actually belong to the answer? (y/n): \033[0m").strip().lower()
                    while verify not in ['y', 'n']:
                        verify = input("\033[1mInvalid input. Please type 'y' or 'n': \033[0m").strip().lower()
                    if verify == 'y':
                        matched_classes += 1
                    else:
                        missing_concepts.append(value)
                   
            for value in concepts:
                if value.lower() in answer.lower():
                    matched_classes += 1
                else:
                    print(f"\033[93mThe selected concept '{value}' was not found in the answer.\033[0m")
                    verify = input(f"\033[1mDoes '{value}' actually belong to the answer? (y/n): \033[0m").strip().lower()
                    while verify not in ['y', 'n']:
                        verify = input("\033[1mInvalid input. Please type 'y' or 'n': \033[0m").strip().lower()
                    if verify == 'y':
                        matched_classes += 1
                    else:
                        missing_concepts.append(value)

            score = matched_classes / total_classes if total_classes > 0 else 0

            # Ensure only the latest evaluation for a question is kept
            existing_evaluation_index = next((i for i, eval in enumerate(evaluations) if eval['question_id'] == question_id), None)
            if existing_evaluation_index is not None:
                evaluations[existing_evaluation_index] = {
                    'question_id': question_id,
                    'is_correct': correct == 'y',
                    'score': score,
                    'missing_concepts': missing_concepts
                }
            else:
                evaluations.append({
                    'question_id': question_id,
                    'is_correct': correct == 'y',
                    'score': score,
                    'missing_concepts': missing_concepts
                })

            # Navigation options
            nav = input("\033[1mPress Enter to continue, 'b' to go back to the previous question, or 'q' to quit: \033[0m").strip().lower()
            if nav == 'b':
                continue
            elif nav == 'q':
                break
            else:
                current_index += 1

        # Write evaluations to a file
        with open(target_file, 'w') as output_file:
            json.dump(evaluations, output_file, indent=4)

        print(f"\033[92mEvaluations saved to {target_file}\033[0m")

    except FileNotFoundError:
        print(f"\033[91mThe file {json_file_path} was not found.\033[0m")
    except json.JSONDecodeError:
        print("\033[91mThe file is not a valid JSON.\033[0m")
    except Exception as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")

def display_question_menu(base_path, eval_path):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1m\033[94mSelect the question to annotate\033[0m")

    questions = []
    questions_paths = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json') and not file.endswith('_evaluations.json'):
                rel_path = os.path.relpath(root, base_path)
                question_path = os.path.join(rel_path, file).replace('\\', '/').replace('.json', '')
                questions_paths.append(question_path)
                question_id = file.replace('.json', '')
                questions.append(question_id)

    evaluated_questions = [
        q for q in questions_paths 
        if os.path.exists(os.path.join(eval_path, f"{q}_evaluations.json"))
    ]

    questions_counts = {}
    questions_completion = {}
    for idx, question in enumerate(questions, 1):
        status = 0
        for ev in evaluated_questions:
            if question in ev:
                status = 1
                break

        question_id = question.replace('_b', '').replace('_r', '').replace('_s', '')
        if question_id in questions_completion.keys():
            questions_completion[question_id] += status
            questions_counts[question_id] += 1
        else:
            questions_completion[question_id] = status
            questions_counts[question_id] = 1

    questions = []
    for idx, question in enumerate(questions_completion, 1):
        questions.insert(idx - 1, question)
        if questions_completion[question] == questions_counts[question]:
            print(f"{idx}. {question} '\033[92m{questions_completion[question]}/{questions_counts[question]} ✔\033[0m")
        elif questions_completion[question] > 0:
            print(f"{idx}. {question} '\033[93m{questions_completion[question]}/{questions_counts[question]} ✘\033[0m")
        else:
            print(f"{idx}. {question} '\033[91m{questions_completion[question]}/{questions_counts[question]} ✘\033[0m")

    choice = input("\033[1mSelect a question by number: \033[0m").strip()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(questions):
        choice = input("\033[1mInvalid choice. Select a question by number: \033[0m").strip()

    return questions[int(choice) - 1]

def display_model_menu(base_path, eval_path, question):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\033[1m\033[94mSelect the model for question: {question}\033[0m")


    models = []
    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            if dir != "baseline" and dir != "shuffle" and dir != "rule":
                models.append(dir)

    base_count = {}
    completion_count = {}
    id = 1
    for model in models:
        base_count[model] = 0
        completion_count[model] = 0

        base_model_path = os.path.join(base_path, model)
        for root, dirs, files in os.walk(base_model_path):
            for file in files:
                if question in file and not file.endswith('_evaluations.json'):
                    base_count[model] += 1

        eval_model_path = os.path.join(eval_path, model)
        for root, dirs, files in os.walk(eval_model_path):
            for file in files:
                if question in file and file.endswith('_evaluations.json'):
                    completion_count[model] += 1

        if completion_count[model] == base_count[model]:
            print(f"{id}. {model} '\033[92m{completion_count[model]}/{base_count[model]} ✔\033[0m")
        elif completion_count[model] > 0:
            print(f"{id}. {model} '\033[93m{completion_count[model]}/{base_count[model]} ✘\033[0m")
        else:
            print(f"{id}. {model} '\033[91m{completion_count[model]}/{base_count[model]} ✘\033[0m")
        id += 1
    
    choice = input("\033[1mSelect a model by number: \033[0m").strip()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(models):
        choice = input("\033[1mInvalid choice. Select a model by number: \033[0m").strip()

    return models[int(choice) - 1]

def display_variant_menu(base_path, eval_path, question, model):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\033[1m\033[94mSelect the variation for question {question} into model {model}\033[0m")

    variations_names = ["baseline", "rule", "shuffle"]
    variations = []
    evaluated = []
    base_model_path = os.path.join(base_path, model)
    eval_model_path = os.path.join(eval_path, model)
    for variation in variations_names:
        base_var_path = os.path.join(base_model_path, variation)
        for root, dirs, files in os.walk(base_var_path):
            for file in files:
                if question in file and not file.endswith('_evaluations.json'):
                    variations.append(variation)

        eval_var_path = os.path.join(eval_model_path, variation)
        for root, dirs, files in os.walk(eval_var_path):
            for file in files:
                if question in file and file.endswith('_evaluations.json'):
                    evaluated.append(variation)

    for idx, variation in enumerate(variations, 1):
        status = '\033[92m✔\033[0m' if variation in evaluated else '\033[91m✘\033[0m'
        print(f"{idx}. {variation} {status}")

    choice = input("\033[1mSelect a model by number: \033[0m").strip()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(variations):
        choice = input("\033[1mInvalid choice. Select a model by number: \033[0m").strip()

    return variations[int(choice) - 1]

def main():
    root_path = "/home/gsarthou/Documents/projects/ollama/"
    base_path = root_path + "answers"
    evaluations_path = root_path + "evaluations"

    if not os.path.exists(evaluations_path):
        os.makedirs(evaluations_path)

    question = display_question_menu(base_path, evaluations_path)
    model = display_model_menu(base_path, evaluations_path, question)
    variant = display_variant_menu(base_path, evaluations_path, question, model)
    print(f"{model} / {variant} / {question}")

    rel_path = model + "/" + variant + "/" + question + "_"  + variant[0] + ".json"

    source_file = os.path.join(base_path, rel_path)
    target_path = os.path.join(evaluations_path, model, variant)
    target_file = os.path.join(evaluations_path, rel_path)
    target_file = target_file.replace(".json", "_evaluations.json")

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    evaluate_answers(source_file, target_file)

if __name__ == "__main__":
    main()
