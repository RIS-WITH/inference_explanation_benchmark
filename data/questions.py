# =================== Q1 ====================

class QuestionInstance:
    def __init__(self, name, fact, explanations, rule, classes_var, template_dict):
        self.name_ = name
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


rule_1 = "-Rule : Robot(?r), hasCapability(?r, ?c), ManipulationCapability(?c), Mug(?o), hasDisposition(?o, ?d), ManipulableDisposition(?d), Support(?s), isOn(?o,?s), isInFrontOf(?r,?s) -> canManipulate(?r, ?o)."

question_1 = QuestionInstance("q1", init_fact_q1, init_explanations_q1, rule_1, class_variables_q1, template_dict_q1)


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

rule_2 = "-Rule : Robot(?r), hasCapability(?r, ?c), ManipulationCapability(?c), Mug(?o), hasDisposition(?o, ?d), ManipulableDisposition(?d) -> canManipulate(?r, ?o)."

question_2 = QuestionInstance("q2",init_fact_q2, init_explanations_q2, rule_2, class_variables_q2, template_dict_q2)

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

rule_3 = "-Rule : Robot(?r), Object(?o), hasGraspingAffordance(?r, ?o), IsInFrontOf(?r,?o), Gripper(?g), hasComponent(?r,?g), isFree(?g, boolean#true), hasWeightPayload(?g,?w1), hasWeight(?o, ?w2), swrlb:lessThan(?w2,?w1) -> canGrasp(?r, ?o)."

question_3 = QuestionInstance("q3",init_fact_q3, init_explanations_q3, rule_3, class_variables_q3, template_dict_q3)


final_ex1_rule = "Agent(?a), hasCapability(?a, ?c), GraspingCapability(?c), Object(?o), hasDisposition(?o, ?d), GraspableDisposition(?d), Closet(?x), isIn(?o, ?x), isInFrontOf(?a, ?x), (hasComponent some (Gripper and (holdsSomething value false)))(?a), hasGripper(?a, ?g), hasOpeningWidth(?g, ?w1), hasWidth(?o, ?w2), greaterThan(?w1, ?w2), (hasDoor some (isOpen value true))(?x) -> canGrasp(?a, ?o)."

final_ex2_rule = "Agent(?a), hasCapability(?a, ?c), LiftingCapability(?c), Object(?o), hasDisposition(?o, ?d), LiftableDisposition(?d), isOn(?o, ?t), Table(?t), isNear(?a, ?t), (hasComponent some (Gripper and (holdsSomething value false)))(?a), hasGripper(?a, ?g), hasWeightLimit(?g, ?w1), hasWeight(?o, ?w2), lessThan(?w2, ?w1), (not (hasPart some (isAttached value true)))(?o) -> canLift(?a, ?o)."

final_ex3_rule = "Agent(?a), hasCapability(?a, ?c), PushingCapability(?c), Object(?o), hasDisposition(?o, ?d), PushableDisposition(?d), Table(?t), isOn(?o, ?t), isNear(?a, ?t), (hasComponent some (Gripper and (holdsSomething value false)))(?a), hasGripper(?a, ?g), hasForceLimit(?g, ?f1), requiresForce(?o, ?f2), equal(?f1, ?f2), (not (isInFrontOf some (isAttached value true)))(?o) -> canPushForward(?a, ?o)."


ex1_affordance = "Agent(?a), hasCapability(?a, ?c), GraspingCapability(?c), Object(?o), hasDisposition(?o, ?d), GraspableDisposition(?d)"
ex1_space_constraint = "Closet(?x), isIn(?o, ?x), isInFrontOf(?a,?x)"
ex1_physical_constraint = "hasGripper(?a, ?g), hasOpeningWidth(?g, ?w1), hasWidth(?o, ?w2), greaterThan(?w1, ?w2)"
ex1_resource_constraint = "(holdsSomething value false)(?g)"
ex1_contextual_constraint = "(hasDoor some (isOpen value true))(?x)"


class_variables_final_q1 = { 
                    "__object1__" : ["Handle", "HandGrip"], 
                    "__object2__" : ["Mug", "Cup"],
                    "__support__" : ["Closet", "Cupboard", "Cabinet"],
                    "__agent__" :   ["Robot", "Agent", "Pepper", "Pr2"]
                     }

ex2_affordance = "Agent(?a), hasCapability(?a, ?c), LiftingCapability(?c), Object(?o), hasDisposition(?o, ?d), LiftableDisposition(?d)"
ex2_space_constraint = "Table(?t), isOn(?o, ?t), isNear(?a, ?t)"
ex2_physical_constraint = "hasWeightLimit(?g, ?w1), hasWeight(?o, ?w2), lessThan(?w2, ?w1)" # the robot can lift the object's weight
ex2_resource_constraint = "(holdsSomething value false)(?g)" # the robot isnt holding anything
ex2_contextual_constraint = "(hasPart only (isAttached value false))(?x)" # the object has no part which is attached to the table

ex3_affordance = "Agent(?a), hasCapability(?a, ?c), PushingCapability(?c), Object(?o), hasDisposition(?o, ?d), PushableDisposition(?d)"
ex3_space_constraint = "Desk(?x), isOn(?o, ?x), isInFrontOf(?a,?x)"
ex3_physical_constraint = "hasGripper(?a, ?g), hasForce(?g, ?f1), requiresForce(?o, ?f2), equal(?f1, ?f2)"
ex3_resource_constraint = "(holdsSomething value false)(?g)"
ex3_contextual_constraint = "(hasDoor some (isOpen value true))(?x)"

# Free gripper constraints
free_gripper_simple = "(hasComponent min 1 FreeGripper)(?a)" # FreeGripper Eq to following definitions
free_gripper_medium = "(hasComponent min 1 (Gripper and (holdsSomething value false)))(?a)"  #FreeGripper Eq to (Gripper and (holdsSomething value false))
free_gripper_complex = "(hasComponent min 1 (Gripper and (holdsSomething value false) and (canBeOpened value true)))(?a)"  #FreeGripper Eq to X

# Space constraints
space_simple = "canReach(?a,?o)" # chain axiom
space_medium = "isNear o isContaining" # isNear o contains -> canReach -- a|isNear|c, c|contains|o -> a|canReach|o
space_complex = "isFrontOf o isContaining" # isNear o contains -> canReach with isInFrontOf SubPropertyOf isNear, and isAtReachDistanceOf inverse of canReach, isContainedIn inverse of contains

# Physical constraints
weight_limit = "hasGripper(?a, ?g), hasWeightLimit(?g, ?w1), hasWeight(?o, ?w2), lessThan(?w2, ?w1)"
width_limit  = "hasGripper(?a, ?g), hasOpeningWidth(?g, ?w1), hasWidth(?o, ?w2), greaterThan(?w1, ?w2)"
force_limit = "hasGripper(?a, ?g), canProduceForce(?g, ?f1), requiresForce(?o, ?f2), equal(?f1, ?f2)"

# QUESTION 1 (3 levels for grasping and graspable + width)
grasping_direct = "c|isA|GraspingCapability"
grasping_indirect = "GraspingCapability|SubClassOf|(hasComponent some Gripper), c|hasComponent|g, g|isA|Gripper"
grasping_indirect_inheritance = "GraspingCapability|SubClassOf|(hasComponent some Gripper), Hand|isA|Gripper, c|hasComponent|g, g|isA|Hand"

graspable_direct = "d|isA|GraspableDisposition"
graspable_indirect = "GraspableDisposition|SubClassOf|(hasPart some Handle), d|hasPart|h, h|isA|Handle"
graspable_indirect_inheritance = "GraspableDisposition|SubClassOf|(hasPart some (Handle and hasDisposition some GraspableDisposition)), d|hasPart|h, h|isA|Handle, h|hasDisposition|dh, dh|isA|GraspableDisposition"

grasp_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), GraspingCapability(?c), Object(?o), hasDisposition(?o, ?d), GraspableDisposition(?d), EndEffector(?g), hasComponent(?a,?g), hasOpeningWidth(?g,?w1), hasWidth(?o,?w2), greaterThan(?w1,?w2) -> canGrasp(?a, ?o)."
questions_grasp = [[graspable_direct, graspable_direct], [grasping_indirect, graspable_indirect], [grasping_indirect_inheritance, graspable_indirect_inheritance]]

class_variables_final_grasp = { 
                    "__object__" : ["Mug", "Cup", "Knife", "Fork", "Pot", "Screwdriver"],
                    "__agent__" :   ["Robot", "Pr2", "Pepper", "Tiago"],
                    "__component__" :   ["Gripper", "Hand", "Claw"]
                     }

template_dict_grasp_direct = {
                    'pepper': '__var0__',  
                    'mug_3': '__var1__',
                    'mug_3_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'Robot': '__agent__',
                    'Mug': '__object__',
                    'Gripper': '__component__'
                    }

init_fact_grasp = "pepper|canGrasp|mug_3"

init_explanations_grasp_direct = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        "pepper_capa|Type|GraspingCapability",
                        "mug_3|Type|Mug",
                        "Mug|SubClassOf|Object",
                        "mug_3|hasDisposition|mug_3_disp",
                        "mug_3_disp|Type|GraspableDisposition",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|hasOpeningWidth|integer#20",
                        "mug_3|hasWidth|integer#10",
                        ]

template_dict_grasp_indirect = {'pepper': '__var0__',  
                    'mug_3': '__var1__',
                    'mug_3_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'handle_3' : '__var5__',
                    'Robot': '__agent__',
                    'Mug': '__object__',
                    'Gripper': '__component__'
                    }

init_explanations_grasp_indirect = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        "pepper_capa|Type|GraspingCapability",
                        "mug_3|Type|Mug",
                        "Mug|SubClassOf|Object",
                        "mug_3|hasDisposition|mug_3_disp",
                        "GraspableDisposition|SubClassOf|(isDispositionOf some (hasPart some Handle))",
                        "mug_3_disp|isDispositionOf|mug_3",
                        "mug_3|hasPart|handle_3",
                        "handle_3|Type|Handle",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|hasOpeningWidth|integer#20",
                        "mug_3|hasWidth|integer#10"
                        ]

template_dict_grasp_indirect_inheritance = {'pepper': '__var0__',  
                    'mug_3': '__var1__',
                    'mug_3_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'handle_3' : '__var5__',
                    'handle_3_disp' : '__var6__',
                    'Robot': '__agent__',
                    'Mug': '__object__',
                    'Gripper': '__component__'
                    }

init_explanations_grasp_indirect_inheritance = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        "pepper_capa|Type|GraspingCapability",
                        "mug_3|Type|Mug",
                        "Mug|SubClassOf|Object",
                        "mug_3|hasDisposition|mug_3_disp",
                        "GraspableDisposition|SubClassOf|(isDispositionOf some (hasPart some (Handle and (hasDisposition some GraspableDisposition)))",
                        "mug_3_disp|isDispositionOf|mug_3",
                        "mug_3|hasPart|handle_3",
                        "handle_3|hasDisposition|handle_3_disp",
                        "handle_3_disp|Type|GraspableDisposition",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|hasOpeningWidth|integer#20",
                        "mug_3|hasWidth|integer#10"
                        ]

final_question_1_simple = QuestionInstance("q_grasp_easy", init_fact_grasp, init_explanations_grasp_direct, grasp_rule, class_variables_final_grasp, template_dict_grasp_direct)
final_question_1_medium = QuestionInstance("q_grasp_medium", init_fact_grasp, init_explanations_grasp_indirect, grasp_rule, class_variables_final_grasp, template_dict_grasp_indirect)
final_question_1_hard = QuestionInstance("q_grasp_hard", init_fact_grasp, init_explanations_grasp_indirect_inheritance, grasp_rule, class_variables_final_grasp, template_dict_grasp_indirect_inheritance)


# QUESTION 2 (3 levels for lifting and liftable + weight)
lifting_direct = "c|isA|LiftingCapability"
lifting_indirect = "LiftingCapability|SubClassOf|(hasComponent min 2 Gripper), c|hasComponent|g1, g1|isA|Gripper, c|hasComponent|g2, g2|isA|Gripper"
lifting_indirect_inheritance = "LiftingCapability|SubClassOf|(hasComponent min 2 Gripper), Hand|isA|Gripper, c|hasComponent|g1, g1|isA|Gripper, c|hasComponent|g2, g2|isA|Hand"

liftable_direct = "d|isA|LiftableDisposition"
liftable_indirect = "LiftableDisposition|SubClassOf|(hasSide min 2 FlatSurface), d|hasSide|s1, s1|isA|FlatSurface, d|hasSide|s2, s2|isA|FlatSurface"
liftable_indirect_inheritance = "LiftableDisposition|SubClassOf|(hasSide min 2 FlatSurface), d|hasSide|s1, s1|isA|FlatSurface, d|hasSide|s2, s2|isA|PlaneSurface, PlaneSurface|isA|FlatSurface"
class_variables_final_lift = { 
                    "__object__" : ["StorageBox", "Book", "Brick", "Cube"], 
                    "__agent__" :   ["Robot", "Agent", "Pepper"],
                    "__component__" :   ["Gripper", "Hand", "Claw"]
                    }

lift_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), LiftingCapability(?c), Object(?o), hasDisposition(?o, ?d), LiftableDisposition(?d), EndEffector(?g), hasComponent(?a,?g), hasWeightLimit(?g,?w1), hasWeight(?o,?w2), lesserThan(?w2,?w1) -> canLift(?a, ?o)."

init_fact_lift = "pepper|canLift|book_1"

template_dict_lift_direct= {
                    'pepper': '__var0__',  
                    'book_1': '__var1__',
                    'book_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'Robot': '__agent__',
                    'Book': '__object__',
                    'Gripper': '__component__'
                    }

init_explanations_lift_direct = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        "pepper_capa|Type|LiftingCapability",
                        "book_1|Type|Book",
                        "Book|SubClassOf|Object",
                        "book_1|hasDisposition|book_1_disp",
                        "book_1_disp|Type|LiftableDisposition",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|hasWeightLimit|integer#400",
                        "book_1|hasWeight|integer#150",
                        ]

template_dict_lift_indirect = {
                    'pepper': '__var0__',  
                    'book_1': '__var1__',
                    'book_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'pepper_right_gripper' : '__var5__',
                    'book_1_side_left' : '__var6__',
                    'book_1_side_right' : '__var7__',
                    'Robot': '__agent__',
                    'Book': '__object__',
                    'Gripper': '__component__'
                    }

init_explanations_lift_indirect = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        " LiftingCapability|SubClassOf|(hasComponent min 2 Gripper)",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "pepper|hasComponent|pepper_right_gripper",
                        "pepper_right_gripper|Type|Gripper",
                        "pepper_left_gripper|DifferentFrom|pepper_right_gripper",
                        "book_1|Type|Book",
                        "Book|SubClassOf|Object",
                        "book_1|hasDisposition|book_1_disp",
                        "LiftableDisposition|SubClassOf|(isDipositionOf some (hasSide min 2 FlatSurface))",
                        "book_1_disp|isDipositionOf|book_1",
                        "book_1|hasSide|book_1_side_left",
                        "book_1_side_left|Type|FlatSurface",
                        "book_1|hasSide|book_1_side_right",
                        "book_1_side_right|Type|FlatSurface",
                        "book_1_side_right|DifferentFrom|book_1_side_left",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|hasWeightLimit|integer#400",
                        "book_1|hasWeight|integer#150",
                        ]

template_dict_lift_indirect_inheritance = {
                    'pepper': '__var0__',  
                    'book_1': '__var1__',
                    'book_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'pepper_right_gripper' : '__var5__',
                    'book_1_side_left' : '__var6__',
                    'book_1_side_right' : '__var7__',
                    'Robot': '__agent__',
                    'Book': '__object__',
                    'Gripper': '__component__'
                    }

init_explanations_lift_indirect_inheritance = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        "LiftingCapability|SubClassOf|(hasComponent min 2 Gripper)",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "pepper|hasComponent|pepper_right_gripper",
                        "pepper_right_gripper|Type|Gripper",
                        "pepper_left_gripper|DifferentFrom|pepper_right_gripper",
                        "book_1|Type|Book",
                        "Book|SubClassOf|Object",
                        "book_1|hasDisposition|book_1_disp",
                        "LiftableDisposition|SubClassOf|(isDipositionOf some (hasSide min 2 FlatSurface))",
                        "book_1_disp|isDipositionOf|book_1",
                        "book_1|hasSide|book_1_side_left",
                        "book_1_side_left|Type|FlatSurface",
                        "book_1|hasSide|book_1_side_right",
                        "book_1_side_right|Type|PlaneSurface",
                        "PlaneSurface|SubClassOf|FlatSurface",
                        "book_1_side_right|DifferentFrom|book_1_side_left",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|hasWeightLimit|integer#400",
                        "book_1|hasWeight|integer#150",
                        ]

final_question_2_simple = QuestionInstance("q_lift_easy", init_fact_lift, init_explanations_lift_direct, lift_rule, class_variables_final_lift, template_dict_lift_direct)
final_question_2_medium = QuestionInstance("q_lift_medium", init_fact_lift, init_explanations_lift_indirect, lift_rule, class_variables_final_lift, template_dict_lift_indirect)
final_question_2_hard = QuestionInstance("q_lift_hard", init_fact_lift, init_explanations_lift_indirect_inheritance, lift_rule, class_variables_final_lift, template_dict_lift_indirect_inheritance)

# QUESTION 3 (3 levels for pushing and pushable + force)
pushing_direct = "c|isA|PushingCapability"
pushing_indirect = "PushingCapability|SubClassOf|(hasComponent only RigidEndEffector), c|hasComponent|g1, g1|isA|RigidEndEffector, c|hasComponent|g2, g2|isA|RigidEndEffector"
pushing_indirect_inheritance = "PushingCapability|SubClassOf|(hasComponent only RigidEndEffector), Hand|isA|Gripper, c|hasComponent|g1, g1|isA|Gripper, c|hasComponent|g2, g2|isA|Hand"

pushable_direct = "d|isA|PushableDisposition"
pushable_indirect = "PushableDisposition|SubClassOf|(hasPart only UnattachedPart), d|hasPart|s1, s1|isA|UnattachedPart, d|hasPart|s2, s2|isA|UnattachedPart"
pushable_indirect_inheritance = "PushableDisposition|SubClassOf|(hasPart only UnattachedPart), d|hasPart|s1, s1|isA|UnattachedPart, d|hasPart|s2, s2|isA|DisconnectedPart, DisconnectedPart|isA|UnattachedPart"
class_variables_final_push = { 
                    "__object__" : ["StorageBox", "Book", "Brick", "Cube"], 
                    "__agent__" :   ["Robot", "Agent", "Pepper"],
                    "__component__" :   ["Gripper", "Hand", "Claw", "RoboticHand"]
                    }

push_rule = "-Rule : Agent(?a), hasCapability(?a, ?c), PushingCapability(?c), Object(?o), hasDisposition(?o, ?d), PushableDisposition(?d), EndEffector(?g), hasComponent(?a,?g), canProduceForce(?g,?w1), requiresForce(?o,?w2), equal(?w2,?w1) -> canPush(?a, ?o)."

init_fact_push = "pepper|canPush|book_1"

template_dict_push_direct= {
                    'pepper': '__var0__',  
                    'book_1': '__var1__',
                    'book_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'handle_3' : '__var5__',
                    'handle_3_disp' : '__var6__',
                    'Robot': '__agent__',
                    'Book': '__object__',
                    'Gripper': '__component__'
                    }

init_explanations_push_direct = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        "pepper_capa|Type|PushingCapability",
                        "book_1|Type|Book",
                        "Book|SubClassOf|Object",
                        "book_1|hasDisposition|book_1_disp",
                        "book_1_disp|Type|PushableDisposition",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|canProduceForce|integer#60",
                        "book_1|requiresForce|integer#60"
                        ]

template_dict_push_indirect = {
                    'pepper': '__var0__',  
                    'book_1': '__var1__',
                    'book_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'pepper_right_gripper' : '__var5__',
                    'book_1_cover' : '__var6__',
                    'book_1_back' : '__var7__',
                    'Robot': '__agent__',
                    'Book': '__object__',
                    'Gripper': '__component__'
                    }

init_explanations_push_indirect = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        "PushingCapability|SubClassOf|(hasGripper only RigidEndEffector)",
                        "pepper|hasGripper|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|RigidEndEffector",
                        "pepper|hasGripper|pepper_right_gripper",
                        "pepper_right_gripper|Type|Gripper",
                        "Gripper|SubClassOf|RigidEndEffector",
                        "book_1|Type|Book",
                        "Book|SubClassOf|Object",
                        "book_1|hasDisposition|book_1_disp",
                        "PushableDisposition|SubClassOf|(isDispositionOf some (hasPart only UnattachedPart))",
                        "book_1_disp|isDipositionOf|book_1",
                        "book_1|hasPart|book_1_cover",
                        "book_1_cover|Type|UnattachedPart",
                        "book_1|hasPart|book_1_back",
                        "book_1_back|Type|UnattachedPart",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|canProduceForce|integer#60",
                        "book_1|requiresForce|integer#60"
                        ]

template_dict_push_indirect_inheritance = {
                    'pepper': '__var0__',  
                    'book_1': '__var1__',
                    'book_1_disp': '__var2__',
                    'pepper_capa': '__var3__',
                    'pepper_left_gripper' : '__var4__',
                    'pepper_right_gripper' : '__var5__',
                    'book_1_cover' : '__var6__',
                    'book_1_back' : '__var7__',
                    'Robot': '__agent__',
                    'Book': '__object__',
                    'Gripper': '__component__'
                    }

init_explanations_push_indirect_inheritance = [
                        "pepper|Type|Robot",
                        "Robot|SubClassOf|Agent",
                        "pepper|hasCapability|pepper_capa",
                        "PushingCapability|SubClassOf|(hasGripper only RigidEndEffector)",
                        "pepper|hasGripper|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|RigidEndEffector",
                        "pepper|hasGripper|pepper_right_gripper",
                        "pepper_right_gripper|Type|Gripper",
                        "Gripper|SubClassOf|RigidEndEffector",
                        "book_1|Type|Book",
                        "Book|SubClassOf|Object",
                        "book_1|hasDisposition|book_1_disp",
                        "PushableDisposition|SubClassOf|(isDispositionOf some (hasPart only UnattachedPart))",
                        "book_1_disp|isDipositionOf|book_1",
                        "book_1|hasPart|book_1_cover",
                        "book_1_cover|Type|UnattachedPart",
                        "book_1|hasPart|book_1_back",
                        "book_1_back|Type|DisconnectedPart",
                        "DisconnectedPart|SubClassOf|UnattachedPart",
                        "pepper|hasComponent|pepper_left_gripper",
                        "pepper_left_gripper|Type|Gripper",
                        "Gripper|SubClassOf|EndEffector",
                        "pepper_left_gripper|canProduceForce|integer#60",
                        "book_1|requiresForce|integer#60"
                        ]

final_question_3_simple = QuestionInstance("q_push_easy", init_fact_push, init_explanations_push_direct, push_rule, class_variables_final_push, template_dict_push_direct)
final_question_3_medium = QuestionInstance("q_push_medium", init_fact_push, init_explanations_push_indirect, push_rule, class_variables_final_push, template_dict_push_indirect)
final_question_3_hard = QuestionInstance("q_push_hard", init_fact_push, init_explanations_push_indirect_inheritance, push_rule, class_variables_final_push, template_dict_push_indirect_inheritance)


# QUESTION 4 (3 levels for movingTo and movableTo + network available)
moving_direct = "c|isA|Moving"
moving_indirect = "Moving|SubClassOf|((hasComponent some MotionCaptureSystem) and (isAvailable value true)), c|hasComponent|optitrack, optitrack|isAvailable|boolean#true, optitrack|isA|MotionCaptureSystem"
moving_indirect_inheritance = "Moving|SubClassOf|((hasComponent some MotionCaptureSystem) and (isAvailable value true)), c|hasComponent|optitrack, optitrack|sameAs|mocap_system, mocap_system|isA|MotionCaptureSystem, optitrack|isAvailable|boolean#true"

movable_direct = "d|isA|MovableTo"
movable_indirect = "MovableTo|SubClassOf|(hasPart some (Door and (isOpen value true))), d|hasPart|d1, d1|isA|Door, d1|isOpen|boolean#true"
movable_indirect_inheritance = "MovableTo|SubClassOf|(hasPart some (Door and (isOpen value true))), d|hasPart|d1, d1|isA|Door, d1|isOpen|boolean#true"
