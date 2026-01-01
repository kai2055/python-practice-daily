

"""
Private Functions in Python: A complete lesson
===============================================


What you will learn?
After reading and running this file, you will understand:
- what "private" means in Python (it's about convention, not enforcement)
- how to single underscore (_method) for "protected" methods
- how to use double underscore (__method) for "private" methods.
- what name mangling is and how Python implements it.
- when and why to use each type of privacy convention.
- best practices for organizing class methods by visibility


What are private functions in python?
In python, there's no true "private" like in Java or C++. Instead, Python uses
naming conventions to signal intent:
- No underscore (method): Public - intended for external use
- Single underscore (-method): Protected - internal use,  but accessible
- Double underscore (__method): Private - Python mangles the name to dicourage access.

Think of it like this:
- Public methods are the "front door" of your class
- Protected methods are the "staff only" door - you can go in, but you probably shouldn't
- Private methods are the "maintainence room" - Python makes it harder to access


"""


# Section 1: Basic class with Public Methods Only

# These are the methods users of your class should call


class BankAccount_V1:
    """A simple bank account with only public methods."""

    def __init__(self, owner, balance=0):
        """
        Initialize a bank account.

        Args:
            owner: Name of the account holder
            balance: Starting balance (default 0)

        """
        self.owner = owner # Public attribute - anyone can access this
        self.balance = balance # Public attribut - anyone can access this


    def deposit(self, amount):
        """
        Public method - intended for external use

        This is a method that users of this class SHOULD call.
        No underscores means "please use this method"
        
        """

        # Add the amount to the balance
        self.balance += amount
        print(f"Deposited ${amount}. New balance: ${self.balance}")

    
    def get_balance(self):
        """
        Public method - safe for anyone to call

        This is another public method. It just returns information,
        so it's perfectly safe for external use.
        """

        return self.balance
    
# Let's test the public methods
print("=" * 80)
print("DEMONSTRATION 1: Publuc Methods")
print("=" * 80)


# Create an account - this uses the public __init__ method
account_v1 = BankAccount_V1("Alice", 100)

# Call public methods - this is exactly what they are designed for
account_v1.deposit(50)  # works perfectly - this is intended usage
print(f"Balance: ${account_v1.get_balance()}")  # Also works perfectly
print()



# Section 2: Adding Protected Methods (Single Underscore)

# Now we will add "protected" methods using a SINGLE underscore prefix.
# The single underscore means: "This is internal. You CAN access it,
# but you probably shouldn't unless you know what you are doing."


class BankAccount_V2:
    """
    Bank account with protected helper methods
    """
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self._transaction_count = 0     # Protected attribute - single underscore


    def deposit(self, amount):
        """Public method that uses a protected helper"""
        # Before accepting the deposit, validate it using our protected method
        if self._validate_amount(amount):  # calling our protected method
            self.balance += amount
            self._transaction_count += 1    # Update protected attribute
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print(f"Invalid deposit amount: ${amount}")


    def _validate_amount(self, amount):
        """Protected method - internal validation logic
        
        The single underscore says: "This is a helper method for interna use.
        You CAN call it from outside, but it's not part of the public interface.
        It might change in future versions without warning."

        Why protected, not public?
        - It's an implementation detail
        - External users don't need to call this directly.
        - We want flexibility to change how validation works later
        """ 

        # Validation logic: amount must be positive
        return amount > 0
    
    def get_stats(self):
        """Public methid showing account statistics."""
        return f"Balance: ${self.balance}, Transactions: {self._transaction_count}"

print("=" * 80)
print("DEMONSTRATION 2: Protected Methods (Single Underscore)")
print("=" * 80)

account_v2 = BankAccount_V2("Bob", 200)

# Using public methods - the intended way
account_v2.deposit(75)  # This works - public method
account_v2.deposit(-10)     # This will be rejected by internal validation
print(account_v2.get_stats())      # Public method works fine


# Now let's try accessing the protected method directly
# Python ALLOWS this, but the underscore is a signal that we shouldn't
print("\nAccessing protected method directly (possible but discouraged:)")
result = account_v2._validate_amount(100)   # This works! No error
print(f"Direct call to _validate_amount(100): {result}")
print("^ Notice: No erro! Single underscore is just a convention, not enforcement")
print()



# Section 3: Adding Private Methods (Double underscore + Name Mangling)

# Now for the main topic: PRIVATE methods with DOUBLE underscores.
# Python uses "name mangling" to make these harder (but not impossible) to access


# NAME MANGING EXPLAINED:
# When you write a method like __calculate(), Python internally renames it to
# _ClassName__calculate(). This prevents accidental access and name conflicts
# in subclass, but it's still not true "private" - more hidden.


class BankAccount_V3:
    """Bank account with private methods demonstrating name mangling."""

    def __init__(self, ownner, balance=0):
        self.owner = ownner
        self.balance = balance
        self._transaction_count = 0 # Protected - single underscore
        self.__pin = "1234"     # Private - double underscore (name mangled)


    def deposit(self, amount):
        """Public method"""
        if self._validate_amount(amount):   # Protected method (internal)
            self.balance += amount
            self._transaction_count += 1

            # NOW we call a PRIVATE method to log this internally
            self.__log_transaction("deposit", amount)  # Private method
            print(f"Deposited ${amount}. New balance: ${self.balance}")


    def withdraw(self, amount, pin):
        """Public method that requires PIN verification"""
        # Use our private authentication method
        if self.__verify_pin(pin):  # Calling private method
            if amount <= self.balance:
                self.balance -= amount
                self.__log_transaction("withdraw", amount)  # Private logging
                print(f"Withdrew ${amount}. New balance: ${self.balance}")
            else:
                print("Insufficient funds!")
        else:
            print("Invalid PIN !")


    def _validate_amount(self, amount):
        """Protected method - same as before"""
        return amount > 0
    

    def __verify_pin(self, pin):
        """Private method - PIN verification logic.
        
        Why PRIVATE (double underscore)?
        - This is sensitive security logic.
        - We don't want it called directly from outside
        - We don't want subclasses to accidentally override it.
        - The double underscore makes it much harder to access

        This is name-mangled to: _BankAccount_V3__verigy_pin()
        """

        # Simple PIN check (in real code, this would be more secure)
        return pin == self.__pin
    

    def __log_transaction(self, transaction_type, amount):
        """Private method - internal logging
        
        Why private?
        - This is purely internal bookeeping
        - External code should never need to call this
        - We might change the logging format later without affeccting users.

        This is name-mangled to : _BankAccount_V3__log_transaction()

        """

        # In a real application, this might write to a file or database
        print(f"    [LOG] {transaction_type}: ${amount}")




print("=" * 80)
print("DEMONSTRATION 3: Private Methods (Double Underscore)")
print("=" * 80)


account_v3 = BankAccount_V3("Charlie", 500)

# Using public methods - they internally call private methods
print("Using public methods (these work):")
account_v3.deposit(100)     # This works - calls __log_transaction internally
account_v3.withdraw(50, "1234") # This works - calls __varify_pin internally
print()


# Now let's try to call the private methods directly
print("Attempting to call private methods directly (will fail)")
try:
    # Try to call __log_transaction directly - also fails!
    account_v3.__verify_pin("1234")
except AttributeError as e:
    print(f"Error calling __verify_pin: {e}")
    print("^ The method doesn't exist with this name due to name mangling!")

try:
    # Try to call __log__transaction directly - also fails
    account_v3.__log_transaction("test", 10)
except AttributeError as e:
    print(f"Error calling __log_transaction: {e}")
    print("^ Same issue - name mangling prevents direct access!")
print()



# Section 4: Understanding Name Mangling (How to see it)

# Let's prove that name mangling actually happens and show what the
# "real" names of private methods are


print("=" * 80)
print("DEMONSTRATION 4: Name Mangling Revealed")
print("=" * 70)

print("All attributes and methods of account_v3:")
# The dir() function shows ALL attributes, including mangled names
all_attributes = dir(account_v3)


# Filter to show only the methods we care about
print("\nPublic methods (no underscore):")
for attr in all_attributes:
    if not attr.startswith('_') and callable(getattr(account_v3, attr)):
        print(f" - {attr}")


print("\nProtected methods (single underscore):")
for attr in all_attributes:
    if attr.startswith('_') and not attr.startswith('__') and callable(getattr(account_v3, attr)):
        print(f" - {attr}")



"""

print("\nPrivate methods (double underscore - MANGLED NAMES):")
for attr in all_attributes:
    # Name-mangled attributes look like: _ClassName__methodname
    if attr.startswith('_BankAccount_V3__') and callable(getattr(account_v3, attr)):
        print(f"  - {attr}")
        # Extract the original name
        original_name = "__" + attr.split('__', 2)[2]
        print(f"    ^ This was originally named: {original_name}")


"""

# We CAN access private methods if we use the mangled name, but we shouldn't
print("Accessing private method using mangled name (possible but wrong:)")
# This works, but violates the intent of privacy
result = account_v3._BankAccount_V3__verify_pin("1234")
print(f"account_v3._BankAccount_v3__verify_pin('1234)) = {result}")
print("^ This works, but you should NEVER do this in real code!")
print("THe double underscore is a clear signal: 'DOn't touch this!' ")
print()

    

