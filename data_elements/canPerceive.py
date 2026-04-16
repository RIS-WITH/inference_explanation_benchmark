from data_elements.QuestionManager import QuestionRule, QuestionManager
from data_elements.VariableManager import VariableManager
from data_elements.Explanation import AffordanceBase, ClassExpression, ClassExpressionExplanation

# ====================== Rule ===================

perceive_rule = QuestionRule(property = "canPerceive",
                             rule = "Agent(?a), hasCapability(?a, ?c), PerceivingCapability(?c), Object(?o),\
                                     hasDisposition(?o, ?d), PerceivingDisposition(?d),\
                                     isVisibleBy(?o,?a), Camera(?g), hasComponent(?a,?g),\
                                     hasMaximumDistanceRange(?g,?w1), isAtDistance(?o,?w2), greaterThan(?w1,?w2) \
                                     -> canPerceive(?a, ?o)",
                             concepts = ['perceiving', 'perceivable', 'visible', 'camera range', 'object_distance', 'can perceive'])

# ====================== Variables ===================

variable_manager = VariableManager()
variable_manager.addClassVariable('__Object__',
                                  {'Book' : 'book',
                                   'Box' : 'box',
                                   'Luggage' : 'luggage',
                                   'Appliance' : 'appliance',
                                   'Cube' : 'cube',
                                   'Table' : 'table',
                                   'Plate' : 'plate'})

# ====================== Affordance ===================

affordance = AffordanceBase(capa=None, # Use the default capability
                            disp=None, # Use the default disposition
                            match=[
                                  "__camera__|Type|__Camera__",
                                  "__Camera__|SubClassOf|Camera",
                                  "__agent__|hasComponent|__camera__",
                                  "__camera__|hasMaximumDistanceRange|integer#2",
                                  "__object__|isAtDistance|integer#1",
                                  "greaterThan(integer#2,integer#1)"
                                  ])

# =============== Disposition explanation =============
disposition_expression = ClassExpression(easy= "PerceivingDisposition|EquivalentTo|(isDispositionOf some (hasPart some ScannablePart))",
                                         medium= "PerceivingDisposition|EquivalentTo|(isDispositionOf some (hasPart some (ScannablePart and (isRegistered value boolean#true)))",
                                         hard= "PerceivingDisposition|EquivalentTo|(isDispositionOf some (hasPart some (ScannablePart and (isRegistered value boolean#true) and (isVisible value boolean#true)))")

diposition_explanation = ClassExpressionExplanation(disposition_expression,
                                                    easy=["__object_disp__|isDispositionOf|__object__",
                                                          "__object__|hasPart|__scannable_part__",
                                                          "__scannable_part__|Type|__ScanablePart__",
                                                          "__ScanablePart__|SubClassOf|ScannablePart"],
                                                    medium=["__scannable_part__|isRegistered|boolean#true"],
                                                    hard=["__scannable_part__|isVisible|boolean#true"],
                                                    concatenate=True)

# =============== Capability Explanation =============
capability_expression = ClassExpression(easy= "PerceivingCapability|EquivalentTo|(isCapabilityOf some (hasComponent some Camera)",
                                        medium= "PerceivingCapability|EquivalentTo|(isCapabilityOf some (hasComponent some (Camera and (isActive value boolean#true))",
                                        hard= "PerceivingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent some (Camera and (isActive value boolean#true)) and (hasComponent some ScanCodeDetectionAlgo))")

capability_explanation = ClassExpressionExplanation(capability_expression,
                                                    easy=["__agent_capa__|isCapabilityOf|__agent__",
                                                          "__agent__|hasComponent|__camera__",
                                                          "__camera__|Type|__Camera__",
                                                          "__Camera__|SubClassOf|Camera"],
                                                    medium=["__camera__|isActive|boolean#true"],
                                                    hard=["__agent__|hasComponent|__algo__",
                                                          "__algo__|Type|ScanCodeDetectionAlgo"],
                                                    concatenate=True)

# =============== Property Explanation =============
property_expression = ClassExpression(easy= "", # cube isVisibleBy agent
                                      medium= "(hasScannableCode o isInFrontOf)|SubPropertyOf|isVisibleBy", # box hasScannableCode __scannable_part__ isInFrontOf agent
                                      hard= "(hasScannableCode o isInFrontOf o isCameraOf)|SubPropertyOf|isVisibleBy") # box hasScannableCode __scannable_part__ isInFrontOf camera isCameraOf __agent__

property_explanation = ClassExpressionExplanation(property_expression,
                                                  easy= ["__object__|isVisibleBy|__agent__"],
                                                  medium= [],
                                                  hard=[],
                                                  concatenate = True)

property_explanation.medium = ["__object__|hasScannableCode|__scannable_part__",
                               "__scannable_part__|isInFrontOf|__agent__"]

property_explanation.hard = ["__object__|hasScannableCode|__scannable_part__",
                             "__scannable_part__|isInFrontOf|__camera__",
                             "__camera__|isCameraOf|__agent__"]

# =============== QuestionManager =============

perceive_manager = QuestionManager(perceive_rule,
                                   variable_manager,
                                   affordance,
                                   capability_explanation,
                                   diposition_explanation,
                                   property_explanation)

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

# gt_perceive_easy = "The __Agent__ can perceive the __Object__ because on one hand it has the perceiving capability through its __Camera__ which is a camera. \
#                  On the other hand, the __Object__ has the disposition of being perceivable because it has a __ScanablePart__, a scannable code. \
#                  Moreover the __Object__ is visible by the __Agent__."

# gt_perceive_medium = "The __Agent__ can perceive the __Object__ because on one hand it has the perceiving capability through its __Camera__, \
#                 a camera, which is active. On the other hand, the __Object__ has the disposition of being perceivable because it has a __ScanablePart__, a scannable code\
#                 which is registered. Moreover the __Object__ is visible by the  because it has a scannable qr code which is in front of the __Agent__."
                 
# gt_perceive_hard = "The __Agent__ can perceive the __Object__ because on one hand it has the perceiving capability through its __Camera__, \
#                 a camera, which is active, and also being equipped with a detection algorithm for scannable code. On the other hand, the __Object__ has the \
#                 disposition of being perceivable because it has a __ScanablePart__, a scannable code, which is registered and visible.\
#                 Moreover the __Object__ is visible by the  because it has a scannable qr code which is in front of the camera of the __Agent__."