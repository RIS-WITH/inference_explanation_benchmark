# =================== Q1 ====================

class QuestionInstance:
    def __init__(self, fact, explanations, rule, classes_var, template_dict):
        self.fact_ = fact
        self.explanations_ = explanations
        self.rule_ = rule
        self.classes_var_ = classes_var
        self.template_dict_ = template_dict
     
class_variables_q1 = {
                    "__support__" : ["Desk", "Table", "Cupboard"],
                    "__object__" : ["Mug", "Pen", "Book"],
                    "__agent__" : ["Robot", "Human", "Agent"]
                        }

template_dict_q1 = {
                'pepper': '__var0__',  
                'mug_3': '__var1__',
                'mug_3_disp': '__var2__',
                'pepper_capa': '__var3__',
                'table_1': '__var4__',
                'Robot': '__agent__',
                'Mug': '__object__',
                'Table': '__support__'
                }

init_fact_q1 = "pepper|canManipulate|mug_3"

init_explanations_q1 = [
                        "pepper|isA|Robot",
                        "pepper|hasCapability|pepper_capa",
                        "pepper_capa|isA|ManipulationCapability",
                        "mug_3|isA|Mug",
                        "mug_3|hasDisposition|mug_3_disp",
                        "mug_3_disp|isA|ManipulableDisposition",
                        "table_1|isA|Table",
                        "mug_3|isOn|table_1",
                        "pepper|isInFrontOf|table_1"
                        ]


rule_1 = "The used rule was : Robot(?r), hasCapability(?r, ?c), ManipulationCapability(?c), Mug(?o), hasDisposition(?o, ?d), ManipulableDisposition(?d), Support(?s), isOn(?o,?s), isInFrontOf(?r,?s) -> canManipulate(?r, ?o)."

question_1 = QuestionInstance(init_fact_q1, init_explanations_q1, rule_1, class_variables_q1, template_dict_q1)


# =================== Q2 ====================
class_variables_q2 = { 
                    "__object__" : ["Cup", "Pen", "Book"],
                    "__agent__" : ["Robot", "Humanoid", "Agent"]
                        }

template_dict_q2 = {'pepper': '__var0__',  
                    'mug_3': '__var1__',
                    'mug_3_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'Robot': '__agent__',
                    'Mug': '__object__',
                    }

init_fact_q2 = "pepper|canManipulate|mug_3"
init_explanations_q2 = [
                        "pepper|isA|Robot",
                        "pepper|hasCapability|pepper_capa",
                        "pepper_capa|isA|ManipulationCapability",
                        "mug_3|isA|Mug",
                        "mug_3|hasDisposition|mug_3_disp",
                        "mug_3_disp|isA|ManipulableDisposition",
                        ]

rule_2 = "The used rule was : Robot(?r), hasCapability(?r, ?c), ManipulationCapability(?c), Mug(?o), hasDisposition(?o, ?d), ManipulableDisposition(?d) -> canManipulate(?r, ?o)."

question_2 = QuestionInstance(init_fact_q2, init_explanations_q2, rule_2, class_variables_q2, template_dict_q2)

# =================== Q3 ====================
class_variables_q3 = { 
                    "__object__" : ["Cup", "Pen", "Book"],
                    "__agent__" : ["Robot", "Humanoid", "Agent"]
                        }

template_dict_q3 = {'pepper': '__var0__',  
                    'mug_3': '__var1__',
                    'mug_3_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'Robot': '__agent__',
                    'Mug': '__object__',
                    }

init_fact_q3 = "pepper|canGrasp|mug_3"
init_explanations_q3 = [
                        "pepper|isA|Robot",
                        "pepper|hasGraspingAffordance|mug_3",
                        "pepper|hasCapability|pepper_capa",
                        "pepper_capa|isA|ManipulationCapability",
                        "mug_3|isA|Mug",
                        "mug_3|hasDisposition|mug_3_disp",
                        "pepper|isInFrontOf|mug_3",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|isFree|boolean#true",
                        "pepper_left_gripper|hasWeightPayload|integer#4",
                        "mug_3|hasWeight|integer#1",
                        "integer#2|lessThan|integer#4"
                        ]

rule_3 = "The used rule was : Robot(?r), Object(?o), hasGraspingAffordance(?r, ?o), IsInFrontOf(?r,?o), Gripper(?g), hasComponent(?r,?g), isFree(?g, boolean#true), hasWeightPayload(?g,?w1), hasWeight(?o, ?w2), swrlb:lessThan(?w2,?w1) -> canGrasp(?r, ?o)."

question_3 = QuestionInstance(init_fact_q3, init_explanations_q3, rule_3, class_variables_q3, template_dict_q3)