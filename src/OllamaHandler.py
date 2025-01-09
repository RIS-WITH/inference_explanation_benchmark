from ollama import chat
from ollama import ChatResponse
import copy

class OllamaHandler:
	def __init__(self, model):
		self.model_ = model
	
	def build_cot_elem(self, role, tokens):
		res_elem = {}
		res_elem["role"]= role
		res_elem["content"] = tokens
		return res_elem

	def build_and_call(self, main_prompt, current_question, with_CoT = True):
		formatted_question = self.build_question(main_prompt, current_question, with_CoT)
		#print("\t\tformatted question : ", formatted_question)
		answer = self.call(formatted_question, False, False)
		return answer
     
	def build_question(self, main_prompt, current_question, with_CoT = True):

		formatted_question = []
  
		if(with_CoT == True):
			formatted_question = copy.deepcopy(main_prompt)  # need to do a deepcopy otherwise it modifies the initial prompt
			formatted_question.append(self.build_cot_elem("user", current_question))
			formatted_question.append(self.build_cot_elem("assistant", "A: Let's translate. translation is "))
		else:
			init_prompt = copy.deepcopy(main_prompt[0]) # add the initial prompt
			init_prompt['content'] += "\nThe inference to explain is : " + current_question + "Let's translate." # add the question
			
			formatted_question.append(init_prompt)
			#formatted_question.append(self.build_cot_elem("assistant", "A: Let's translate. translation is "))
			
		return formatted_question

	def call(self, question, verbose = False, full_verbose = False):
		# with the argument keep_alive at 0, it unloads from meory each time, with keep_alive = 1, it remains on memory for 5min
		
		response: ChatResponse = chat(model=self.model_, messages=question, stream=False, options={ "temperature":0}, keep_alive = 1)
		
		if(verbose == True):
			if(full_verbose == True):
				print("question is : ")
				for elem in question:
					print("\t--", elem)
				print("answer is : ", response)
			else:
				print("question is : ", question[-2]['content'])
				print("answer is : ", response['message']['content'])
		
		return response['message']['content']