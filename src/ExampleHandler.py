class Example():
    def __init__(self, question, answer, rule):
        self.question_ = question
        self.answer_ = answer
        self.rule_ = rule

class ExampleHandler():
    def __init__(self, examples = None):
        self.examples_ = []
        for example in examples:
            self.add_example(example[0], example[1], example[2])
    
    def add_example(self, question, answer, rule):
        new_example = Example(question, answer, rule)
        self.examples_.append(new_example)
        
    def print_example(self, id):
        selected_example = self.examples_[id]
        print("Example n°" + str(id) + " is :")
        print(" -- question : ", selected_example.question_)
        print(" -- answer : ", selected_example.answer_)
        print(" -- rule is : ", selected_example.rule_)