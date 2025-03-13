from data_elements.questions import QuestionInstance
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
                    "realsense|hasMaximumDistanceRange|integer#2",
                    "cube_1|isAtDistance|integer#1",
                    "greaterThan(integer#2,integer#1)"
                    ]

# =============== Explanations why the class PerceivingDisposition is inferred =============
perceivable_easy = "PerceivingDisposition|EquivalentTo|(isDispositionOf some (hasPart some ScannablePart))"
perceivable_medium= "PerceivingDisposition|EquivalentTo|(isDispositionOf some (hasPart some (ScannablePart and (isRegistered value boolean#true)))"
perceivable_hard = "PerceivingDisposition|EquivalentTo|(isDispositionOf some (hasPart some (ScannablePart and (isRegistered value boolean#true) and (isVisible value boolean#true)))"

explanations_perceivable_easy= [
                                perceivable_easy,
                                "cube_1_disp|isDispositionOf|cube_1",
                                "cube_1|hasPart|qr_code_1",
                                "qr_code_1|Type|QRCode",
                                "QRCode|SubClassOf|ScannablePart"
                                ]

explanations_perceivable_medium = [
                                perceivable_medium,
                                "cube_1_disp|isDispositionOf|cube_1",
                                "cube_1|hasPart|qr_code_1",
                                "qr_code_1|Type|QRCode",
                                "QRCode|SubClassOf|ScannablePart",
                                "qr_code_1|isRegistered|boolean#true"
                                ]

explanations_perceivable_hard = [
                                perceivable_hard,
                                "cube_1_disp|isDispositionOf|cube_1",
                                "cube_1|hasPart|qr_code_1",
                                "qr_code_1|Type|QRCode",
                                "QRCode|SubClassOf|ScannablePart",
                                "qr_code_1|isRegistered|boolean#true",
                                "qr_code_1|isVisible|boolean#true"
                            ]

# =============== Explanations why the class PerceivingCapability is inferred =============
perceiving_easy = "PerceivingCapability|SubClassOf|(isCapabilityOf some (hasComponent some Camera)"
perceiving_medium= "PerceivingCapability|EquivalentTo|(isCapabilityOf some (hasComponent some (Camera and (isActive value boolean#true))"
perceiving_hard = "PerceivingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent some (Camera and (isActive value boolean#true)) and (hasComponent some ScanCodeDetectionAlgo))"

explanations_perceiving_easy= [
                                perceiving_easy,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|realsense",
                                "realsense|Type|RGBCamera",
                                "RGBCamera|SubClassOf|Camera"
                                ]

explanations_perceiving_medium = [
                                perceiving_medium,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|realsense",
                                "realsense|Type|RGBCamera",
                                "RGBCamera|SubClassOf|Camera",
                                "realsense|isActive|boolean#true"
                                ]

explanations_perceiving_hard = [
                                perceiving_hard,
                                "pepper_capa|isCapabilityOf|pepper",
                                "pepper|hasComponent|realsense",
                                "realsense|Type|RGBCamera",
                                "RGBCamera|SubClassOf|Camera",
                                "realsense|isActive|boolean#true",
                                "pepper|hasComponent|ar_track_alvar",
                                "ar_track_alvar|Type|ScanCodeDetectionAlgo"
                                ]

# =============== Explanations why the property isApproachableBy exists =============
object_perceive_available_easy = "isVisibleBy" # cube isVisibleBy agent
object_perceive_available_medium = "(hasScannableCode o isInFrontOf)|SubPropertyOf|isVisibleBy" # box hasScannableCode qr_code_1 isInFrontOf agent
object_perceive_available_hard = "(hasScannableCode o isInFrontOf o isCameraOf)|SubPropertyOf|isVisibleBy" # box hasScannableCode qr_code_1 isInFrontOf camera isCameraOf pepper

explanations_object_perceive_easy = ["cube_1|isVisibleBy|pepper"]

explanations_object_perceive_medium = [
                                object_perceive_available_medium,
                                "cube_1|hasScannableCode|qr_code_1",
                                "qr_code_1|isInFrontOf|pepper"
                                ]

explanations_object_perceive_hard = [
                                object_perceive_available_hard,
                                "cube_1|hasScannableCode|qr_code_1",
                                "qr_code_1|isInFrontOf|realsense",
                                "realsense|isCameraOf|pepper",
                                ]

# Concatenate the explanations according to the complexity level (easy, medium, hard)
explanations_perceive_easy = explanation_robot_capa + explanations_perceiving_easy + explanation_object_disp + explanations_perceivable_easy + explanations_object_perceive_easy + explanation_force
explanations_perceive_medium = explanation_robot_capa + explanations_perceiving_medium + explanation_object_disp + explanations_perceivable_medium + explanations_object_perceive_medium + explanation_force
explanations_perceive_hard= explanation_robot_capa + explanations_perceiving_hard + explanation_object_disp + explanations_perceivable_hard + explanations_object_perceive_hard + explanation_force

# print("easy : ", explanations_perceive_easy)
# print("medium : ", explanations_perceive_medium)
# print("hard : ", explanations_perceive_hard)

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
                    'RGBCamera': '__component__',
                    'Cube': '__object__',
                    'QRCode': '__part__'
                    }

new_objects = ["Book", "Box", "Luggage", "Appliance", "Cube", "Table"]
class VariableConcept:
  def __init__(self, concept, label):
    self.concept_ = concept
    self.label_ = label

object_list = [
              VariableConcept('Book', 'book'), 
              VariableConcept('Box', 'box'), 
              VariableConcept('Luggage', 'luggage'), 
              VariableConcept('Appliance', 'appliance'), 
              VariableConcept('Cube', 'cube'),
              VariableConcept('Table', 'table'),
              VariableConcept('Plate', 'plate')
              ]

part_list = [
              VariableConcept('QRCode', 'qr code'), 
              VariableConcept('2DBarcode', '2d barcode'), 
              VariableConcept('QRTag', 'qr tag'), 
              VariableConcept('ScanTag', 'scan tag')
              ]

agent_list = [
              VariableConcept('Robot', 'robot'), 
              VariableConcept('Pr2', 'pr2'), 
              VariableConcept('Pepper', 'pepper'), 
              VariableConcept('Tiago', 'tiago')
              ]

component_list = [
              VariableConcept('RealsenseL515', 'realsense l515'), 
              VariableConcept('RGBCamera', 'rgb camera'), 
              VariableConcept('Webcam', 'webcam'),
              VariableConcept('KinectV2', 'kinect v2'),
              VariableConcept('RealsenseD435i', 'realsense d435i')
              ]

class_variables_final_perceive = { 
                    "__object__" :  object_list,
                    "__part__" :    part_list,
                    "__agent__" :   agent_list,
                    "__component__" : component_list
                     }

perceive_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), PerceivingCapability(?c), Object(?o), hasDisposition(?o, ?d), PerceivingDisposition(?d),\
                 isVisibleBy(?o,?a), Camera(?g), hasComponent(?a,?g), hasMaximumDistanceRange(?g,?w1), isAtDistance(?o,?w2), greaterThan(?w1,?w2) -> canPerceive(?a, ?o)."

concepts_rule = ['perceiving', 'perceivable', 'visible', 'camera range', 'object_distance', 'can perceive']

concept_easy = {
                'rule' : ['can perceive', '__robot__', '__camera__', '__object__', '__scannable_code__'],
                'disp' : ['perceivable disposition', "1scannable_part"], 
                'capa': ['perceiving capability', '1camera'], 
                'property' : ['object_visible_by_robot'],
                'constraint' : ['camera range', 'object_distance']
                }


concept_medium = {
                'rule' : ['can perceive', '__robot__', '__camera__', '__object__', '__scannable_code__'],
                'disp' : ['perceivable disposition',"1scannable_part", "scannable_part_registered"], 
                'capa': ['perceiving capability', '1camera', 'camera_active'], 
                'property' : ['object_visible_by_robot', 'object_has_scannable_code', 'code_in_front_of_camera'],
                'constraint' : ['camera range', 'object_distance']
                }

concept_hard = {
                'rule' : ['can perceive', '__robot__', '__camera__', '__object__', '__scannable_code__'],
                'disp' : ['perceivable disposition', "1scannable_part", "scannable_part_registered", 'scannable_part_visible'],
                'capa': ['perceiving capability', '1camera', 'camera_active', 'scan_detection_algo' ], 
                'property' : ['object_visible_by_robot', 'object_has_scannable_code', 'code_in_front_of_camera', 'camera_of_robot'],
                'constraint' : ['camera range', 'object_distance']
                }

#easy
# "concepts" : [
#   "can perceive", 
#   "perceivable",
#   "perceiving",
#   "object_visible_by_robot", 
#   "camera range", "object_distance"  
# ]

# medium
# "concepts" : [
#   "can perceive", 
#   "perceivable", "scannable_part_registered",
#   "perceiving","camera_active",
#   "object_visible_by_robot", "object_has_scannable_code", "code_in_front_of_camera",
#   "camera range", "object_distance"    
# ]

# hard
# "concepts" : [
#   "can perceive", 
#   "perceivable", "scannable_part_registered", "scannable_part_visible",
#   "perceiving","camera_active", "scan_detection_algo",
#   "object_visible_by_robot", "object_has_scannable_code", "code_in_front_of_camera", "camera_of_robot",
#   "camera range", "object_distance"   
# ]

# gt_perceive_easy = "The __agent__ can perceive the __object__ because on one hand it has the perceiving capability through its __component__ which is a camera. \
#                  On the other hand, the __object__ has the disposition of being perceivable because it has a __part__, a scannable code. \
#                  Moreover the __object__ is visible by the __agent__."

# gt_perceive_medium = "The __agent__ can perceive the __object__ because on one hand it has the perceiving capability through its __component__, \
#                 a camera, which is active. On the other hand, the __object__ has the disposition of being perceivable because it has a __part__, a scannable code\
#                 which is registered. Moreover the __object__ is visible by the  because it has a scannable qr code which is in front of the __agent__."
                 
# gt_perceive_hard = "The __agent__ can perceive the __object__ because on one hand it has the perceiving capability through its __component__, \
#                 a camera, which is active, and also being equipped with a detection algorithm for scannable code. On the other hand, the __object__ has the \
#                 disposition of being perceivable because it has a __part__, a scannable code, which is registered and visible.\
#                 Moreover the __object__ is visible by the  because it has a scannable qr code which is in front of the camera of the __agent__."
                            
question_perceive_easy = QuestionInstance(name="q_perceive_easy", fact=fact_perceive, explanations=explanations_perceive_easy, rule=perceive_rule, 
                                          classes_var=class_variables_final_perceive, template_dict=template_dict_perceive, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)

question_perceive_medium= QuestionInstance(name="q_perceive_medium", fact=fact_perceive, explanations=explanations_perceive_medium, rule=perceive_rule,
                                           classes_var=class_variables_final_perceive, template_dict=template_dict_perceive, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)

question_perceive_hard = QuestionInstance(name="q_perceive_hard", fact=fact_perceive, explanations=explanations_perceive_hard, rule=perceive_rule, 
                                          classes_var=class_variables_final_perceive, template_dict=template_dict_perceive, ground_truth_sentence=None,
                                      concept_rule=concepts_rule)
