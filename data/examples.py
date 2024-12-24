
# =============== EXAMPLES ===================

example_question_0 = "S: inference = xhz|hasBrother|okm / explanations = xhz|isA|Human, xhz|hasSilbing|okm, okm|isA|Man."
example_rule_0 = "The used rule was : Human(?a), hasSilbing(?a,?b), Man(?b) -> hasBrother(?a, ?b)."
example_answer_0 =  "A: Let's translate. translation is okm is xhz's brother because he is a man and his sibling."
example_0 = (example_question_0, example_answer_0, example_rule_0)



example_question_1 = "S: inference = prth|canSpeakWith|dzkl / explanations = prth|isA|Robot, prth|hasCapability|stkl, stkl|isA|VerbalCommunicationCapability,\
                     dzkl|isA|Human, dzkl|hasDisposition|szom, szom|isA|VerbalCommunicationDisposition, prth|isNear|dzkl, dzkl|isInFrontOf|prth, \
                     dzkl|isAvailable|boolean#true."
                    
example_rule_1 = "The used rule was : Robot(?r), hasCapability(?r,?c), VerbalCommunicationCapability(?c), Human(?a), hasDisposition(?a, ?d), \
                  VerbalCommunicationDisposition(?d), isNear(?r,?a), isInFrontOf(?a,?r), isAvailable(?a, boolean#true) -> canSpeakWith(?r, ?a)."
                  
#example_answer_1=  "A: Let's translate. translation is prth can speak with dzkl because it has the capability to communicate verbally and dzkl has the disposition for verbal communication, and both agents are close to each other."
example_answer_1=  "A: Let's translate. translation is the robot prth can speak with the human dkzl because it has the capability to communicate verbally and dzkl has \
                    the disposition for verbal communication, and both agents are close to each other."
example_1 = (example_question_1, example_answer_1, example_rule_1)

# example_question_2 = "S: inference = pepper|canSpeakWith|agent_0 / explanations = pepper|isA|Robot, pepper|hasCapability|pepper_capa, \
#                     pepper_capa|isA|VerbalCommunicationCapability, agent_0|isA|Human, agent_0|hasDisposition|agent_0_disp,\
#                     agent_0_disp|isA|VerbalCommunicationDisposition, pepper|isNear|agent_0, agent_0|isInFrontOf|pepper, agent_0|isAvailable|boolean#true."
                    
# example_rule_2 = "The used rule was : Robot(?r), hasCapability(?r,?c), VerbalCommunicationCapability(?c), Human(?a), hasDisposition(?a, ?d), \
#                   VerbalCommunicationDisposition(?d), isNear(?r,?a), isInFrontOf(?a,?r), isAvailable(?a, boolean#true)  -> canSpeakWith(?r, ?a)."
                  
# example_answer_2=  "A: Let's translate. translation is pepper can speak with agent_0 because it has the capability to communicate verbally and agent_0\
#                     has the disposition for verbal communication, and both agents are close to each other."
# example_2 = (example_question_2.replace('\t', ''), example_answer_2.replace('\t', ''), example_rule_2.replace('\t', ''))

