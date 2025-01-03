class QuestionInstance:
    def __init__(self, name, fact, explanations, rule, classes_var, template_dict):
        self.name_ = name
        self.fact_ = fact
        self.explanations_ = explanations
        self.rule_ = rule
        self.classes_var_ = classes_var
        self.template_dict_ = template_dict

# ====================== canGrasp ===================

explanation_robot_capa = [
                           "pepper|Type|Robot",
                           "Robot|SubClassOf|Agent",
                           "pepper|hasCapability|pepper_capa"
                         ]

explanation_object_disp = [
                            "mug_3|Type|Mug",
                            "Mug|SubClassOf|Object",
                            "mug_3|hasDisposition|mug_3_disp"
                          ]

explanation_width = [
                    "pepper_left_gripper|Type|Gripper",
                    "Gripper|SubClassOf|EndEffector",
                    "pepper|hasComponent|pepper_left_gripper",
                    "pepper_left_gripper|hasOpeningWidth|integer#20",
                    "mug_3|hasWidth|integer#10"
                    ]

# =============== Explanations why the class GraspableDisposition is inferred =============
graspable_easy = "GraspableDisposition|SubClassOf|"
graspable_medium= "GraspableDisposition|SubClassOf|(isDispositionOf some (hasPart some Handle))"
graspable_hard = "GraspableDisposition|SubClassOf|(isDispositionOf some (hasPart some (Handle and (IsInUse value boolean#false)))"

explanations_graspable_easy= ["mug_3_disp|Type|GraspableDisposition"]

explanations_graspable_medium = [
                                graspable_medium,
                                "mug_3_disp|isDispositionOf|mug_3",
                                "mug_3|hasPart|handle_3",
                                "handle_3|Type|Handle",
                                ]

explanations_graspable_hard = [
                                graspable_hard,
                                "mug_3_disp|isDispositionOf|mug_3",
                                "mug_3|hasPart|handle_3",
                                "handle_3|Type|Handle",
                                "handle_3|isInUse|boolean#false"
                                ]

# =============== Explanations why the class GraspingCapability is inferred =============
grasping_easy = "GraspingCapability|SubClassOf|"
grasping_medium= "GraspingCapability|SubClassOf|(isCapabilityOf some (hasComponent some Gripper)"
grasping_hard = "GraspingCapability|SubClassOf|(isCapabilityOf some (hasComponent some (Gripper and (holdsSomething value boolean#false))"

explanations_grasping_easy= ["pepper_capa|Type|GraspingCapability"]

explanations_grasping_medium = [
                                grasping_medium,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|Gripper",
                                ]

explanations_grasping_hard = [
                                grasping_hard,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|pepper_left_gripper",
                                "pepper_left_gripper|Type|Gripper",
                                "pepper_left_gripper|holdsSomething|boolean#false"
                                ]

# =============== Explanations why the property isReachable exists =============
object_grasp_available_easy = "isReachableBy" # mug isReachableBy agent
object_grasp_available_medium = "(isContainedIn o isNear)|SubPropertyOf|isReachableBy" # mug isContainedIn cupboard isNear agent
object_grasp_available_hard = "(isContainedIn o isNear)|SubPropertyOf|isReachableBy, isInFrontOf|SubPropertyOf|IsNear" # mug isContainedIn cupboard isNear agent

explanations_object_grasp_easy = ["mug_3|isReachableBy|pepper"]

explanations_object_grasp_medium = [
                                "mug_3|isReachableBy|pepper",
                                object_grasp_available_medium,
                                "mug_3|isContainedIn|cupboard_1",
                                "cupboard_1|isNear|pepper"
                                ]

explanations_object_grasp_hard = [
                                "mug_3|isReachableBy|pepper",
                                object_grasp_available_hard,
                                "mug_3|isContainedIn|cupboard_1",
                                "cupboard_1|isInFrontOf|pepper"
                                ]

# Concatenate the explanations according to the complexity level (easy, medium, hard)
explanations_grasp_easy = explanation_robot_capa + explanations_grasping_easy + explanation_object_disp + explanations_graspable_easy + explanations_object_grasp_easy + explanation_width
explanations_grasp_medium = explanation_robot_capa + explanations_grasping_medium + explanation_object_disp + explanations_graspable_medium + explanations_object_grasp_medium + explanation_width
explanations_grasp_hard= explanation_robot_capa + explanations_grasping_hard + explanation_object_disp + explanations_graspable_hard + explanations_object_grasp_hard + explanation_width

print("easy : ", explanations_grasp_easy)
print("medium : ", explanations_grasp_medium)
print("hard : ", explanations_grasp_hard)

fact_grasp = "pepper|canGrasp|mug_3"

template_dict_grasp = {'pepper': '__var0__',  
                            'mug_3': '__var1__',
                            'mug_3_disp': '__var2__',
                            'pepper_capa': '__var3__',
                            'pepper_left_gripper' : '__var4__',
                            'handle_3' : '__var5__',
                            'cupboard_1' : '__var6__',
                            'Robot': '__agent__',
                            'Mug': '__object__',
                            'Gripper': '__component__'
                            }

class_variables_final_grasp = { 
                    "__object__" : ["Mug", "Cup", "Knife", "Fork", "Pot"],
                    "__agent__" :   ["Robot", "Pr2", "Pepper", "Tiago"],
                    "__component__" :   ["Gripper", "Hand", "Claw"]
                     }

grasp_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), GraspingCapability(?c), Object(?o), hasDisposition(?o, ?d), GraspableDisposition(?d),\
               isReachableBy(?o,?a), EndEffector(?g), hasComponent(?a,?g), hasOpeningWidth(?g,?w1), hasWidth(?o,?w2), greaterThan(?w1,?w2) -> canGrasp(?a, ?o)."
               
question_grasp_easy = QuestionInstance(name="question_grasp_easy", fact=fact_grasp, explanations=explanations_grasp_easy,
                                       rule=grasp_rule, classes_var=class_variables_final_grasp, template_dict=template_dict_grasp)

question_grasp_medium= QuestionInstance(name="question_grasp_medium", fact=fact_grasp, explanations=explanations_grasp_medium,
                                       rule=grasp_rule, classes_var=class_variables_final_grasp, template_dict=template_dict_grasp)

question_grasp_hard = QuestionInstance(name="question_grasp_hard", fact=fact_grasp, explanations=explanations_grasp_hard,
                                       rule=grasp_rule, classes_var=class_variables_final_grasp, template_dict=template_dict_grasp)