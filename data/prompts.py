

prompt_0 = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an \
          inference into a compact and simple sentence in natural langage."
          
prompt_1 = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an \
          inference into a compact and simple sentence in natural langage. \
          In description logics, x|isA|Y represent an inheritance relation, while x|property|z represents a relation between two individuals."
          
prompt_2 = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an \
          inference into a compact and simple sentence in natural langage. \
          In description logics, x|isA|Y represent an inheritance relation, while x|property|z represents a relation between two individuals. \
          The explanation should not refer to the individual names, but rather the semantic concepts they represent."
          
prompt_3 = "As an expert translator from description logics in ontologies to natural language, your job is to transform the chain of explanations for an \
          inference into a compact and simple sentence in natural langage. The translation must contain the least number sentences as possible, and you mustn't describe the reasoning process\
          In description logics, x|isA|Y represent an inheritance relation, while x|property|z represents a relation between two individuals. \
          The explanation should not refer to the individual names, but rather the semantic concepts they represent. \
          For instance, x|isA|Cup, x|isEmpty|boolean#true would translate to the cup is empty"
          
prompt_0_clean = prompt_0.replace('\t', '')
prompt_1_clean = prompt_1.replace('\t', '')
prompt_2_clean = prompt_2.replace('\t', '')
prompt_3_clean = prompt_3.strip('\t')

print(prompt_3_clean)
          

          

          
