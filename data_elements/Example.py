from data_elements.VariableManager import VariableManager

class SubQuestionExample:
  def __init__(self, infered_fact, translation, rule, explanation):
    self.infered_fact = infered_fact
    self.translation = " ".join(translation.split())
    self.rule = rule
    self.explanation = explanation

class QuestionExample:
  def __init__(self, infered_fact, translation, rule, explanation, sub_questions):
    self.infered_fact = infered_fact
    self.translation = " ".join(translation.split())
    self.rules = [rule]
    self.explanations = [explanation]
    self.sub_questions = sub_questions
    self.variable_manager = VariableManager()

  def getRules(self, to_string=False):
    """
    Concatenates the main rule with all sub-question rules.
    If instance_id is provided, it instantiates the strings.
    """
    all_rules = self.rules + [sq.rule for sq in self.sub_questions]
    
    return "\n".join(all_rules) if to_string else all_rules
  
  def getExplanations(self, instance=False, use_label=False, to_string=False):
    """
    Concatenates the main explanation with all sub-question explanations.
    If instance_id is provided, it instantiates the strings.
    """
    all_explanations = self.explanations + [sq.explanation for sq in self.sub_questions]
    
    if instance is True:
      all_explanations = [self.variable_manager.instantiate(e, 0, use_label) for e in all_explanations]
    
    return ", ".join(all_explanations) if to_string else all_explanations

  def generate(self):
    self.variable_manager.extractVariables(self.explanations)
    for sub_question in self.sub_questions:
      self.variable_manager.extractVariables([sub_question.explanation])
    self.variable_manager.generateInstances(1)

  def instantiate(self, data, use_label):
    return self.variable_manager.instantiate(data, 0, use_label)