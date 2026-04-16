class AffordanceBase:
  def __init__(self, capa, disp, match):
    if capa is None:
      self.capability = [
                          "__agent__|Type|__Agent__",
                          "__Agent__|SubClassOf|Agent",
                          "__agent__|hasCapability|__agent_capa__"
                        ]
    else:
      self.capability = capa

    if disp is None:
      self.disposition = [
                          "__object__|Type|__Object__",
                          "__Object__|SubClassOf|Object",
                          "__object__|hasDisposition|__object_disp__"
                         ]
    else:
      self.disposition = disp
    
    self.match = match

class ClassExpression:
  def __init__(self, easy, medium, hard):
    self.easy = easy
    self.medium = medium
    self.hard = hard

class ClassExpressionExplanation:
  def __init__(self, class_expression, easy, medium, hard, concatenate = True):
    self.class_expression = class_expression
    self.easy = easy
    self.medium = easy + medium
    if concatenate is True:
      self.hard = easy + medium + hard
    else:
      self.hard = easy + hard

  def getEasyExplanation(self, use_class_expression):
    if use_class_expression is True:
      return [self.class_expression.easy] + self.easy
    else:
      return self.easy

  def getMediumExplanation(self, use_class_expression):
    if use_class_expression is True:
      return [self.class_expression.medium] + self.medium
    else:
      return self.medium

  def getHardExplanation(self, use_class_expression):
    if use_class_expression is True:
      return [self.class_expression.hard] + self.hard
    else:
      return self.hard