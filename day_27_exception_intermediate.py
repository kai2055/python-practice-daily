"""
DESIGNING ERRORS INTENTIONALLY
==============================


What you will learn:
- Why catching all errors is dangerous (in depth)
- How to raise exceptions intentionally
- Creating custom exception classes
- When to re-raise exceptions vs handle them
- Error propogation as a design decision

Core mental model:
Exceptions are communication. When your code discovers something wrong,
it needs to tell someone. Sometimes that "someone" is the calling code,
sometimes it's the user, sometimes it'a a log file.

Good exception design means: clear communication about what went wrong
and giving the caller the tools to respond appropriately.

This is about THINKING LIKE A SYSTEM DESIGNER, not just making code work.

"""

# PART 1: Why blind catching is dangerous

"""
Imagine you are a chef. A customer orders a fish.

BAD APPROACH: ""If anything goes wrong, just say 'sorry, can't do it'
- Kitchen on fire? 'Sorry, can't do it.'
- Out of one ingredient? 'Sorry can't do it.'
- Dish not on menu? 'Sorry, can't do it.'

The customer has no idea what actually went wrong ot if it's fixable.

GOOD APPROACH: Specific error messages
- "Fire in the kitchen - evacuate"
- "Out of tomatoes - can sunstitute with marinara?"
- "Dish not available - may I suggest alternatives?"

Each error needs a different response. Same with code.

"""

def dangerous_blind_catching():
    """
    This demonstrates WHY catching all exceptions blindly is dangerous.

    The problem: You hide different types of errors under one blanket,
    making debugging impossible and hiding serious bugs.
    """

    print("\n--- DANGEROUS PATTERN: Blind Exception Catching ---")


    data_sources = [
        'valid_data.txt',
        'corrupted_dat.txt',
        'nonexistent_file.txt'
    ]

    for source in data_sources:
        try:
            # Multiple failure points here
            with open(source, 'r') as f:
                content = f.read()
                number = int(content)
                result = 1000 / number
                print(f" {source}: {result}")
        
        except Exception:
            # BAD: All errors look the same to the outside world
            print(f"x {source}: Failed")
            # Questions we CAN'T answer:
            # - Did the file exist?
            # - Was the content invalid?
            # - Was there a division by zero?
            # - Was there a permissions issue?
            # - Was there a bug in our code?


def better_specific_handling():
    """
    Bette approach: Handle each error type specifically.

    This gives you:
    - Better debugging information
    - Appropiate responses to different problems
    - Clear understanding of what went wrong
    """

    print("\n--- BETTER PATTERN: Specific Exception Handling ---")


    data_sources = [
        'valid_data.txt',
        'corrupted_data.txt',
        'nonexistent_file.txt'
    ]

    for source in data_sources:
        try:
            with open(source, 'r') as f:
                content = f.read()
                number = int(content)
                result = 1000 / number
                print(f" {source}: {result}")

        except FileNotFoundError:
            print(f" {source}: File missing - check path")

        except ValueError:
            print(f" {source}: Invalid data format - needs number")

        except ZeroDivisionError:
            print(f"x {source}: Cannot divide by zero")

        except PermissionError:
            print(f"{source}: Permission denied - check access right")

        # Notice: Each error gets appropiate handling
        # Debugging is noe possible because we know WHAT failed




# Part 2: Raising exceptions intentionally

"""
Sometimes YOU discover a problem and need to raise an exception.

When to raise exceptions:
1. Invalid input that you can't process.
2. Contract violations (function used incorrectly)
3. Unrecoverable errors (missing critical resources)


When NOT to raise exceptions:
1. Expected edge cases you can handle (empty list, etc)
2. Flow control (use if/else instead)
3. User errors that you can prompt for correction

"""

def validate_age(age):
    """
    Demonstrates intentionally raising exceptions for invalid input.

    Pattern: Check preconditions, raise exception if violated

    This is like a bouncer at a club - if you don't meet requirements,
    you are not getting in, and the bouncer tells you why.
    
    """

    print(f"\n--- Validating age: {age} ---")


    # Check type first
    if not isinstance(age, (int, float)):
        # RAISE an exception intentionally
        # We discovered a contract violation
        raise TypeError(
            f"Age must be a number, got {type(age).__name__}"
        )
    
    # Check range
    if age < 0:
        raise ValueError(
            "Age cannot be negative"
        )
    
    if age > 150:
        raise ValueError(
            "Age seems unrealistic (>150 years)"
        )
    
    # All checks passed
    print(f" Age {age} is valid")
    return age


def process_age_with_validation():
    """
    Shows how raising exceptions helps catch bugs early.

    Without validation, bad data propogates through your system
    causing weird bugs later. With validation, you fail fast
    with clear error messages.
    
    """

    print("\n--- DEMONSTRATION: Raising exceptions for Validation ---")

    test_cases = [
        25,          # Valid
        -5,          # Invalid: negative
        200,         # Invalid: too large
        'twenty',    # Invalid: wrong type
    ]


    for test_age in test_cases:
        try:
            validate_age(test_age)
        except (TypeError, ValueError) as e:
            # We catch the exceptions we intentionally raised
            print(f"x Validation failed: {e}")




# Part 3: Custo Exception classes

"""
Why create custom exception?

Built-in exceptions (ValueError, TypeError, etc.) are generic.
Custom exceptions let you signal SPECIFIC problems unique to your system.

Benefits:
1. More descriptive error messages
2. Easier to catch specific errors
3. Can include extra context/data
4. Makes your code's error contract clear

Think of it like custom error codes in APIs - much more useful than
generic "400 Bad Request" for everything.


"""


# Define custom exceptions at module level
class DataValidationError(Exception):
    """
    Base class for data validation errors.

    Why inherit from Exception?
    - It's the base class for all exceptions
    - Gives us all exception behavior for free
    - allows catching all our custom exceptions together if needed

    """
    
    pass

class MissingFieldError(DataValidationError):
    """
    Raised when required data field is missing.

    Notice: This inherits from DataValidationError, which inherits from Exception.
    This creates a hierarchy:
    - Exception (all errors)
        - DataValidationError (all our validation errors)
            - MissingFieldError (specificallly missing fields)
    
    """

    def __init__(self, field_name):
        self.field_name = field_name
        # Create a descriptive message
        super().__init__(f"Required field missing: '{field_name}'")


class InvalidFormatError(DataValidationError):
    """
    Raised when data format is invalid.

    This exception stores extra content (expected vs actual format)
    to help debugging.
    
    """

    def __init__(self, field_name, expected_format, actual_value):
        self.field_name = field_name
        self.expected_format = expected_format
        self.actual_value = actual_value

        super().__init__(
            f"Field '{field_name}' has invalid format. "
            f"Expected {expected_format}, got '{actual_value}"
        )



def validate_user_data(user_data):
    """
    Demonstrate using custom exceptions for domain-specific validation.

    This is realistic: when building systems, you often need to validate
    structured data (user profiles, APU requests, config files, etc.)

    Custom exceptions make the validation errors much clearer.
    
    """
    print(f"\n--- Validating user data ---")
    print(f"Input: {user_data}")

    # Required fields check
    required_fields = ['username', 'email', 'age']
    for field in required_fields:
        if field not in user_data:
            # Raise our CUSTOM exception
            raise MissingFieldError(field)
        
    # Email format check (simplified)
    email = user_data['email']
    if '@' not in email:
        raise InvalidFormatError('email', 'email address', email)
    

    # Age format check
    age = user_data['age']
    if not isinstance(age, int) or age < 0:
        raise InvalidFormatError('age', 'positive integer', age)
    
    print(" All validations passed")
    return True


def demonstrate_custom_exceptions():
    """
    Shows the power of custom exceptions in practice.

    Notice how each exception type gives us specifc, actionable information.

    """
    print("\n--- DEMONSTRATION: Custom Exceptions ---")

    test_cases = [
        # Valid data
        {'username': 'jhon', 'email': 'jhon@exampke.com', 'age': 25},

        # Missing field
        {'username': 'jane', 'email': 'jane@example.com'},

        # Invalid email format
        {'username': 'alice', 'email': 'alice@example.com', 'age': -5},

    ]

    for i, user_data in enumerate(test_cases, 1):
        print(f"\n--- Test case {i} ---")
        try:
            validate_user_data(user_data)

        except MissingFieldError as e:
            # We can catch this specific error type
            print(f"x Missing field: {e.field_name}")
            print(f" Action: Add '{e.field_name}' to user data")

        except InvalidFormatError as e:
            # And this specific error type seperately
            print(f"x Invalid format in '{e.field_name}'")
            print(f" Expected: {e.expected_format}")
            print(f" Got: {e.actual_value}")
            print(f" Action: Fix the format")

        except DataValidationError as e:
            # Or catch all out validation errors together
            print(f"x Validation error: {e}")




# Part 4: Re-raising exceptions (propogation)


"""
Sometimes you want to:
1. Detect an error
2. Do some local handling (log it, cleanup, etc.)
3. Let it propogate up to the caller

This is called "re-raising" and exception.


Real-world analogy:
You are assembling furniture. A screw breaks.
- You (local handler): Note which step failed, clean up the broken screw
- Then tell the person who asked to build it (propogate): "can't finish, broken screw at step 5"

Both levels need to know, but handle it differently

"""

def read_config_file(filepath):
    """
    Low-level function: reads configuration.

    This function's job: read the file, nothing else.
    If it fails, it SHOULD propogate the failure up.

    But we add some context before re-raising
    
    """
    print(f"\n [read_config_file] Attempting to read {filepath}")

    try:
        with open(filepath, 'r') as f:
            content = f.read()
            return content
        
    except FileNotFoundError as e:
        # We do some local handling (logging context)
        print(f" [read_config_file] ERROR: Config file not found")
        print(f" [read_config_file] Looked in: {filepath}")

        # Then RE-RAISE the exception
        # The 'raise' keyword with no arguments re-raises the current exception
        raise   # Propogates the exception upward

        # Why re-raise? Because WE can't fix a missing file
        # Our caller might have a fallback config or different handling
        # We provide context (logging) then let them decide


def initialize_application():
    """
    High-level function: starts the application

    This function calls read_config_file()
    If that fails, THIS function decides how to handle it
    (use defaults, try alternative path, abort, etc.)

    This is exception PROPOGATION in action

    """
    print("\n--- DEMONSTRATION: Exception Re-raising ---")
    print("[initialize_application] Starting application...")


    config_files = ['config.json', 'config.default.json']
    config = None


    for config_file in config_files:
        try:
            # Call function that might raise
            config = read_config_file(config_file)
            print(f" [initialize_application] Loaded config from {config_file}")
            break   # Success, stop trying

        except FileNotFoundError:
            # read_config_file raised this exception
            # We caught it here and can decide what to do
            print(f"[Initialize_appliction] {config_file} not found, trying next.....")
            continue # try next config file


        if config is None:
            # All config files failed
            print(f"\n [initialize_application] X No config files found")
            print(" [initialize_application] Cannot start application")
            # We could raise a NEW exception here
            raise RuntimeError("Application startup failed: No configuration available")
        

        print("[initialize_application] Application initialized successfully")
        return config
    


def demonstrate_selective_reraising():
    """
    Sometime you want to catch some exceptions and re-raise others.

    Pattern: handle what you can, propogate what you can't

    """
    print("\n--- DEMONSTRATION: Selective Re-raising ---")

    def process_data(value):
        """
        Process data, handling some errors but not others
        
        """

        try:
            # Multiple things can go wrong
            result = int(value) / 10
            return result
        
        except ValueError as e:
            # We CAN handle this: provide a default
            print(f" Warning: Invalid number '{value}', using 0")
            return 0
        
        except ZeroDivisionError:
            # We CANNOT handle this meaningfully, re-raise
            print(f" ERROR: Division by zero occured")
            raise   # propogate upward

        # Any other exception automatically propogates (we didn't catch it)
    
    test_values = ['100', 'abc', '0']

    for val in test_values:
        print(f"\nProcessing: {val}")
        try:
            result = process_data(val)
            print(f" Result: {result}")
        except ZeroDivisionError:
            print(f" Caller handling division by zero error")



# Part 5: Exception chaining (preserving context)


"""
When you catch an exception and raise a DIFFERENT exception
you should preserve the original exception for debugging.


Use: raise NewException() from original_exception


This creates a chain showing the full error history
"""

class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass


def query_database(query):
    """
    Simulates a databse query that might fail.

    Shows exception chaining: we raise our domain-specific exception 
    while preserving the original system exception.
    
    """

    print(f"\n [query_database] Executing: {query}")


    try:
        # Simulate: open a database connection file
        with open('database.db', 'r') as db:
            data = db.read()
            return data

    except FileNotFoundError as e:
        # The original exception (FileNotFoundError) is a low-level detail
        # We raise a high-level exception (DatabaseError) that makes sense
        # for our application domain

        print(f" [query_database] Database file not accessible")

        # CHAIN the exceptions: "from e" preserves the original
        raise DatabaseError(
            "Failed to connect to database"
        ) from e
    
        # Now the exception chain shows:
        # DatabaseError caused by FileNotFoundError
        # Debugging gets the full story


def demonstrate_exception_chaining():
    """
    Shows how chaining preserves debugging context
    
    """
    print("\n--- DEMONSTRATION: Exception Chaining ---")

    try:
        query_database("SELECT * FROM users")

    except DatabaseError as e:
        print(f"\n x Application error: {e}")
        print(f" Original cause: {e.__cause__}")
        print(f" Error type chain: {type(e).__name__} -> {type(e.__cause__).__name__}")


        # In real systems, you would log both exceptions
        # The chain gives you the full debugging story



# Main demonstration


if __name__ == "__main__":
    print("=" * 70)
    print("DESIGNING ERRORS INTENTIONALLY")
    print("=" * 70)



    # Create test files
    with open('validate_data.txt', 'w') as f:
        f.write('10')
    with open('corrupted_data.txt', 'w') as f:
        f.write('not a number')

    # Demo 1: Danger of blind catching
    dangerous_blind_catching()
    better_specific_handling()

    # Demo 2: Raising exceptions intentionally
    process_age_with_validation()

    # Demo 3: Custom exceptions
    demonstrate_custom_exceptions()

    # Demo 4: Re-raising and propogation

    try:
        initialize_application()
    except RuntimeError as e:
        print(f"\n x Fatal error: {e}")


    demonstrate_selective_reraising()


    # Demo 5: Exception chaining
    demonstrate_exception_chaining()


