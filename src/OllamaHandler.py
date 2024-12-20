from ollama import chat
from ollama import ChatResponse

class OllamaHandler:
	def __init__(self, model):
		self.model_ = model
	
	def build_cot_elem(self, role, tokens):
		res_elem = {}
		res_elem["role"]= role
		res_elem["content"] = tokens
		return res_elem

	def build_question(self, main_question, current_question):
		formatted_question = main_question["init_prompt"]
		formatted_question.append(self.build_cot_elem("user", current_question))
		formatted_question.append(self.build_cot_elem("assistant", "A: Let's translate. translation is "))
        
		return formatted_question

	def call(self, question, verbose = False):
		# with the argument keep_alive at 0, it unloads from meory each time, with keep_alive = 1, it remains on memory for 5min
		
		response: ChatResponse = chat(model=self.model_, messages=question, stream=False, options={ "temperature":0}, keep_alive = 1)
		
		if(verbose == True):
			print("question is : ", question[-2]['content'])
			print("answer is : ", response['message']['content'])
   
		return response['message']['content']