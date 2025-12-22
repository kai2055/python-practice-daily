"""
What is the Standard library?

Python's standard library is a colletion of modules that come pre-installed
with python. You don't need to pip install them - they are always available.
 

The standard library includes modules for:
- File system operations (pathlib, os, shutil)
- Data structures (collections, dataclasses)
- Date/time handling (datetime)
- Text processing (re, string)
- And much more

Philosophy: "Batteries included" - Python gives you powerful tools out of the box.

What is pathlib and why does it exist?

pathlib is a modern, object-oriented approach to handling filesystem paths.


Historical context:
1. Early Python: Paths were just strings, manipulated with string operations
2. os.path module: Functions like os.path.join(), os.path.exists()
3. pathlib: Object-oriented, intuitive, cross-platform


Why pathlib was created:
- String manipulation of paths is error-prone and platform-specific
- os.path requires remembering many seperate functions
- pathlib provides a unified, untuitive interface


Example of the evolution:
    Old way (strings):  path = "data/" + filename
    Better (os.path):   path = os.path.join("data", filename)
    Modern (pathlib):   path = Path("data") / filename


Why pathlib over os.path?

1. Object-oriented: Paths are objects with methods, not strings with functions
2. Intuitive syntax: Use "/" operator to joins paths naturally
3. Chainable operations: path.parent.parent vs os.path.dirname(os.path.dirname(path))
4. Built-in validation: Methods like .exists(), .is_file() are clear and readable
5. Cross-platform by design: Automatically handles Windows Vs Unix path differences


When to still use os module:
- Very old Python versions (pre-3.4)
- Interfacing with legacy code that expects strings
- Some advanced operations not yet in pathlib

Rule of thumb: Default to pathlib for new code. It's cleaner and safer.

"""


# PART 2: Core Filesystem concepts

"""
What is a path?

A path is the adress or location of a file or directory in a filesystem.
Think of it like a postal address for data on your computer.


Components of a path:
- Root: The starting point (C:\ on Windows, / on Unix)
- Directories: Folders that organize files
- Filename: The actual file name
- Extension: The suffix that hints at file type (.txt, .csv, .pv)

Example path breakdown:
    /home/user/projects/data/sales.csv
    ^^^^                            ^^^
    root                            filename
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
         directories (nested folders)
                                 ^^^
                                 extension


Key insight: Directories structure your data; files hold your data

When to use which:
- Absolute: Configuration files, system paths, when you need certainity
- Relative: Project files, portable code, when flexibility is valuable


"""



# Part 3: Importing and basic usage


from pathlib import Path
import sys

print("=" * 80)
print("PATHLIB TUTORIAL: HANDS-ON EXPLORATION")
print("=" * 80)
print()


# Section 3.1: Creating Path Objects


print("SECTION 1: Creating Path Objects")
print("-" * 80)

"""
The Path class is yout main tool. You create Path objects by passing strings.

Syntax: Path(string_path)

A Path object is NOT a string - it's a rich object with methods and properties.
"""

# Create various Path objects
current_file = Path(__file__) # __file__ is the path to this script
current_dir = Path.cwd()      # cwd = Current Working Directory
home_dir = Path.home()        # User's home directory


print(f"This script: {current_file}")
print(f"Current working directory: {current_dir}")
print(f"Home directory: {home_dir}")
print()


# Create Path objects from string literals
data_dir = Path("data")
csv_file = Path("data/sales.csv")
relative_path = Path("./documents/report.txt")

print(f"Data directory path: {data_dir}")
print(f"CSV file path: {csv_file}")
print(f"Relative path: {relative_path}")

"""
IMPORTANT CONCEPT: Path objects vs strings

When you print a Path object, it looks like a string, but it's not!
    type(csv_file) -> <class 'pathlib.PosixPath> or <class 'pathlib.WindowsPath' >

You can convert:
    Path to string: str(csv_file) or csv_file.as_posix()
    String to Path: Path(): Path(string_variable)

Why this matters: Many old functions expect strings, so you may need to convert.

"""

print(f"Type of csv_file: {type(csv_file)}")
print(f"As string: {str(csv_file)}")
print(f"As POSIX string: {csv_file.as_posix()}")    # Always forward slashes
print()

# Section 3.2 The "/" Operator - joining Paths Safely

print("\nSection 2: Joining Paths with / Operator")
print("=" * 80)

"""
One of pathlib's most elegant features: the / operator for joining paths.

Instead of:
    os.path.join("data", "2024", "sales.csv")

You write:
    Path("data") / "2024", "sales.csv"


This is:
1. More readable (looks like actual paths)
2. Cross-platform (pathlib handles correct seperator)
3. Type-safe (you're working with Path ojects, not fragile strings)


You can mix Path objects and strings:
    path_obj / "filename.txt"
    "directory" / path_obj  (doesn't work - left side must be Path)

"""


# Build a complex path piece by piece
base = Path("projects")
year = "2024"
month = "december"
filename = "sales_report.csv"


# Method 1: Chain the / operator
full_path = base / year / month / filename
print(f"Built path: {full_path}")


# Method 2: Build incrementally (useful in loops or conditionals)
project_path = Path("projects")
project_path = project_path / year
project_path = project_path / month
project_path = project_path / filename
print(f"Incrementally built: {project_path}")


# Method 3: Join all at once
all_at_once = Path("projects", year, month, filename)
print(f"All at once: {all_at_once}")
print()

"""
COMMON MISTAKE: Don't do this!
            bad_path = "data" + "/" + filename          # String concatenation - OS-specific

Always use / operator or Path constructor for joining

"""


# PART 4: Interogatting paths - does it exist? what is it?


print("\nSECTION 3: Checking Path Existence and Type")
print("-" * 80)


"""
Before working with a path, you need to know:
1. Does it exist on the filesystem?
2. If it exists, is it a file or directory?

pathlib provides clear methods for this:
    .exists() - True if path exists (file OR directory)
    .is_file() - True if path exists AND is a file
    .is_dir() - True if path exists AND is a directory


CRITICAL INSIGHT:
- .exists() just checks existence
- .is_file() and .is_dir() check existence AND type
- If a path doesn't exist, .is_file() and .is_dir() return False (not an error)


"""


# Check this script itself
this_script = Path(__file__)
print(f"Checking: {this_script}")
print(f"  Exists? {this_script.exists()}")
print(f" Is file? {this_script.is_file()}")
print(f" Is directory? {this_script.is_dir()}")
print()

# Check the directory containing this script

script_dir = this_script.parent
print(f"Checking: {script_dir}")
print(f" Exists? {script_dir.exists()}")
print(f" Is file? {this_script.is_file()}")
print(f" Is directory? {script_dir.is_dir()}")
print()

# Check a path that likely doesn't exist
nonexistent = Path("this_definitely_does_not_exist_12345.txt")
print(f"Checking: {nonexistent}")
print(f" Exists? {nonexistent.exists()}")
print(f" Is file? {nonexistent.is_file()}")
print(f" Is directory? {nonexistent.is_dir()}")
print()



# PART 5: Dissecting Paths - Extracting Components

print("\nSECTIOn 4: Extracting Path Components")
print("=" * 80)

"""






"""






