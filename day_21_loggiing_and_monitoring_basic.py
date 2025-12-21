
"""
LOGGING AND MONITORING IN MACHINE LEARNING WORKFLOWS

This program demonstrates how logging and monitoring form the backbone of
professional ML/AI development, enabling reproducibility, debugging, and
performance optimization


"""

# IMPORTS AND SETUP

import logging # Python's built-in logging framework - the foundation of tracking program behavior
import time # For measuring execution time and simulating delays
import numpy as np # For numerical operations and creating sample datasets
import functools as wraps # For creating decorators - functions that modify other functions
import datetime as datetime # For timestamping events and experiments
import sys # For system-level operations like file handling
import traceback # For detailed error reporting

# Optional but recommended for production monitoring

try:
    import psutil # For system resource montioring (CPU, memory, GPU)
    PUSTIL_AVAILABLE = True
except ImportError:
    PUSTIL_AVAILABLE = False
    print("Note: psutil not installed. System monitoring will be limited.")
    print("Install with: pip install psutil")

# For our ML example, we will use scikit-learn (lightweight and beginner-friendly)
try:
    from sklearn.datasets import make_classification # Generates synthetic datasets
    from sklearn.model_selection import train_test_split # Splits data into train/test
    from sklearn.linear_model import LogisticRegression # Simple classifier for demo
    from sklearn.metrics import accuracy_score, precision_score, recall_score # Performance metric
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Note: scikit-learn not installed. Using simulated ML workflow.")
    print("Install with: pip install scikit-learn")


# Part 1: Understanding logging in ML/AI Context


"""
What is logging?

Logging is the systematic recording of events, data, and state changes during program execution.
In ML/AI, logging is CRITICAL because:

1. REPRODUCIBILITY: Track exact configurations that produced specific results.
2. DEBUGGING: Identify where pipelines fail (data issues, model error, etc.)
3. EXPERIMENT TRACKING: Record hyperparameters, metrics, and outcomes
4. AUDITING: Maintain records for compliance and model governance
5. COLLABORATION: Share detailed experiment histories with team members


Unlike print() statements (whic are temporary and unstructured), logging
provides:
- persistent records (saved to files)
- different severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- structured formats (timestamps, module names, etc.)
- flexibility (easy to enable/disable without code changes)

"""

"""
LOGGING ARCHITECTURE

Python's logging system has three components:

1. LOGGER: The entry point - creates log records
    - Think of it as a "channel" for messagges
    - Multiple loggers can exist (one per module/component)

2. HANDLER: Determines WHERE logs go (console, file, database, etc.)
    - StreamHandler: Outputs to console (stdout/stderr)
    - FileHandler: Writes to a file
    - Can have multiple handlers per logger

3. FORMATTER: Defines HOW logs look (timestamp format, message structure)
    - Controls the appereance of log messages
    - Can include: timestamp, log level, module name, message

"""

"""
LOG LEVELS (from least to most severe):

DEBUG (10): Detailed diagnostic information for developers 
            Example: "Shape of input tensor: (32, 224, 224,3)"

INFO (20):  General information messages about progress
            Example: "Epoch 5/10 completed - Loss: 0.234"

WARNING (30): Something unexpected but not critical happened
             Example: "Learning rate very high (0.1) - mau caus instability"

ERROR (40): A serious problem occured, but program continues
             Example: "Failed to load checkpoint file - starting from scratch"

CRITICAL (50): A very serious error that may cause program termination
               Example: "GPU out of memory - cannot continue training" 
"""


def setup_ml_logger(experiment_name, log_level=logging.INFO):
    """
    Creates a customized logger for ML experiments with both file and and console output.

    This function demonstrates professional logging setup for ML pipelies.

    Parameters:

    experiment_name : str
        Name of the experiment (used for log filenmae and logger identification)

    log_level : int
        Minimum severity level to log (default: INFO)

    Returns:
    logger: logging.Logger
       Configure logger ready for use


    Technical Details:

    - Creates a unique logger instance (avoids conflicts with other modules)
    - Sets up TWO handlers: console (immediate feedback) and file(permanent record)
    - Uses detailed formatter with timestamps for experiment tracking

    """

    # Step 1: Create a logger with a unique name
    # logger = logging.getLogger(name) creates or retrieves a logger
    # Using experiment_name ensures each experiment has its own logger
    logger = logging.getLogger(experiment_name)

    # Step 2: Set the minimum severity level
    # Only messages at this level or higher will be processed
    # Example: if set to INFO, DEBUG messages are ignored
    logger.setLevel(log_level)

    # Step 3: Clear any existing hanflers (prevents duplicate logs)
    # This is important if the function is called multiple times
    logger.handlers = []

    # Step 4: Create a CONSOLE HANDLER (for real-time monitoring)
    # StreamHandler writes to sys.stdout (yout terminal/console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level) # COnsole shows all message at or above this level

    # Step 5: Creat a FILE HANDLER ( for permanent records)
    # FileHandler writes to a file on disk
    # Using timestamp in filenmae ensires each run creates a unique log file
    log_filename = f"ml_experiment_{experiment_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_filename, mode='W') # ''W' = overwrite if exists
    file_handler.setLevel(logging.DEBUG) # File captures EVRYTHING (including DEBUG)


    # Step 6: Create a FORMATTER (defines log message structure)
    # Format string breakdown:
    # %(asctime)s - Timestamp when log was created
    # %(name)s - Logger name (our experiment_name)
    # %(levelname)s - Severity level (INFO, ERROR, etc.)
    # %(message)s - The actual log message
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S' # Date format: YYYY-MM-DD HH:MM:SS

    )


    # Step 7: Attach formatter to both handlers
    # This ensures consistent formatting across console and file
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Step 8: Attach handlers to logger
    # Now our logger will output to BOTH console and file
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Log the logger creation itself (meta-logging!)
    logger.info(f"Logger initialized for experiment: {experiment_name}")
    logger.info(f"Log file created: {log_filename}")

    return logger
