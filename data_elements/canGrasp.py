from data_elements.QuestionManager import QuestionRule, QuestionManager
from data_elements.VariableManager import VariableManager
from data_elements.Explanation import AffordanceBase, ClassExpression, ClassExpressionExplanation

# ====================== Rule ===================

grasp_rule = QuestionRule(property = "canGrasp",
                          rule = "Agent(?a), hasCapability(?a, ?c), GraspingCapability(?c),\
                                  Object(?o), hasDisposition(?o, ?d), GraspableDisposition(?d),\
                                  isReachableBy(?o,?a), EndEffector(?g), hasComponent(?a,?g),\
                                  hasOpeningWidth(?g,?w1), hasHoldingPartWidth(?o,?w2), greaterThan(?w1,?w2)\
                                  -> canGrasp(?a, ?o)",
                          concepts = ['grasping', 'graspable', 'reach', 'opening', 'object_width', 'can grasp'])

# ====================== Variables ===================

variable_manager = VariableManager()
variable_manager.addClassVariable('__Object__',
                                  {'Mug' : 'mug',
                                   'Hammer' : 'hammer',
                                   'ToyBucket' : 'toy bucket',
                                   'Suitcase' : 'suitcase',
                                   'Shovel' : 'shovel',
                                   'CookingPot' : 'cooking pot',
                                   'Lunchbox' : 'lunchbox'})

# ====================== Affordance ===================

affordance = AffordanceBase(capa=None, # Use the default capability
                            disp=None, # Use the default disposition
                            match=[
                                  "__gripper__|Type|Gripper",
                                  "Gripper|SubClassOf|EndEffector",
                                  "__agent__|hasComponent|__gripper__",
                                  "__gripper__|hasOpeningWidth|integer#2",
                                  "__object__|hasHoldingPartWidth|integer#1",
                                  "greaterThan(integer#2,integer#1)"
                                  ])

# =============== Disposition Explanation =============
disposition_expression = ClassExpression(easy= "GraspableDisposition|EquivalentTo|isDispositionOf some (hasPart some GraspablePart)",
                                         medium= "GraspableDisposition|EquivalentTo|(isDispositionOf some ((hasPart some GraspablePart) and (isATouchableObject value boolean#true)))",
                                         hard= "GraspableDisposition|EquivalentTo|(isDispositionOf some ((hasPart some (GraspablePart and (IsAlreadyInUse value boolean#false)) and (isATouchableObject value boolean#true)))")

diposition_explanation = ClassExpressionExplanation(disposition_expression,
                                                    easy=["__object_disp__|isDispositionOf|__object__",
                                                          "__object__|hasPart|__handle__",
                                                          "__handle__|Type|__Handle__",
                                                          "__Handle__|SubClassOf|GraspablePart"],
                                                    medium=["__object__|isATouchableObject|boolean#true"],
                                                    hard=["__handle__|IsAlreadyInUse|boolean#false",
                                                          "__object__|isATouchableObject|boolean#true"],
                                                    concatenate=False) # Hard will not be concatenated with Medium

# =============== Capability Explanation =============
capability_expression = ClassExpression(easy= "GraspingCapability|EquivalentTo|(isCapabilityOf some (hasComponent some Gripper)",
                                        medium= "GraspingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent some Gripper) and (hasComponent some MotionPlanningAlgo))",
                                        hard = "GraspingCapability|EquivalentTo|(isCapabilityOf some ((hasComponent some (Gripper and (holdsSomething value boolean#false)) and (hasComponent some MotionPlanningAlgo))")

capability_explanation = ClassExpressionExplanation(capability_expression,
                                                    easy=["__agent_capa__|isCapabilityOf|__agent__",
                                                          "__agent__|hasComponent|__gripper__",
                                                          "__gripper__|Type|__Gripper__",
                                                          "__Gripper__|SubClassOf|Gripper"],
                                                    medium=["__agent__|hasComponent|__algo__",
                                                            "__algo__|Type|MotionPlanningAlgo"],
                                                    hard=["__gripper__|holdsSomething|boolean#false",
                                                          "__agent__|hasComponent|__algo__",
                                                          "__algo__|Type|MotionPlanningAlgo"],
                                                    concatenate=False) # Hard will not be concatenated with Medium

# =============== Property Explanation =============
property_expression = ClassExpression(easy= "", # isReachableBy
                                      medium= "(isContainedIn o isWithinGraspRangeOf)|SubPropertyOf|isReachableBy",
                                      hard= "(isContainedIn o isLocatedInArea o isWithinGraspRangeOf)|SubPropertyOf|isReachableBy")

property_explanation = ClassExpressionExplanation(property_expression,
                                                  easy= ["__object__|isReachableBy|__agent__"],
                                                  medium= [],
                                                  hard=[],
                                                  concatenate = True)

property_explanation.medium = ["__object__|isContainedIn|__container__",
                               "__container__|isWithinGraspRangeOf|__agent__"]

property_explanation.hard = ["__object__|isContainedIn|__container__",
                             "__container__|isLocatedInArea|__room__",
                             "__room__|isWithinGraspRangeOf|__agent__"]

# =============== QuestionManager =============

grasp_manager = QuestionManager(grasp_rule,
                                variable_manager,
                                affordance,
                                capability_explanation,
                                diposition_explanation,
                                property_explanation)

# easy
# "concepts" : [
#   "can grasp", 
#  "graspable",
#   "grasping",
#   "reachable", 
#   "opening width", "object_width"  
# ]

# medium
# "concepts" : [
#   "can grasp", 
#  "graspable", "touchable_object",
#   "grasping","motion_planing_algo",
#   "reachable", "is_contained_in", "within_grasping_range",
#   "opening width", "object_width"    
# ]

# hard
# "concepts" : [
#   "can grasp", 
#  "graspable", "touchable_object", "object_not_already_used",
#   "grasping","motion_planing_algo", "empty_gripper",
#   "reachable", "is_contained_in", "container_in_area", "within_grasping_range",
#   "opening width", "object_width"   
# ]

# gt_grasp_easy = "The __Agent__ can grasp the __Object__ because on one hand it has the grasping capability through its __Gripper__ which is a gripper. \
#                  On the other hand, the __Object__ has the disposition of being graspable because it has a __Handle__. \
#                  Moreover the __Object__ is reachable by the __Agent__."

# gt_grasp_medium = "The __Agent__ can grasp the __Object__ because on one hand it has the grasping capability through its __Gripper__ which is a gripper, \
#                   and being equipped with a motion planning algorithm. On the other hand, the __Object__ has the disposition of being graspable \
#                   because it has a __Handle__ and is a touchable object. Moreover the __Object__ is reachable by the __Agent__ because \
#                   it is contained in something which is within the grasping range of the __Agent__."
                 
# gt_grasp_hard = "The __Agent__ can grasp the __Object__ because on one hand it has the grasping capability through its __Gripper__ which is a gripper, \
#                   not currently holding something, and being equipped with a motion planning algorithm. On the other hand, the __Object__ has the disposition \
#                   of being graspable because it is a touchable object, and has a __Handle__ which is not already in use by someone. \
#                   Moreover the __Object__ is reachable by the __Agent__ because it is contained in something which is located in an area within the \
#                   grasping range of the __Agent__."