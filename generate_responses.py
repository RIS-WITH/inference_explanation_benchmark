from src.OllamaHandler import OllamaHandler
from src.AnswerGenerator import AnswerGenerator

if __name__ == '__main__':
    # models in the paper
    models = ["llama3.2:3b"] #, "llama3.1:8b", "gemma2:2b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"]  
  
    directory_path = "/home/gsarthou/Documents/LAAS/Code/inference_explanation_benchmark/dataset_2026"

    generator = AnswerGenerator(directory_path)

    for model in models:
      ollama = OllamaHandler(model)

      generator.generate(ollama, model)