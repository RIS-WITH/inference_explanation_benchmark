class QuestionInstance:
    def __init__(self, name, fact, explanations, rule, classes_var, template_dict):
        self.name_ = name
        self.fact_ = fact
        self.explanations_ = explanations
        self.rule_ = rule
        self.classes_var_ = classes_var
        self.template_dict_ = template_dict

# ====================== canPush ===================
explanation_robot_capa = [
                           "pepper|Type|Robot",
                           "Robot|SubClassOf|Agent",
                           "pepper|hasCapability|pepper_capa"
                         ]

explanation_object_disp = [
                            "chair_1|Type|Chair",
                            "Chair|SubClassOf|Object",
                            "chair_1|hasDisposition|chair_1_disp"
                          ]

explanation_force = [
                    "pepper_left_gripper|Type|Gripper",
                    "Gripper|SubClassOf|EndEffector",
                    "pepper|hasComponent|pepper_left_gripper",
                    "pepper_left_gripper|hasApplicableForce|integer#40",
                    "chair_1|requiresForce|integer#40"
                    ]

# =============== Explanations why the class PushableDisposition is inferred =============
pushable_easy = "PushableDisposition|SubClassOf|"
pushable_medium= "PushableDisposition|SubClassOf|(isDispositionOf some (hasPart some Wheel))"
pushable_hard = "PushableDisposition|SubClassOf|(isDispositionOf some (hasPart some (Wheel and (isBlocked value boolean#false)))"

explanations_pushable_easy= ["chair_1_disp|Type|PushableDisposition"]

explanations_pushable_medium = [
                                pushable_medium,
                                "chair_1_disp|isDispositionOf|chair_1",
                                "chair_1|hasPart|wheel_1",
                                "wheel_1|Type|Wheel",
                                ]

explanations_pushable_hard = [
                                pushable_hard,
                                "chair_1_disp|isDispositionOf|chair_1",
                                "chair_1|hasPart|wheel_1",
                                "wheel_1|Type|Wheel",
                                "wheel_1|isBlocked|boolean#false"
                            ]

# =============== Explanations why the class PushingCapability is inferred =============
pushing_easy = "PushingCapability|SubClassOf|"
pushing_medium= "PushingCapability|SubClassOf|(isCapabilityOf some (hasGripper min 1 Gripper)"
pushing_hard = "PushingCapability|SubClassOf|(isCapabilityOf some (hasGripper min 1 (Gripper and RigidEndEffector))"

explanations_pushing_easy= ["pepper_capa|Type|PushingCapability"]

explanations_pushing_medium = [
                                pushing_medium,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasGripper|pepper_left_gripper",
                                "pepper_left_gripper|Type|Gripper"
                                ]

explanations_pushing_hard = [
                                pushing_hard,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasGripper|pepper_left_gripper",
                                "pepper_left_gripper|Type|Gripper",
                                "pepper_left_gripper|Type|RigidEndEffector"
                                ]

# =============== Explanations why the property isApproachableBy exists =============
object_push_available_easy = "isApproachableBy" # chair isApproachableBy agent
object_push_available_medium = "(isSupportedBy o isNear)|SubPropertyOf|isApproachableBy" # box isSupportedBy table isNear agent
object_push_available_hard = "(isSupportedBy o isNear)|SubPropertyOf|isApproachableBy, isFacing|SubPropertyOf|IsNear" # box isSupportedBy table isFacing agent

explanations_object_push_easy = ["chair_1|isApproachableBy|pepper"]

explanations_object_push_medium = [
                                "chair_1|isApproachableBy|pepper",
                                object_push_available_medium,
                                "chair_1|isSupportedBy|table_1",
                                "table_1|isNear|pepper"
                                ]

explanations_object_push_hard = [
                                "chair_1|isApproachableBy|pepper",
                                object_push_available_hard,
                                "chair_1|isSupportedBy|table_1",
                                "table_1|isFacing|pepper"
                                ]

# Concatenate the explanations according to the complexity level (easy, medium, hard)
explanations_push_easy = explanation_robot_capa + explanations_pushing_easy + explanation_object_disp + explanations_pushable_easy + explanations_object_push_easy + explanation_force
explanations_push_medium = explanation_robot_capa + explanations_pushing_medium + explanation_object_disp + explanations_pushable_medium + explanations_object_push_medium + explanation_force
explanations_push_hard= explanation_robot_capa + explanations_pushing_hard + explanation_object_disp + explanations_pushable_hard + explanations_object_push_hard + explanation_force

print("easy : ", explanations_push_easy)
print("medium : ", explanations_push_medium)
print("hard : ", explanations_push_hard)

fact_push = "pepper|canPush|chair_1"

template_dict_push = {'pepper': '__var0__',  
                    'chair_1': '__var1__',
                    'chair_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'wheel_1' : '__var5__',
                    'table_1' : '__var6__',
                    'Robot': '__agent__',
                    'Chair': '__object__',
                    'Gripper': '__component__'
                    }

class_variables_final_push = { 
                    "__object__" : ["ToyWagon", "Stool", "Chair", "ShoppingCart"],
                    "__agent__" :   ["Robot", "Pr2", "Pepper", "Tiago"],
                    "__component__" :   ["Gripper", "Hand", "Claw"]
                     }

push_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), PushingCapability(?c), Object(?o), hasDisposition(?o, ?d), PushableDisposition(?d),\
               isApproachableBy(?o,?a), EndEffector(?g), hasComponent(?a,?g), hasApplicableForce(?g,?w1), requiresForce(?o,?w2), equal(?w2,?w1) -> canPush(?a, ?o)."
               
question_push_easy = QuestionInstance(name="question_push_easy", fact=fact_push, explanations=explanations_push_easy,
                                       rule=push_rule, classes_var=class_variables_final_push, template_dict=template_dict_push)

question_push_medium= QuestionInstance(name="question_push_medium", fact=fact_push, explanations=explanations_push_medium,
                                       rule=push_rule, classes_var=class_variables_final_push, template_dict=template_dict_push)

question_push_hard = QuestionInstance(name="question_push_hard", fact=fact_push, explanations=explanations_push_hard,
                                       rule=push_rule, classes_var=class_variables_final_push, template_dict=template_dict_push)