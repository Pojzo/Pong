class Pet:
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)


class Dog(Pet):
    def __init__(self, name):
        super().__init__(name)


pet = Pet("Albert")
dog = Dog("Štefan")

pet.print_name()
dog.print_name()