"""
FOUNDATIONS OF ERROR HANDLING
=============================

What you will learn:
- What exceptions actually ARE (conceptually)
- Why prograns crash and how to prevent it
- The mechanics of try/except/else/finally
- The danger of catching too broadly vs too specifically

Core mental model:
Think of exceptions like traffic signal. A red light (exception) tells you
something went wrong and you need to handle it. Ignoring it causes a crash.
Good drivers (programmers) anticipate problems and respond appropriately.


"""


# Part 1: What is an exception? (The conceptual foundation)

"""
MENATAL MODEL: An exception is Python's way of saying "I encountered a situation
I can't handle on my own."

When you ask Python to do something impossible (divide by zero, open a file
that doesn't exist, eccess a list index  that's out of range), it creates an exception 
object that describes what went wrong.

If you don't "catch" this exception, your program crashes.

Think of it like this:
- You are cooking and realize you are out of gas
- Exception: "I can't continue this recipe"
- If no one handles it (goes to the store), dinner fails
- If someone handles it (uses a substitute), dinner continues

"""


def demonstrate_handled_exception():
    """
    This function WILL crash if you run it.

    Why? Because we are asking Python to do something impossible,
    and we are not handling the exception that results
    """

    print("\n --- UNHANDLED EXCEPTION DEMO ---")
    print("Attempting to divide by zero...")

    # This line will raise a ZeroDivisionError
    # Python literally cannot do this calculation
    result = 10 / 0     # CRASH POINT


    # This line will NEVER run because the program crashed above
    print(f"Result: {result}")



    # demonstrate_handled_exception()



# Part 2: Basic try/except - The saftey net

"""
TRY/EXCEPT is how we tell Python:
"Try to do this thing. If it fails, don't crash - do this instead."

Structure:
    try:
        # Code that might fail
    except SomeSpecificError:
        # What to do if that specific error happens
"""


def basic_error_handling():
    """
    Here we wrap risky code in a try/except block.

    This is like saying: "Try to cook with eggs. If there are no eggs
    make pancakes without eggs instead of giving up entirely.
    
    """
    print("\n--- BASIC TRY/EXCEPT DEMO ---")

    try:
        # This code might fail
        print("Attempting to divide by zero...")
        result = 10 / 0
        print(f"Result: {result}")  # Won't run if exception occurs

    except ZeroDivisionError:
        # This code runs ONLY if ZeroDivisionError happens above
        print("ERROR: Cannot divide by zero!")
        print("Handling it gracefully instead of crashing")
        result = None   # We provide a safe fallback value

    print(f"Program continues. Result is: {result}")
    print("Notice: The program didn't crash. We handled the error.")



    # basic_error_handling()


# Part 3: Specific vs Broad Exception handling (critical concept)

"""
BAD PATTERN: Catching all exceptions blindly
GOOD PATTERN: Catching specific exceptions you expect

Why does this matter?
Because different errors need different responses. Catching everything
is like saying "if anythin goes wrong while cooking, order pizza."
Sometimes you are just out of salt(minor) vs your kitchen is on fire (major).

"""


def bad_exception_handling(filename):
    """
    BAD PATTERN EXAMPLE - DO NOT DO THIS
    
    This catches ALL exceptions, which means:
    - You don't know what actually went wrong.
    - You might hide serious bugs
    - You can't respond appropiately to different problems
    """

    print(f"\n--- BAD PATTTERN: Catching too broadly ---")

    try:
        # Multiple things could go wrong here
        with open(filename, 'r') as f:
            content = f.read()
            number = int(content)   # What if content isn't a number?
            result = 100 / number   # What if number is zero?

    except Exception:   # BAD: This catches EVERYTHING
        print("Something went wrong!")
        # But WHAT went wrong? We have no idea
        # # Was it a missing file? Bad data? Division by zero?
        # We can't respond appropiately because we don't know.
        # 


def good_exception_handling(filename):
    """
    GOOD PATTERN EXAMPLE - DO THIS INSTEAD
    
    Handle specific exceptions you anticipate.
    Each exception gets appropiate handling.
    
    This is like having different reaponses for different cooking problems:
    - Out of eggs? Use substitutes
    - Oven broken? Use stovetop
    - Kitchen on fire? Call 911
    """

    print(f"\n--- GOOD PATTERN: Specific exception handling ---")


    try:
        with open(filename, 'r') as f:
            content = f.read()
            number = int(content)
            result = 100 / number
            print(f"Sucess! Result: {result}")

    except FileNotFoundError:
        # This specific error = file doesn't exist
        print(f"ERROR: File '{filename}' not found.")
        print("ACTION: Please check filename and try again.")

    except ValueError:
        # This specific error = content couldn't convert to int
        print(f"ERROR: File content is not a valid number.")
        print(f"ACTION: File shlould contain only a number.")

    except ZeroDivisionError:
        # This specific error = tried to divide by zero
        print(f"ERROR: Cannot divide by zero.")
        print(f"ACTION: File should contain a non-zero number.")

    # Notice: Each error gets a specific, helpful response
    # The user knows exactly what went wrong and how to fix it


# Part 4: The ELSE clause (Often overlooked, very useful)


"""
The ELSE clause runs ONLY if the try block suceeds (no exception  raised).

Why use it?
To seperate "risky code" from "only do this if risk suceeded" code.

Think of it like:
try: Cross the street
except CarComing: Jump back
else: Continue walking (only if crossing succeeded)
"""

def demonstrate_else_clause(dividend, divisor):
    """
    The else clause helps organize code logically.
    
    Pattern:
    - TRY: Risky operation
    - EXCEPT: handle failure
    - ELSE: Do something only if try succeded
    """

    print("\n--- ELSE CLAUSE DEMO: {devident} / {divisor} ---")


    try:
        # Risky operation
        result = dividend / divisor

    except ZeroDivisionError:
        # Handle the specific failure
        print("ERROR: Division by zero attempted")
        print("Cannot proceed with calculation")

    else:
        # This runs ONLY if no exception occured
        # Notice: result variable exists here because try suceeded
        print(f"Success! {dividend} /  {divisor} = {result}")
        print(f"The square of the result is: {result ** 2}")


        # IMPORTANT: We do additional work here ONLY because we know
        # the division succeeded. If it failed, this entire block is skipped.


# Part 5: The FINALLY clause (cleanup guarantee)

"""
The FINALLY clause ALWAYS runs, whether an exception occured or not.

Use it for cleanup operations that must happen no matter what:
- Closing files
- Releasing locks
- Cleaning up resources
- Logging that an operation finished

Think of it like:
try: Cook dinner
except BurnedFood: Order takeout
else: Enjoy your cooking
finally: Clean the kitchen (AlWAYS happens)

"""

def demonstrate_finally_clause(filename):
    """
    Finally ensures cleanup happens even if errors occur.

    In real systems, this is crucial for:
    - Closing database connections
    - Releasing file handles
    - Cleaning up temporary resources
    """

    print("\n--- FINALLY CLAUSE DEMO ---")

    file_handle = None  # Track if we opened a file
    
    try:
        print(f"Attempting to open '{filename}...'")
        file_handle = open(filename, 'r')
        content = file_handle.read()
        print(f"Sucessfully read {len(content)} characters")

    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found")

    else:
        print("File operation completed sucessfully")

    finally:
        # This ALWAYS runs, even if an exception occured
        print("FINALLY: Cleanup phase...")

        if file_handle and not file_handle.closed:
            file_handle.close()
            print("File closed properly")
        else:
            print("No file to close")

        print("Cleanup complete - resources released")

    print("Function complete\n")



# Part 6: Putting it all together - a complete pattern

def safe_number_from_file(filename):
    """
    Read a number from a file safely, with proper error handling and guaranteed cleanup
    """
    print(f"\n--- COMPLETE PATTERN DEMO: Reading from '{filename} ---'")

    file_handle = None
    number = None

    try:
        # RISKY OPERATIONS
        print("Step 1: Opening file...")
        file_handle = open(filename, 'r')

        print("Step 2: Reading content...")
        content = file_handle.read().strip()

        print("Step 3: Converting to number...")
        number = float(content)

    except FileNotFoundError:
        # SPECIFIC ERROR HANDLING
        print(f"x File {filename} does not exist")
        return None
    
    except ValueError as e:
        # Note:'as e' captures the exception object for details
        print(f"x File content is not a valid number")
        print(f" Details: {e}")
        return None
    
    except PermissionError:
        print(f"x Permission denied to read '{filename}'")
        return None
    
    else:
        # SUCESS PATH - only runs if not exceptions
        print(f"Sucessfully read number: {number}")
        print(f" The number doubled is {number ** 2}")

    finally:
        # GUARANTEED CLEANUP
        if file_handle:
            file_handle.close()
            print("File closed")
        print("--- Operation complete ---\n")

    return number


# MAIN DEMOMSTRATION

if __name__ == "__main__":
    print("=" * 80)
    print("PYTHON ERROR HANDLING FUNDAMENTALS")
    print("=" * 80)

    # Demo 1: Basic try/except
    basic_error_handling()

    # Demo 2: Specific vs braod exception handling
    # First, create a test file
    with open('test_number.txt', 'w') as f:
        f.write('42')

    good_exception_handling('test_number.txt')
    good_exception_handling('nonexistent_file.txt')

    # Demo 3: The else clause 
    demonstrate_else_clause(10, 2)  # Sucess case
    demonstrate_else_clause(10, 0)  # Error case

    # Demo 4: The finally clause 
    demonstrate_finally_clause('test_number.txt')
    demonstrate_finally_clause('missing.txt')

    # Demo 5: Complete pattern
    result = safe_number_from_file('test_number.txt')

    # Create a bad dile for testing
    with open('bad_number.txt', 'w') as f:
        f.write('not a number')

    result = safe_number_from_file('bad_number.txt')
