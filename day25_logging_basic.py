
"""
LOGGING AS A SYSTEM SKILL
==========================

What you will learn:
- Why print() is insufficient for real systems
- What logging conceptually represents
- Log levels and when to use them
- Basic logging configuration
- Logging errors with full exception details


Core mental model:
Logging is writing a narrative od what your program does for FUTURE readers.
Those readers might be:
- You, debugginh at 2 AM
- A teammate investigating production issues
- An automated monitoring system
- Audit requirements

print() is for IMMEDIATE human consumption.
logging is for RECORDED system behavior.

Read this thinking: "I am learning to make my code observable."

"""


import logging
import sys
from datetime import datetime

# Part 1: Why print() is not enough

"""
print() is great for:
- quick debugging during developmemt
- direct user interaction (CLI tools)
- learnin/teaching

print() is TERRIBLE for:
- production systems
- multi-user applications
- anything that runs attended
- systems that need debugging after the fact

why?
1. output disappears (no record)
2. can't filter by severity
3. can't rout to different destinations (files, services, etc.)
4. mixes with actual program output
5. no timestamp or context
6. can't turn on/off without code changes

"""


def demonstrate_print_limitation():
    """
    Shows why print() fails in real scenarios.

    Imagine this code running on a server. Someone reports a bug.
    You need to know what happened. But...

    """
    print("\n--- LIMITATIONS OF PRINT() ---")

    # Scenario: Processing user uploads
    files = ['documents.pdf', 'photo.jpg', 'data.csv', 'corrupted.dat']

    for filename in files:
        print(f"Processing {filename}") # When did this happen ?

        # Simulate processing
        if 'corrupted' in filename:
            print("ERROR: File is corrupted" )      # How severe?  Is it critical ?
        else:
            print(f"Sucess: {filename} processed")   # where did output go ?

    print("\nProblems with this approach:")
    print("1. No timestamps - when did errors occur?")
    print("2. No severity - is 'ERROR' critical or just a warning? ")
    print("3. No persistence - output disappears after run")
    print("4. No context - which user? which server?")
    print("5. Can't filter - all or nothing")
    print("6. Mixes with real output - hard to parse")


# Part 2: What is logging? (conceptual foundation)

"""
Logging is creating a persistent, structured record od program behavior.

Think of it like a ship's log or flight recorder:
- records what happened
- records when it happened
- records severity (routine vs emergency)
- survives the 'crash'
- can be analyzed later


In code, logging means:
- using a logging library instead of print()
- categorizing messages by severity
- including context (timestamps, source, etc.)
- routing messages to appropiate destinations

"""


def demonstrate_basic_logging():
    """
    Shows the simples logging usage

    logging.basicConfig() is the minimal setup.
    After that, you get a logger that works much better than print()

    """

    print("\n--- BASIC LOGGING DEMONSTRATION---")

    # Configure logging (do this ONCE at program start)
    logging.basicConfig(
        level=logging.DEBUG,    # Show all messages 
        format='%(asctime)s - %(levelname)s - %(message)s'
        # Format: timestamp - severity - message
    )


    # Get a logger
    logger = logging.getLogger(__name__)

    # Now use it instead of print()
    logger.debug("This is a debug message.")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    print("\nNotice:")
    print("- Each message has a timestamp")
    print("- Each message has a severity level")
    print("- Format is consistent")


    # Part 3: Log levels - the severity scale

    """
    Log levels let you categorize message severity.

    Think of them like alert systems:
    - DEBUG: Technical details for diagnosing problems (like car's diagnostic codes)
    - INFO: Routine operations (like "engine started")
    - WARNING: Something unusual but handled (like "tire pressure low")
    - ERROR: Something failed but system continues (like "radio malfunction")
    - CRITICAL: System- level failure ("engine failure")

    WHy does this matter?
    Because you want different information in different situations:
    - Development: See everything (DEBUG level)
    - Production: Only problems (WARNING+ level)
    - Incident investigation: Everything again (DEBUG level)

    You control this WITHOUT Changing code, just configuration.
    
    """

    