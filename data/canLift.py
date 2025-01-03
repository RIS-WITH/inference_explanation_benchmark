class QuestionInstance:
    def __init__(self, name, fact, explanations, rule, classes_var, template_dict):
        self.name_ = name
        self.fact_ = fact
        self.explanations_ = explanations
        self.rule_ = rule
        self.classes_var_ = classes_var
        self.template_dict_ = template_dict

# ====================== canLift ===================

explanation_robot_capa = [
                           "pepper|Type|Robot",
                           "Robot|SubClassOf|Agent",
                           "pepper|hasCapability|pepper_capa"
                         ]

explanation_object_disp = [
                            "box_2|Type|Box",
                            "Box|SubClassOf|Object",
                            "box_2|hasDisposition|box_2_disp"
                          ]

explanation_weight = [
                    "pepper_left_gripper|Type|Gripper",
                    "Gripper|SubClassOf|EndEffector",
                    "pepper|hasComponent|pepper_left_gripper",
                    "pepper_left_gripper|hasWeightLimit|integer#40",
                    "box_2|hasWeight|integer#20"
                    ]

# =============== Explanations why the class LiftableDisposition is inferred =============
liftable_easy = "LiftableDisposition|SubClassOf|"
liftable_medium= "LiftableDisposition|SubClassOf|(isDispositionOf some (hasPart min 2 GraspablePart))"
liftable_hard = "LiftableDisposition|SubClassOf|(isDispositionOf some (hasPart min 2 (GraspablePart and (isAttached value boolean#false)))"

explanations_liftable_easy= ["box_2_disp|Type|LiftableDisposition"]

explanations_liftable_medium = [
                                liftable_medium,
                                "box_2_disp|isDispositionOf|box_2",
                                "box_2|hasPart|handle_1",
                                "handle_1|Type|GraspablePart",
                                "box_2|hasPart|handle_2",
                                "handle_2|Type|GraspablePart"
                                ]

explanations_liftable_hard = [
                                liftable_hard,
                                "box_2_disp|isDispositionOf|box_2",
                                "box_2|hasPart|handle_1",
                                "handle_1|Type|GraspablePart",
                                "handle_1|isAttached|boolean#false",
                                "box_2|hasPart|handle_2",
                                "handle_2|Type|GraspablePart",
                                "handle_2|isAttached|boolean#false"
                            ]

# =============== Explanations why the class LiftingCapability is inferred =============
lifting_easy = "LiftingCapability|SubClassOf|"
lifting_medium= "LiftingCapability|SubClassOf|(isCapabilityOf some (hasComponent min 2 Gripper)"
lifting_hard = "LiftingCapability|SubClassOf|(isCapabilityOf some ((hasComponent min 2 Gripper) and (hasSomethingInHands value boolean#false))"

explanations_lifting_easy= ["pepper_capa|Type|LiftingCapability"]

explanations_lifting_medium = [
                                lifting_medium,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|Gripper",
                                "pepper|hasComponent|pepper_right_gripper",
                                "pepper_right_gripper|Type|Gripper",
                                ]

explanations_lifting_hard = [
                                lifting_hard,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|Gripper",
                                "pepper|hasComponent|pepper_right_gripper",
                                "pepper_right_gripper|Type|Gripper",
                                "pepper|hasSomethingInHands|boolean#false"
                                ]

# =============== Explanations why the property isTouchableBy exists =============
object_lift_available_easy = "isTouchableBy" # box isTouchableBy agent
object_lift_available_medium = "(isOnTouchableSupport o isNear)|SubPropertyOf|isTouchableBy" # box isOnTouchableSupport table isNear agent
object_lift_available_hard = "(isOnTouchableSupport o isNear)|SubPropertyOf|isTouchableBy, isFacing|SubPropertyOf|IsNear" # box isOnTouchableSupport table isFacing agent

explanations_object_lift_easy = ["box_2|isTouchableBy|pepper"]

explanations_object_lift_medium = [
                                "box_2|isTouchableBy|pepper",
                                object_lift_available_medium,
                                "box_2|isOnTouchableSupport|table_1",
                                "table_1|isNear|pepper"
                                ]

explanations_object_lift_hard = [
                                "box_2|isTouchableBy|pepper",
                                object_lift_available_hard,
                                "box_2|isOnTouchableSupport|table_1",
                                "table_1|isFacing|pepper"
                                ]

# Concatenate the explanations according to the complexity level (easy, medium, hard)
explanations_lift_easy = explanation_robot_capa + explanations_lifting_easy + explanation_object_disp + explanations_liftable_easy + explanations_object_lift_easy + explanation_weight
explanations_lift_medium = explanation_robot_capa + explanations_lifting_medium + explanation_object_disp + explanations_liftable_medium + explanations_object_lift_medium + explanation_weight
explanations_lift_hard= explanation_robot_capa + explanations_lifting_hard + explanation_object_disp + explanations_liftable_hard + explanations_object_lift_hard + explanation_weight

print("easy : ", explanations_lift_easy)
print("medium : ", explanations_lift_medium)
print("hard : ", explanations_lift_hard)

fact_lift = "pepper|canLift|box_2"

template_dict_lift = {'pepper': '__var0__',  
                    'box_2': '__var1__',
                    'box_2_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'pepper_right_gripper' : '__var4__',
                    'handle_1' : '__var5__',
                    'handle_2' : '__var5__',
                    'table_1' : '__var6__',
                    'Robot': '__agent__',
                    'Box': '__object__',
                    'Gripper': '__component__'
                    }

class_variables_final_lift = { 
                    "__object__" : ["StorageBox", "Stool", "Chair", "Bookshelf"],
                    "__agent__" :   ["Robot", "Pr2", "Pepper", "Tiago"],
                    "__component__" :   ["Gripper", "Hand", "Claw"]
                     }

lift_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), LiftingCapability(?c), Object(?o), hasDisposition(?o, ?d), LiftableDisposition(?d),\
               isTouchableBy(?o,?a), EndEffector(?g), hasComponent(?a,?g), hasWeightLimit(?g,?w1), hasWeight(?o,?w2), lesserThan(?w2,?w1) -> canLift(?a, ?o)."
               
question_lift_easy = QuestionInstance(name="question_lift_easy", fact=fact_lift, explanations=explanations_lift_easy,
                                       rule=lift_rule, classes_var=class_variables_final_lift, template_dict=template_dict_lift)

question_lift_medium= QuestionInstance(name="question_lift_medium", fact=fact_lift, explanations=explanations_lift_medium,
                                       rule=lift_rule, classes_var=class_variables_final_lift, template_dict=template_dict_lift)

question_lift_hard = QuestionInstance(name="question_lift_hard", fact=fact_lift, explanations=explanations_lift_hard,
                                       rule=lift_rule, classes_var=class_variables_final_lift, template_dict=template_dict_lift)