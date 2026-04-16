from src.OllamaHandler import OllamaHandler
from src.AnswerGenerator import AnswerGenerator
import config

if __name__ == '__main__':
    generator = AnswerGenerator(config.DATASET_DIR)

    for model in config.MODELS:
      ollama = OllamaHandler(model)

      generator.generate(ollama, model)