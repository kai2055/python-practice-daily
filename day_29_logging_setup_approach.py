
"""
PYTHON LOGGING - TWO SETUP APPROACHES DEMOSTRATION

This program demonstrates:
1. Simple setup using bsicConfig()
2. Manual setup with explicit Logger, Handler and Formatter
3. Exception Logging with full traceback

Goal: Understand the difference between two approaches and see them in action.

"""

import logging
import sys

# Approach 1: Simple setup using basicConfig()


def demonstrate_basic_config():
    """
    Approach 1: Quick and easy setup - good for learning and simple scripts
    

    What basicConfig() does automatically:
    - Creates a root logger
    - Creates ONE handler (StreamHandler to console by default)
    - Creates a formatter and attaches it to the handler
    - Connects the handler to the logger

    You configure everything in ONE function call
    
    """

    print("Approach 1: Simple setup - basicConfig()")
    print("=" * 80)


    # Configure logging in one line
    # Note: force=True resets any existing configuration (useful for demos)
    logging.basicConfig(
        level=logging.DEBUG,        # Show all messages DEBUG and above
        format='%(asctime)s - %(levelname)s - %(message)s', # How messages look
        datefmt='%H:%M:%S',         # Time formate (hours: minutes: seconds
        force=True                  # Reset any previous config (for demo purposes)
    )

    # Now just use the logger directly
    # logging.debug(), logging.info(), etc. use the 'root logger'

    print("\n--- Regular Log Message ---")
    logging.debug("This is a DEBUG message - detailed diagnostic info")
    logging.info("This is an INFO message - general information")
    logging.warning("This is a WARNING mwssage - something unexpected")
    logging.error("This is an ERROR message - something failed")
    logging.critical("This is a CRITICAL message - system failure")


    # Demonstrate exception logging
    print("\n --- Exception Logging with basicConfig()---")
    demonstrate_exception_basic()

    print("\n" + "=" * 80)


def demonstrate_exception_basic():
    """
    Shows how to log exceptions with basicConfig() setup.

    logger.exception() captures:
    - The error message you provide
    - The exception type
    - The FULL TRACEBACK (call stack)
    """

    def divide_numbers(a, b):
        """Function that might cause an exception"""
        return a / b

    def process_data(value):
        """Another function that calls divide numbers"""
        result = divide_numbers(100, value)
        return result

    # Try to process data with invalid input
    try:
        # This will cause a ZeroDivisionError
        result = process_data(0)

    except ZeroDivisionError:
        # logging.exception() automatically captures the full traceback
        # This is MUCH BETTER than just the error message
        logging.exception("Failed to process data - division error occured")

        print("\nNotice above: The traceback shows:")
        print(" - Which function the error occured in (divide_numbers)")
        print(" - The chain of function calls (process_data) -> divide_numbers")
        print(" The exact line number where it failed")
        print(" The exception type and message")




# APPROACH 2: MANUAL SETUP WITH EXPLICIT COMPONENTS

def demonstrate_manual_setup():
    """
    APPROACH 2: Manual setup - gives you full control

    This approach explicitly creates:
    1. Logger - creates the log records
    2. Handler(s) - direct where logs go (you can have multiple)
    3. Formatter - structures how logs look


    WHy use this?
    - Need multile destinations (console AND file)
    - Want different formats log levels for different handlers
    - Want different log levels for different handlers
    - Building production systems or libraries
    
    """

    print("\n\n" + "=" * 80)
    print("Approach 2: Manual Setup - Explicit Logger, Handler, Formatter")
    print("=" * 80)

    # Step 1: Create a logger with a specific name
    # Using a name (not root logger) prevents conflicts with other modules
    logger = logging.getLogger('demo_app')
    logger.setLevel(logging.DEBUG)  # Logger accepts DEBUG and above

    # Clear any existing handlers (important for demos/reruns)
    logger.handlers.clear()

    # Step 2: Create a Handler - decides WHERE logs go
    # StreamHandler sends logs to console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # This handler only shows INFO and above

    # Step 3: Create a Formatter - defines HOW logs look
    # You can use different format variables to custimize the output
    formatter = logging.Formatter(
        fmt= '[%(levelname)s] %(name)s -%(message)s (line %(lineno)d)',
        # fmt includes: level, logger name, message, and linen number
        # You can add: %(filename)s, %(funcName)s, %(asctime)s, etc.
    )


    # Step 4: Attach the Formatter to the handler
    console_handler.setFormatter(formatter)

    # Step 5: Attach the Handler to the Logge
    # Now the logger will send messages through this handlers
    logger.addHandler(console_handler)

    # Step 6: Use the logger
    print("\n--- Regular Log Messages with Manual Setup ---")
    logger.debug("This is DEBUG - Handler blocks its (only INFO+)")
    logger.info("This is INFO - passes through handler")
    logger.warning("This is WARNING - passes thorugh handler")
    logger.error("This is ERROR - passes through handler")

    print("\n Note : DEBUG message didn't appear because the handler")
    print(" is set to INFO level (even though logger allows DEBUG)")

    # Demonstrate exception logging with manual setup
    print("\n --- Exception Logging with Manual Setup----")
    demonstrate_exception_manual(logger)

    print("\n" + "=" * 80)

def demonstrate_exception_manual(logger):
    """
    Shows how to log exception with manual setup
    
    Parameters"
        logger: The logger instance to use
     
    """

    def fetch_user_data(user_id):
        """Simulates fetching data that might fail"""
        # Simulate KeyError (missing key in dictionary)
        user_database = {'user_1': 'Alice', 'user_2': 'Bob'}
        return user_database[user_id]   # WIll fail if user_id not found
    
    def validate_and_process(user_id):
        """Another layer of function calls"""
        user_name = fetch_user_data(user_id)
        return user_name
    

    # Try to fetch a user that doesn't exist

    try:
        # This will cause a KeyError
        result = validate_and_process('user_9999')

    except KeyError:
        # logger.exception() automatically logs the full traceback
        # Always use this inside except blocks to capture context


        print("\nNotice above: The traceback shows all the call chain:")
        print(" validate_and_process() -> fetch_user_data() ->KeyError")
        print(" This helps you understand WHERE and WHY the error occured")





# MAIN EXECUTION

if __name__ == "__main__":
    """
    Run both demonstration to see the difference.
    """

    # Demo 1: Simple approach
    demonstrate_basic_config()

    # Demo 2: Manual approach
    demonstrate_manual_setup()

    
