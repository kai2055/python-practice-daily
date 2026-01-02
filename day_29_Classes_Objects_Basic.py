
"""
UNDERSTANDING CLASSES AND OBJECTS 
================================

This program demonstrates:
1. How to create a class (the blueprint)
2. How to create objects (actual instances from that blueprint)
3. How to pass one object to another
4. How objects can interact with each other.


We will use a simple real-world example: Dogs and Owners

"""


# Part 1: Creating our First Class - The Dog Class

class Dog:
    """
    A class is like a BLUEPRINT for creating objects.
    Think of it like a cookie cutter - the class is the cutter,
    and each object is an actual cookie made from it.
    
    """

    # The __init__ method is called automatically when you create a new object
    # 'self' refers to the specific object being created
    # Think of 'self' as "this particular dog we are creating right now"

    def __init__(self, name, breed, age):
        """
        This is the CONSTRUCTOR - it runs when we create a new Dog object
        It sets up the initial properties (attributes) of the dog.
        
        Parameters:
            name: The dog's name (string)
            breed: The dog's breed (string)
            age: The dog's age (integer)
        
        """

        # self.name means "THIS dog's name"
        # We are storing the name parameter into this dog's  name attribute
        self.name = name
        self.breed = breed
        self.age = age

        print(f"A new dog named {self.name} has been created!")


    # Methods are functions that belong to the class
    # They define what actions/behaviors objects of this class can do

    def bark(self):
        """
        A method that makes the dog bark.
        Notice we still use 'self' to access this dog's attributes.
        
        """

        print(f"{self.name} says: Woof! Woof!" )

    def get_info(self):
        """
        A method that returns information about this specific dog.
        
        """
        return f"{self.name} is a {self.age}--year--old {self.breed}"
    
    def have_birthday(self):
        """
        A method that increases the dog's age by 1.
        Notice how we can MODIFY the object's attributes.
        
        """
        self.age += 1
        print(f" {self.name} just turned {self.age} years old!.")


# Part 2: Crearting Out Secod Class - The Owner Class

class Owner:
    """
    This class represents a dog owner.
    Notice: This class will INTERACT with Dog objects!
    """

    def __init__(self, name):
        """
        Constructor for Owner class.

        Parameters:
            name: The owner's name (string)
        """

        self.name = name
        # This will store Dog objects that this owner owns
        # Starting with an empty list - owner has no dogs yet
        self.dogs = []

        print(f" Owner {self.name} has been created")

    def adopt_dog(self, dog):
        """
        THIS IS THE KEY CONCEPT: Passing one object to another!

        This method recieves a Dog OBJECT as a parameter.
        The 'dog' parameter is an actual Dog object (created from Dog class)

        Parameters:
            dog: A Dog object (not just data, but an entire object!)

        
        """ 

        # We are adding the Dog object to this owner's list of dogs
        self.dogs.append(dog)
        print(f" {self.name} adopted {dog.name}")
        # Notice: dog.name - we are accessing the Dog object's attribute!

    
    def list_dogs(self):
        """
        Show all dogs that this owner has.
        This demonstrates ITERATING over objects stored in a list.
        """

        if not self.dogs:
            print(f"{self.name} doesn't have any dogs yet.")
        else:
            print(f"\n{self.name}'s dogs:")
            # Here we are looping through DOg OBJECTS
            for dog in self.dogs:
                # For each Dog object, we call its get_info() method
                print(f" - {dog.get_info()}")


    
    def play_with_dog(self, dog):
        """
        Another example of passing an object to a method.

        Parameters:
            dog: A Dog object to play with
        
        """

        # We can call methods on the Dog object that was passed in
        print(f"\n{self.name} is playing with {dog.name}...")
        dog.bark()  # Calling the Dog object's bark() method



# Part 3: Creating Objects and Making them interact

print("\n" + "=" * 80)
print("Creating objects from classes")
print("=" * 80 + "\n")

# Creating Dog objects (instances of the Dog class)
# Syntax: object_name = ClassName(parameters for __init__)

dog1 = Dog("Buddy", "Golden Retriever", 3)
# This creates ONE specific dog with name="Buddy", breed="Golden Retriever", age=3


dog2 = Dog("Max", "German Shepherd", 5)
# This creates a DIFFERENT dog with different attributes

dog3 = Dog("Luna", "Beagle", 2)
# And another different dog


# Now we hace 3 seperate objects, each with their own attributes

print("\n" + "=" * 80)
print("Testing methods on individual objects")
print("=" * 80, "\n")


# Each object can use the methods defined in its class
dog1.bark()     # Buddy barks
dog2.bark()     # Max barks (different dog, same method)

# Each object has it's own data
print(f"\n{dog1.get_info()}")
print(f"{dog2.get_info()}")
print(f"{dog3.get_info()}")


print("\n" + "=" * 80)
print("Creating owner objects")
print("=" * 80 + "\n")

# Creating Owner objects
owner1 = Owner("Aice")
owner2 = Owner("Bob")

print("\n" + "=" * 80)
print("Passing objects to other objects - the key concept!")
print("=" * 80 + "\n")

# Here's the magic: We pass Dog Objects to Owner Objects
# The adopt_dog method recieves an entire Dog object, not just simple data

owner1.adopt_dog(dog1)  # Alice adopts Buddy (dog1 object)
owner1.adopt_dog(dog3)  # ALice adopts Luna (dog3 object)

owner2.adopt_dog(dog2)  # Bob adopts Max (dog2 object)

# Now the Owner objects have Dog objects stored inside them

print("\n Objects interacting with each other")

# The owner object can now work with its Dog objects
owner1.list_dogs()  # Alice lists her dogs
owner2.list_dogs()  # Bob lists his dogs

# An Owner can interact with a specifc Dog
owner1.play_with_dog(dog1)  # Alice plays with Buddy

# We can call methods on Dog objects through the Owner's list
print(f"\nAlice's first dog is named: {owner1.dogs[0].name}")
# owner1.dogs[0] gets the first Dog object from Alice's list
# .name accesses that Dog object's name attribute

print("\n" + "=" * 80)
print("Modififying objects")

# Objects can change their state
dog1.have_birthday()    # Buddy ages by 1 year

# The change is reflecred when we check the object
print(f"\nUpdated info: {dog1.get_info()}")




