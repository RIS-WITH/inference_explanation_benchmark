
# =============== EXAMPLES ===================

example_question_0 = "S: inference = bob|hasBrother|fred / explanations = bob|isA|Human, bob|hasSilbing|fred, fred|isA|Man."
example_rule_0 = "The used rule was : Human(?a), hasSilbing(?a,?b), Man(?b) -> hasBrother(?a, ?b)."
example_answer_0 =  "A: Let's translate. translation is fred is bob's brother because he is a man and his sibling."
example_0 = (example_question_0.replace('\t', ''), example_answer_0.replace('\t', ''), example_rule_0.replace('\t', ''))



example_question_1 = "S: inference = pepper|canSpeakWith|agent_0 / explanations = pepper|isA|Robot, pepper|hasCapability|pepper_capa, \
                    pepper_capa|isA|VerbalCommunicationCapability, agent_0|isA|Human, agent_0|hasDisposition|agent_0_disp,\
                    agent_0_disp|isA|VerbalCommunicationDisposition, pepper|isNear|agent_0, agent_0|isInFrontOf|pepper, agent_0|isAvailable|boolean#true."
example_rule_1 = "The used rule was : Robot(?r), hasCapability(?r,?c), VerbalCommunicationCapability(?c), Human(?a), hasDisposition(?a, ?d), \
                  VerbalCommunicationDisposition(?d), isNear(?r,?a), isInFrontOf(?a,?r), isAvailable(?a, boolean#true)  -> canSpeakWith(?r, ?a)."
example_answer_1=  "A: Let's translate. translation is pepper can speak with agent_0 because it has the capability to communicate verbally and agent_0\
                    has the disposition for verbal communication, and both agents are close to each other."
example_1 = (example_question_1.replace('\t', ''), example_answer_1.replace('\t', ''), example_rule_1.replace('\t', ''))

