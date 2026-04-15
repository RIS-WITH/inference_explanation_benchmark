from ollama import chat
from ollama import ChatResponse

class OllamaHandler:
	def __init__(self, model):
		self.model_ = model

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