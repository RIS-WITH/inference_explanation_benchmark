class QuestionInstance:
    def __init__(self, name, fact, explanations, rule, classes_var, template_dict):
        self.name_ = name
        self.fact_ = fact
        self.explanations_ = explanations
        self.rule_ = rule
        self.classes_var_ = classes_var
        self.template_dict_ = template_dict
        
# ====================== canPerceive ===================

explanation_robot_capa = [
                           "pepper|Type|Robot",
                           "Robot|SubClassOf|Agent",
                           "pepper|hasCapability|pepper_capa"
                         ]

explanation_object_disp = [
                            "cube_1|Type|Cube",
                            "Cube|SubClassOf|Object",
                            "cube_1|hasDisposition|cube_1_disp"
                          ]

explanation_force = [
                    "realsense|Type|RGBCamera",
                    "RGBCamera|SubClassOf|Camera",
                    "pepper|hasComponent|realsense",
                    "realsense|hasMaximumDistanceRange|integer#40",
                    "cube_1|isAtDistance|integer#5",
                    "greaterThan(integer#40,integer#5)"
                    ]

# =============== Explanations why the class PerceivingDisposition is inferred =============
perceivable_easy = "PerceivingDisposition|EquivalentTo|"
perceivable_medium= "PerceivingDisposition|EquivalentTo|(isDispositionOf some (hasPart some QRCode))"
perceivable_hard = "PerceivingDisposition|EquivalentTo|(isDispositionOf some (hasPart some (QRCode and (isVisible value boolean#true)))"

explanations_perceivable_easy= ["cube_1_disp|Type|PerceivingDisposition"]

explanations_perceivable_medium = [
                                perceivable_medium,
                                "cube_1_disp|isDispositionOf|cube_1",
                                "cube_1|hasPart|qr_code_1",
                                "qr_code_1|Type|QRCode",
                                ]

explanations_perceivable_hard = [
                                perceivable_hard,
                                "cube_1_disp|isDispositionOf|cube_1",
                                "cube_1|hasPart|qr_code_1",
                                "qr_code_1|Type|QRCode",
                                "qr_code_1|isVisible|boolean#true",
                            ]

# =============== Explanations why the class PerceivingCapability is inferred =============
perceiving_easy = "PerceivingCapability|SubClassOf|"
perceiving_medium= "PerceivingCapability|EquivalentTo|(isCapabilityOf some (hasComponent some RGBCamera)"
perceiving_hard = "PerceivingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent some RGBCamera) and (hasComponent some QRCodeDetectionAlgo))"

explanations_perceiving_easy= ["pepper_capa|Type|PerceivingCapability"]

explanations_perceiving_medium = [
                                perceiving_medium,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|realsense",
                                "realsense|Type|RGBCamera"
                                ]

explanations_perceiving_hard = [
                                perceiving_hard,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|realsense",
                                "realsense|Type|RGBCamera",
                                "pepper|hasComponent|ar_track_alvar",
                                "ar_track_alvar|Type|QRCodeDetectionAlgo"
                                ]

# =============== Explanations why the property isApproachableBy exists =============
object_perceive_available_easy = "isVisibleBy" # cube isVisibleBy agent
object_perceive_available_medium = "(hasQRCode o isInFrontOf)|SubPropertyOf|isVisibleBy" # box hasQRCode qr_code_1 isInFrontOf agent
object_perceive_available_hard = "(hasQRCode o isInFrontOf o isCameraOf)|SubPropertyOf|isVisibleBy" # box hasQRCode qr_code_1 isInFrontOf camera isCameraOf pepper

explanations_object_perceive_easy = ["cube_1|isVisibleBy|pepper"]

explanations_object_perceive_medium = [
                                object_perceive_available_medium,
                                "cube_1|hasQRCode|qr_code_1",
                                "qr_code_1|isInFrontOf|pepper"
                                ]

explanations_object_perceive_hard = [
                                object_perceive_available_hard,
                                "cube_1|hasQRCode|qr_code_1",
                                "qr_code_1|isInFrontOf|realsense",
                                "realsense|isCameraOf|pepper",
                                ]

# Concatenate the explanations according to the complexity level (easy, medium, hard)
explanations_perceive_easy = explanation_robot_capa + explanations_perceiving_easy + explanation_object_disp + explanations_perceivable_easy + explanations_object_perceive_easy + explanation_force
explanations_perceive_medium = explanation_robot_capa + explanations_perceiving_medium + explanation_object_disp + explanations_perceivable_medium + explanations_object_perceive_medium + explanation_force
explanations_perceive_hard= explanation_robot_capa + explanations_perceiving_hard + explanation_object_disp + explanations_perceivable_hard + explanations_object_perceive_hard + explanation_force

print("easy : ", explanations_perceive_easy)
print("medium : ", explanations_perceive_medium)
print("hard : ", explanations_perceive_hard)

fact_perceive = "pepper|canPerceive|cube_1"

template_dict_perceive = {'pepper': '__var0__',  
                    'cube_1': '__var1__',
                    'cube_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'realsense' : '__var4__',
                    'qr_code_1' : '__var5__',
                    'table_1' : '__var6__',
                    'ar_track_alvar' : '__var7__',
                    'Robot': '__agent__',
                    'Cube': '__object__',
                    'RGBCamera': '__component__'
                    }

class_variables_final_perceive = { 
                    "__object__" : ["Box", "Cube", "Spoon", "Fork", "Pot", "Plate"],
                    "__agent__" :   ["Robot", "Pr2", "Pepper", "Tiago"],
                    "__component__" : ["RealsenseL515", "RGBCamera", "Webcam", "KinectV2", "RealsenseD435i"]
                     }

perceive_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), PerceivingCapability(?c), Object(?o), hasDisposition(?o, ?d), PerceivingDisposition(?d),\
                 isVisibleBy(?o,?a), Camera(?g), hasComponent(?a,?g), hasMaximumDistanceRange(?g,?w1), isAtDistance(?o,?w2), greaterThan(?w1,?w2) -> canPerceive(?a, ?o)."
               
question_perceive_easy = QuestionInstance(name="q_perceive_easy", fact=fact_perceive, explanations=explanations_perceive_easy,
                                       rule=perceive_rule, classes_var=class_variables_final_perceive, template_dict=template_dict_perceive)

question_perceive_medium= QuestionInstance(name="q_perceive_medium", fact=fact_perceive, explanations=explanations_perceive_medium,
                                       rule=perceive_rule, classes_var=class_variables_final_perceive, template_dict=template_dict_perceive)

question_perceive_hard = QuestionInstance(name="q_perceive_hard", fact=fact_perceive, explanations=explanations_perceive_hard,
                                       rule=perceive_rule, classes_var=class_variables_final_perceive, template_dict=template_dict_perceive)