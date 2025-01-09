import random
import copy
import collections
import string
import uuid
import re

from data.canGrasp import VariableConcept
from data.prompts import prompt_0_clean, prompt_1_clean, prompt_2_clean, prompt_3_clean, prompt_test

global_nb_var = 20

class PromptGenerator:
	def __init__(self, prompt):
		self.init_prompt_ = prompt
		self.examples_ = []

	def build_cot_elem(self, role, tokens):
		res_elem = {}
		res_elem["role"]= role
		res_elem["content"] = tokens
		return res_elem

	def build_prompt(self, with_CoT = True, with_rule = False):
		final_prompt = []
		clean_prompt = self.init_prompt_.replace("\n", "").replace("\t", "").replace("      ", "")
		user_init_prompt = self.build_cot_elem('user', clean_prompt)
		final_prompt.append(user_init_prompt)

		if(with_CoT == True):
			for example in self.examples_:
				question = example.question_
				rule = example.rule_
				answer = example.answer_

				if(with_rule):
					final_prompt.append(self.build_cot_elem("user", question + " " + rule))
				else:
					final_prompt.append(self.build_cot_elem("user", question))
				final_prompt.append(self.build_cot_elem("assistant",  answer))
		
		return final_prompt
    

# generates a random value for variables
def id_generator(size=6, chars=string.ascii_lowercase): # + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# check if pattern is in input (list is in list of lists)
def isInList(input, pattern):
	for elem in input:
		if collections.Counter(elem) == collections.Counter(pattern) :
			return True
	return False
 
# contains every generated variation of a question
class InstantiatedQuestion:
	""" Stores an instantiated generated question """
	def __init__(self, fact, explanation, id_question, rule, selected_classes, sentence, selected_names):
		self.fact_ = fact
		self.explanations_ = explanation
		self.selected_classes_ = selected_classes
		self.selected_names_ = selected_names
		self.id_question_ = id_question
		self.rule_ = rule
		self.sentence_ = sentence

	def print_question(self):
		print("Question " + self.id_question_ + " is : ")
		print("-- fact : ", self.fact_)
		print("-- explanations :")
		for e in self.explanations_:
			print("\t", e)

# contains a top level question, and generated variations
class Question:
	def __init__(self, init_question, id_question, class_variables, rule, sentence, concepts_rule):
		# a ne pas mettre dans le dataset final
		self.init_question_ = init_question # contains the initial instantiated question
		self.template_question_ = None
		self.class_variables_ = class_variables
		self.generated_questions_ = [] # contains every question generated through the template
		self.id_question_ = id_question
		self.rule_ = rule # contains the rule used to infer the fact
		self.init_prompt_ = None
		self.init_prompt_rule_ = None
		self.template_ground_truth_sentence_ = sentence
		self.concepts_rule_ = concepts_rule

class QuestionGenerator:
	def __init__(self, prompt_generator):
		self.questions_ = []
		self.examples_ = []
		self.prompt_generator_ = prompt_generator
	
	def add_example(self, example):
		self.examples_.append(example)
		self.prompt_generator_.examples_.append(example)
    
	def replace_template(self, old_template, template_dict):
     
		new_fact = copy.deepcopy(old_template)
  
		for id_elem in range(0, len(old_template)):
			for template_param in template_dict:
				#if(template_param in old_template[id_elem]):
				if(template_param == old_template[id_elem]):
					new_fact[id_elem] = template_dict[template_param]
     
		return new_fact
     
	def generate_template(self, fact, explanations, template_dict):
		instantiated_fact = ""
		instantiated_explanations = []

		split_fact = fact.split("|")
		new_fact = self.replace_template(split_fact, template_dict)
		instantiated_fact = '|'.join(new_fact)
  
		for expl in explanations:
			split_exp = expl.split("|")
			new_exp = self.replace_template(split_exp, template_dict)
			instantiated_explanation = '|'.join(new_exp)
			instantiated_explanations.append(instantiated_explanation)

		return (instantiated_fact, instantiated_explanations)

	def add_question(self, question, with_CoT = True, verbose = False):

		new_id = question.name_ #"q"+str(len(self.questions_))
		new_question = Question(init_question=[question.fact_, question.explanations_, question.rule_], id_question=new_id, 
                        		class_variables=question.classes_var_, rule=question.rule_, sentence=question.gt_template_sentence_, 
                          		concepts_rule=question.concepts_rule_)

		prompt_with_rule = self.prompt_generator_.build_prompt(with_CoT, True)
		prompt_without_rule = self.prompt_generator_.build_prompt(with_CoT, False)
		new_question.init_prompt_ = prompt_without_rule
		new_question.init_prompt_rule_ = prompt_with_rule
  
		template_fact, template_explanations = self.generate_template(question.fact_, question.explanations_, question.template_dict_)
		new_question.template_question_ = [template_fact, template_explanations]
  
		if(verbose == True):
			self.print_question(new_question, False)
		self.questions_.append(new_question)
	
	def create_question(self, question, with_rule = False):
     
		explanation_str = ', '.join(question.explanations_)
		res = "-Inference : " + question.fact_ + " \n -Justifications : " + explanation_str + ". "
  
		if(with_rule):
			res += question.rule_
	
		return res
  
	def generate_question_variations(self, nb_var = global_nb_var):
		for q in self.questions_:
			facts, explanations, selected_classes, sentences, selected_names  = self.generate_variations(q, nb_var)

			for fact, expl, sel_class, sent, sel_ind in zip(facts, explanations, selected_classes, sentences, selected_names):
				id_var = q.id_question_ + "_"+ str(len(q.generated_questions_))
				new_var = InstantiatedQuestion(fact, expl, id_var, q.rule_, sel_class, sent, sel_ind)
				q.generated_questions_.append(new_var)
    
	def get_classes_names(self, selected_classes):
		res = []
		for selected_class in selected_classes.items():
			res.append(selected_class[1].label_)
   
		return res
  
	def generate_variations(self, question, nb_variations):
		res_facts = []
		res_explanations = []
		res_selected_classes = []
		res_gt_sentences = []
		res_selected_individual_names = []

		print("generating variations")

		while len(res_facts) < nb_variations:
			# creates empty dict with each class variation to be made
			selected_classes_ = {}
			selected_indivs_ = []
   
			for class_var in question.class_variables_:
				selected_classes_[class_var] = None

			new_fact = copy.deepcopy(question.template_question_[0])
			new_explanation = copy.deepcopy(question.template_question_[1])
			new_sentence = copy.deepcopy(question.template_ground_truth_sentence_)

			for class_var in question.class_variables_:
				if(class_var in new_fact):
					selected_classes_[class_var] = random.choice(question.class_variables_[class_var])
					new_fact = new_fact.replace(class_var, selected_classes_[class_var].concept_)
     
			for index, exp in enumerate(new_explanation):
       
				for class_var in question.class_variables_:
					if(class_var in exp):
						if(selected_classes_[class_var] is None):
							selected_classes_[class_var] = random.choice(question.class_variables_[class_var])
						new_explanation[index] = exp.replace(class_var, selected_classes_[class_var].concept_)
						# split by caps lock letter and add spaces between
						#new_sentence = new_sentence.replace(class_var, selected_classes_[class_var].lower())
						
				for i in range(0, 20):
					var_name = "__var" + str(i) + "__"
					var_value = id_generator(random.choice(range(1,5)))
					#var_value = str(uuid.uuid4()).split('-')[0]

					if var_name in new_fact:
						new_fact = new_fact.replace(var_name, var_value)
						# add the chosen random individual name into the list
						selected_indivs_.append(var_value)

					for index, exp in enumerate(new_explanation):
						if var_name in exp:
							new_explanation[index] = exp.replace(var_name, var_value)
							# add the chosen random individual name into the list
							if(var_value not in selected_indivs_):
								selected_indivs_.append(var_value)
        
				prev_int = 0
				for i in range(1, 3):
					var_name = "integer#" + str(i) + ""
					int_value = 0
					while int_value <= prev_int:
						int_value = random.choice(range(30, 60 + i*10))
					var_value = "integer#" + str(int_value) + ""
					prev_int = int_value

					if var_name in new_fact:
						new_fact = new_fact.replace(var_name, var_value)
						# add the chosen random individual name into the list
						new_val = VariableConcept(var_value, str(int_value))
						selected_classes_[var_value] = new_val

					for index, exp in enumerate(new_explanation):
						if var_name in exp:
							new_explanation[index] = exp.replace(var_name, var_value)
							# add the chosen random individual name into the list
							if(var_value not in selected_classes_):
								new_val = VariableConcept(var_value, str(int_value))
								selected_classes_[var_value] = new_val

			if((not new_fact in res_facts) and (not isInList(res_explanations, new_explanation))):
				res_facts.append(new_fact)
				res_explanations.append(new_explanation)
				res_selected_classes.append(self.get_classes_names(selected_classes_))
				res_selected_individual_names.append(selected_indivs_)
				res_gt_sentences.append(new_sentence)

		return (res_facts, res_explanations, res_selected_classes, res_gt_sentences, res_selected_individual_names)

	def print_question(self, selected_question, with_var = False):

		print("Question " + selected_question.id_question_, " :")
		print("Initial question : ")
		print("- fact : ", selected_question.init_question_[0])
		print("- explanations : ")
		for e in selected_question.init_question_[1]:
			print("\t - ", e)
		print("Template question : ")
		print("- fact : ", selected_question.template_question_[0])
		print("- explanations : ")
		for e in selected_question.template_question_[1]:
			print("\t - ", e)
		print("Rule : ",  selected_question.rule_)
		print("Init Prompt : ",  selected_question.init_prompt_)
		print("Init Prompt Rule : ",  selected_question.init_prompt_rule_)
		if(with_var == True):
			print("Variation questions : ")
			for v in selected_question.generated_questions_:
				v.print_question()

	def build_question(self, question, with_rule = False, with_CoT = True):
		res = []

		# Get the prompt with Chain of Thought (with rules or not) or without it
		res = self.prompt_generator_.build_prompt(with_CoT, with_rule)
		
  		# Build the explanation into one single string, separated by commas	
		explanation_str = ', '.join(question.explanations_)

		question_str = "-Inference : " + question.fact_ + " \n -Justifications : " + explanation_str + ". "
		if(with_rule):
			question_str + question.rule_
		res.append(self.build_cot_elem("user", question_str))

		if(with_CoT == True):
			res.append(self.build_cot_elem("assistant", "Let's translate. translation is "))
		
		return res


