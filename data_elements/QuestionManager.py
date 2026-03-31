class QuestionRule:
  def __init__(self, property, rule, concepts):
    self.property = property
    self.rule = rule
    self.concepts = concepts

class QuestionManager:
  def __init__(self, rule, variable_manager, affordance, capability_expl, disposition_expl, property_expl):
    self.rule = rule
    self.infered_fact = "__agent__|" + self.rule.property + "|__object__"
    self.variable_manager = variable_manager
    self.affordance = affordance
    self.capability_expl = capability_expl
    self.disposition_expl = disposition_expl
    self.property_expl = property_expl

    self.explanations = {"easy" : "",
                         "medium" : "",
                         "hard" : ""}

    self.rules = {"easy" : "",
                  "medium" : "",
                  "hard" : ""}
    
    self.names = {"easy" : self.rule.property + "_easy",
                  "medium" : self.rule.property + "_medium",
                  "hard" : self.rule.property + "_hard"}
    
    self.levels = ["easy", "medium", "hard"]
    self.nb_variations = 0
    
  def generateExplanations(self, integrate_class_expressions):
    self.explanations["easy"] = self.affordance.capability + \
                                self.capability_expl.getEasyExplanation(integrate_class_expressions) + \
                                self.affordance.disposition + \
                                self.disposition_expl.getEasyExplanation(integrate_class_expressions) + \
                                self.property_expl.getEasyExplanation(integrate_class_expressions) + \
                                self.affordance.match

    self.explanations["medium"] = self.affordance.capability + \
                                  self.capability_expl.getMediumExplanation(integrate_class_expressions) + \
                                  self.affordance.disposition + \
                                  self.disposition_expl.getMediumExplanation(integrate_class_expressions) + \
                                  self.property_expl.getMediumExplanation(integrate_class_expressions) + \
                                  self.affordance.match
    
    self.explanations["hard"] = self.affordance.capability + \
                                self.capability_expl.getHardExplanation(integrate_class_expressions) + \
                                self.affordance.disposition + \
                                self.disposition_expl.getHardExplanation(integrate_class_expressions) + \
                                self.property_expl.getHardExplanation(integrate_class_expressions) + \
                                self.affordance.match
    
  def generateRules(self, integrate_class_expressions):
    base_rule = " ".join(self.rule.rule.split())
    self.rules["easy"] = [base_rule]
    if integrate_class_expressions is True:
      self.rules["easy"] += [self.capability_expl.class_expression.easy,
                             self.disposition_expl.class_expression.easy]
      
    self.rules["medium"] = [base_rule]
    if integrate_class_expressions is True:
      self.rules["medium"] += [self.capability_expl.class_expression.medium,
                               self.disposition_expl.class_expression.medium,
                               self.property_expl.class_expression.medium]
      
    self.rules["hard"] = [base_rule]
    if integrate_class_expressions is True:
      self.rules["hard"] += [self.capability_expl.class_expression.hard,
                             self.disposition_expl.class_expression.hard,
                             self.property_expl.class_expression.hard]
      
  def generate(self, integrate_class_expressions_in_explanation, count):
    self.generateExplanations(integrate_class_expressions_in_explanation)
    self.generateRules(not integrate_class_expressions_in_explanation)

    self.variable_manager.extractVariables([self.explanations["easy"],
                                            self.explanations["medium"],
                                            self.explanations["hard"]])
    self.variable_manager.generateInstances(count)
    self.nb_variations = count

  def getExplanations(self, complexity, instance_id, use_label=False, to_string=False):
    """Fetches, instantiates, and optionally joins the explanation list."""
    exps = self.explanations[complexity]
    exps = [self.variable_manager.instantiate(e, instance_id, use_label) for e in exps]
        
    return ", ".join(exps) if to_string else exps
  
  def getRules(self, complexity, to_string=False, separator="\n"):
    """Fetches and optionally joins the rule list without instantiation."""
    rules = self.rules[complexity]
    
    return separator.join(rules) if to_string else rules