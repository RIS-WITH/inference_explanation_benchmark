

prompt_0 = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an \
          inference into a compact and simple sentence in natural langage."
          
prompt_1 = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an \
          inference into a compact and simple sentence in natural langage. \
          In description logics, x|isA|Y represent an inheritance relation, while x|property|z represents a relation between two individuals."
          
prompt_2 = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an \
          inference into a compact and simple sentence in natural langage. \
          In description logics, x|isA|Y represent an inheritance relation, while x|property|z represents a relation between two individuals. \
          The explanation should not refer to the individual names, but rather the semantic concepts they represent."
          
prompt_3 = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an\
            inference into a compact and simple sentence in natural langage. The translation must contain the least number sentences as possible, \
            and you mustn't describe the reasoning process. In description logics, x|isA|Y represent an inheritance relation, while x|property|z \
            represents a relation between two individuals. The explanation should not refer to the individual names, but rather the semantic concepts \
            they represent. For instance, x|isA|Cup, x|isEmpty|boolean#true would translate to the cup is empty. The inferences you will have to translate are about why an agent can do a particular action. The explanations are all important and must be all used in order to generate the translation."

prompt_init = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an\
               inference into a compact and simple sentence in natural langage."
               
prompt_test = "You are an AI model specialized in transforming formal logical inferences and their explanations into clear and concise natural language sentences.\
    In this task: \n\
    \t You will interpret inferences and explanations derived from the resolution of SWRL rules. \n\
    \t SWRL rules are used in ontologies to infer new facts based on known facts and logical conditions. \n\
    \t Each inference is accompanied by a set of explanations in the form of triples. These triples specify relationships between entities or concepts, such as xhz|isA|Human (which means xhz is an instance of the class Human). \n\
    Your goal: \n\
    \tConvert the SWRL inference and its supporting explanations into a natural language sentence. \n\
    \tEnsure the explanation is clear, concise, and accessible to someone unfamiliar with SWRL or Description Logics. \n\
    Here is an example: Input: Inference: xhz|hasBrother|okm Explanations: xhz|isA|Human (xhz is a Human), xhz|hasSibling|okm (xhz has a sibling okm), okm|isA|Man (xhz is a Man)\
    Output in Natural Language : The human xhz has a brother named okm because xhz is a human, who has okm as a sibling, who is a man."
    #Output in Natural Language : xhz has a brother named okm because xhz is a human, okm is a man, and okm is a sibling of xhz."

prompt_0_clean = prompt_0.replace('\t', '')
prompt_1_clean = prompt_1.replace('\t', '')
prompt_2_clean = prompt_2.replace('\t', '')
prompt_3_clean = prompt_3.strip('\t')

print(prompt_3_clean)
          

          

          
