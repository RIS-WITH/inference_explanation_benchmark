import os
import json

class QuestionGenerator:
  def __init__(self, path, base_prompt, examples, questions):
    self.path = path + "/questions"
    self.base_prompt = " ".join(base_prompt.split())
    self.examples = examples
    self.questions = questions

    self._createDirectory(self.path)

  def generateBaseline(self):
    variation = "baseline"
    self._createDirectory(self.path + "/" + variation)

    baseline_prompt = self.getBaselinePrompt(False)

    for question in self.questions:
      for complexity in question.levels:
        question_set = self._getBaseQuestionSet(question, complexity)

        question_set["init_prompt"] = baseline_prompt
        question_set["questions"] = self.getBaselineQuestions(question, complexity, False)
        
        self._saveQestionSet(question_set, variation)

  def generateLabeled(self):
    variation = "labeled"
    self._createDirectory(self.path + "/" + variation)

    baseline_prompt = self.getBaselinePrompt(True)

    for question in self.questions:
      for complexity in question.levels:
        question_set = self._getBaseQuestionSet(question, complexity)

        question_set["init_prompt"] = baseline_prompt
        question_set["questions"] = self.getBaselineQuestions(question, complexity, True)
        
        self._saveQestionSet(question_set, variation)

  def getBaselinePrompt(self, use_label):
    prompt = []
    prompt.append({"role" : "user",
                   "content" : self.base_prompt})
    
    for example in self.examples:
      user_content = "-Inference : " + example.instantiate(example.infered_fact, use_label)
      user_content += "\n-Justifications : " + example.getExplanations(instance=True, use_label=use_label, to_string=True)
      user_content += "\n-Rules : " + example.getRules(to_string=True)
      prompt.append({"role" : "user",
                     "content" : user_content})
      prompt.append({"role" : "assistant",
                     "content" : "Let's translate. Translation is " + example.translation + "."})
    
    return prompt
  
  def getBaselineQuestions(self, question, complexity, use_label):
    questions = []

    for i in range(question.nb_variations):

      raw_justifications_blob = " ".join(question.explanations[complexity])
        
      if use_label:
          current_map = question.variable_manager.labeled_instances[i]
      else:
          current_map = question.variable_manager.instances[i]
          
      # Extract selected_classes
      selected_classes = []
      for cv in question.variable_manager.class_variables:
        if cv.pattern in raw_justifications_blob and cv.pattern in current_map:
          selected_classes.append(current_map[cv.pattern])
              
      # Extract selected_names
      selected_names = []
      for var in question.variable_manager.variables:
          if var in raw_justifications_blob and var in current_map:
              selected_names.append(current_map[var])
              
      # Construct the question string
      inference = question.variable_manager.instantiate(question.infered_fact, i, use_label)
      
      # Then grab the justifications
      justifications = question.getExplanations(complexity, instance_id=i, use_label=use_label, to_string=True)
      rules = question.getRules(complexity, to_string=True, separator="\n\t")
      
      # Stitch them together in the exact layout you showed me
      question_text = f"-Inference : {inference} \n -Justifications : {justifications} \n -Rules : {rules}"
      
      # Build ID
      suffix = "l" if use_label else "b"
      question_id = f"q_{question.names[complexity]}_{i}{suffix}"
      
      # Package it up
      questions.append({
          "id": question_id,
          "selected_classes": selected_classes,
          "selected_names": selected_names,
          "question": question_text
      })
        
    return questions

  def _getBaseQuestionSet(self, question, complexity):
    question_set_id = "q_" + question.names[complexity]
    question_set = {}
    question_set["id"] = question_set_id

    question_set["template"] = {}
    question_set["template"]["fact"] = question.infered_fact
    question_set["template"]["explanation"] = question.explanations[complexity]

    question_set["rules"] = question.rules[complexity]

    question_set["concepts"] = question.rule.concepts

    return question_set

  def _saveQestionSet(self, question_set, variation):
    json_object = json.dumps(question_set, indent=2)

    with open(self.path + '/' + variation + '/' + question_set["id"] + '_' + variation + '.json', "w") as file:
      file.write(json_object)

  def _createDirectory(self, directory):
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
        return True
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")
        return True
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory}'.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False