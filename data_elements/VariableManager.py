import re
import random
import string

class ClassVariable:
  def __init__(self, pattern, dictionary):
    self.pattern = pattern
    self.dictionary = dictionary

class VariableManager:
  def __init__(self):
    self.class_variables = []
    self.class_variables.append(ClassVariable('__Agent__',
                                              {'Robot' : 'robot',
                                               'Pr2' : 'pr2',
                                               'Pepper' : 'pepper',
                                               'Tiago' : 'tiago'}))
    
    self.class_variables.append(ClassVariable('__Camera__',
                                              {'RealsenseL515' : 'realsense l515',
                                               'RGBCamera' : 'rgb camera',
                                               'Webcam' : 'webcam',
                                               'KinectV2' : 'kinect v2',
                                               'RealsenseD435i' : 'realsense d435i'}))
    
    self.class_variables.append(ClassVariable('__ScanablePart__',
                                              {'QRCode' : 'qr code',
                                               '2DBarcode' : '2d barcode',
                                               'QRTag' : 'qr tag',
                                               'ScanTag' : 'scan tag'}))
    
    self.class_variables.append(ClassVariable('__Gripper__',
                                              {'MechanicalHand' : 'mechanical hand',
                                               'Claw' : 'claw',
                                               'TwoFingerClaw' : 'two-finger claw',
                                               'Manipulator' : 'manipulator'}))
    
    self.class_variables.append(ClassVariable('__Handle__',
                                              {'Handle' : 'handle',
                                               'HandGrip' : 'hand grip',
                                               'Grip' : 'grip'}))
    
    self.class_variables.append(ClassVariable('__Wheel__',
                                              {'Wheel' : 'wheel',
                                               'Roller' : 'roller',
                                               'Caster' : 'caster',
                                               'PivotRoller' : 'pivot roller',
                                               'PivotWheel' : 'pivot wheel'}))
    self.variables = set()
    self.integers = set()
    self.classes = {cv.pattern for cv in self.class_variables}
    self.instances = []
    self.labeled_instances = []
      
  def addClassVariable(self, pattern, dictionary):    
    self.class_variables.append(ClassVariable(pattern, dictionary))
    self.classes = {cv.pattern for cv in self.class_variables}

  def extractVariables(self, data):

    # This handles strings, lists of strings, and lists of lists of string
    def flatten_to_string(item):
      if isinstance(item, list):
        return " ".join(flatten_to_string(i) for i in item)
      return str(item)

    text = flatten_to_string(data)

    world_pattern = r"(__.*?__)"
    int_pattern = r"(integer#\d)(?!\d)"

    self.variables.update(re.findall(world_pattern, text))
    self.integers.update(re.findall(int_pattern, text))

  def removeClassVariables(self):
    patterns_to_remove = {cv.pattern for cv in self.class_variables}
    self.variables -= patterns_to_remove

  def _generateGibberish(self):
      """Generates a random string of 2-6 letters."""
      length = random.randint(2, 6)
      # Using mostly consonants reduces the chance of forming English words
      chars = string.ascii_lowercase
      return ''.join(random.choice(chars) for _ in range(length))
  
  def generateInstances(self, count):
    self.removeClassVariables()
    self.instances = []
    self.labeled_instances = []
    
    for _ in range(count):
      instance_map = {}
      labeled_instance_map = {}
      seen_identifiers = set()

      # 1. Handle Classic Variables (__word__)
      for var in self.variables:
          while True:
            identifier = self._generateGibberish()
            if identifier not in seen_identifiers:
              seen_identifiers.add(identifier)
              break

          instance_map[var] = identifier
          label = var.strip("_")
          labeled_instance_map[var] = f"{label}_{identifier}"

      # 2. Handle Integers (Ensuring strictly increasing values)
      # We pick 'count' unique random numbers and sort them

      # Pre-sort integers to ensure integer#1 < integer#2 ...
      # This sorts ['integer#1', 'integer#2'] numerically based on the digit
      sorted_int_keys = sorted(list(self.integers), key=lambda x: int(x.split('#')[1]))
      random_vals = sorted(random.sample(range(10, 101), len(sorted_int_keys)))
      for i, key in enumerate(sorted_int_keys):
          instance_map[key] = f"integer#{random_vals[i]}"
          labeled_instance_map[key] = instance_map[key]

      # 3. Handle Class Variables
      for cv in self.class_variables:
        if cv.dictionary:
          instance_map[cv.pattern] = random.choice(list(cv.dictionary.keys()))
          labeled_instance_map[cv.pattern] = instance_map[cv.pattern]

      self.instances.append(instance_map)
      self.labeled_instances.append(labeled_instance_map)

  def instantiate(self, data, instance_id, use_label=False):
    """
    Replaces patterns in the input data with values from a specific instance.
    :param data: String or List of strings
    :param instance_id: The index of the instance to use
    :param use_label: If True, uses self.labeled_instances; else self.instances
    """
    # 1. Normalize input to a single string and clean spaces
    text = " ".join(data) if isinstance(data, list) else data
    text = " ".join(text.split())

    # 2. Select the correct mapping dictionary
    try:
      if use_label:
        mapping = self.labeled_instances[instance_id]
      else:
        mapping = self.instances[instance_id]
    except IndexError:
      return f"Error: Instance ID {instance_id} out of range."

    # 3. Create a combined regex pattern for all keys in the mapping
    # We escape the keys to handle the underscores and hashes safely
    if not mapping:
      return text
        
    pattern = re.compile("|".join(re.escape(key) for key in mapping.keys()))

    # 4. Define the replacement logic
    def replace_match(match):
      return mapping[match.group(0)]

    # 5. Perform the substitution
    return pattern.sub(replace_match, text)