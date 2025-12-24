"""
Data Quality in CSV Files

What is data quality?
---------------------
Data quality refers to the fitness of data for its intended use. High-quality
data is:
- Accurate: Correctly represents reality
- Complete: No missing critical information
- Consistent: Follows the same format and rules throughout
- Valid: Conforms to expected formats, ranges, and business rules
- Unique: No unintended duplicates


Why data quality matters?
------------------------
1. INCORRECT ANALYSIS
    - Missing values can skew averages and statistics
    - Wrong data types prevent mathematical operation
    - Duplicates inflate counts and distort patterns

2. BROKEN PIPELINES
    - Unexpected formats crash automated systems
    - Type mismatches cause processing failures
    - Invalid values trigger exceptions in production

3. MISLEADING RESULTS
    - Bad data leads to bad decisions
    - Models trained on poor data make poor predictions
    - Reports based on dirty data misinform stakeholders

    
THE GOLDEN RULE:
------------------
Always validate and clean data BEFORE analysis or modeling.
Data quality checks should be the FIRST step in any data pipeline.


DETECTION vs. FIXING
--------------------
- DETECTION: Finding problems in data (what this program focuses on)
- FIXING: Correcting ot handling those problems (requires domain knowledge)


This program teaches you to DETECT issues. Fixing requires understanding:
- Business context (what values make sense?)
- Downstream use (how will this data be used?)
- Stakeholders requirements (what's acceptable)

Let's explore common data quality issues in CSV files..

"""

import pandas as pd
import numpy as np

# Part 1: Creating a sample dataset with intentional quality issues

"""
Why we are creating artifcial data:
-----------------------------------------
To learn data quality concepts, we need controlled examples where we KNOW 
what problem exists. In real projects, you will applu those detection techniques
to actual data where problems are hidden.

This sample dataset a customer database for an e-commerce company.
We are intentionally introducting every common data quality issue so you 
can see how to detect each one.

"""

# Create a dictionary representing out problematic dataset
# Each key is a column name, each value is a list of data for that column

problematic_data = {
    # Customer ID column - will have duplicates (a serious problem!)
    'customer_id': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1005],
    
    # Name column - has inconsistent formatting (spaces, casing issues)
    'customer_name': ['John Doe', 'jane smith', '  Bob Wilson  ', 'Alice Brown', 
                      'CHARLIE DAVIS', 'Emma Watson', 'Frank Miller', 'Grace Lee',
                      'Henry Ford', 'Alice Brown'],
    
    # Age column - has missing values (None), negative values, and wrong type (string)
    'age': [25, None, 45, -5, 67, '30', 22, 150, 33, 28],
    
    # Email column - has missing values and invalid formats
    'email': ['john@email.com', 'jane.email.com', None, 'alice@email.com',
              'charlie@email', 'emma@email.com', None, 'grace@email.com',
              'henry@email.com', 'alice@email.com'],
    
    # Purchase amount - has outliers and missing values
    'purchase_amount': [50.00, 75.50, 1000000.00, None, 120.00, 85.30, 
                        45.00, None, 95.00, 120.00],
    
    # Region column - completely empty (a useless column)
    'region': [None, None, None, None, None, None, None, None, None, None],
    
    # Status column - has a constant value (not useful for analysis)
    'status': ['active', 'active', 'active', 'active', 'active', 
               'active', 'active', 'active', 'active', 'active']
}


# Convert dictionary to pandas DataFrame
# A DataFrame is like a spreadshert in Python - rows and columns of data
df = pd.DataFrame(problematic_data)

print("=" * 80)
print("Original dataset with quality issues")
print("=" * 80)
print(df)
print("\n")


# Part 2: Missing values


"""
What are missing values?
-------------------------
Missing values are absent data points, represented as None, NaN (Not a Number),
or empty strings. They appeat as "NaN' in pandas DataFrames.

Why do they happen?
---------------------
- Users skip optional from fieldds
- Sensors fail to record measurements
- Data integration errors during ETL (Extract, Transform, Load)
- Manual data entry mistakes
- System crashes during data collection


Why do they matter?
--------------------
- Many mathematical operations fail with missing values
- Machine learning algorithms can't process them directly
- Statistics like mean/median can be skewed
- Missing values might indicate deeper data collection problems

How to detect:
-------------
pandas provides built-in methods to find missing values across entire datasets

"""

print("=" * 80)
print("Detecting missing values")
print("=" * 80)

# Check if any value in  each column is missing
# This returns a Series with column names and Tru/False for missing values
has_missing_values = df.isnull().any()
print("\nColumn with missing values:")
print(has_missing_values)

# Count how many missing values in each column
# This is more informative than just True/False
missing_value_counts = df.isnull().sum()
print("\nNumber of missing values per column:")
print(missing_value_counts)

# Calculate percentage of missing values (useful for large datasets)
# If 80% of a column is missing, you might drop that column entirely
total_rows = len(df)
missing_percentage = (df.isnull().sum() / total_rows) * 100
print("\nPercentage of missing values per column")
print(missing_percentage)


"""
COMMON SOLUTIONS FOR MISSING VALUES:
------------------------------------

1. DELETION (Remove missing data)
    - Drop rows: When few rows have missing values
    - Drop columns: When most values in a column are missing
    - When to use: Small percentage of data affected
    - When NOT to use: Losing too much data, missing data is informative


2. IMPUTATION (Fill in missing values)
    - Mean/Median: For numerical data (age, income, etc.)
    - Mode: For categorical data (most common category)
    - Forward fill: Use previous value (time series data)
    - Model-based: Predict missing values using other columns
    - When to use: Significant amout of missing data, pattern is random
    - When not to use: Missing data is not random, it has meaning


3. FLAG CREATION (Keep track of what was missing)
    - Create a new column: "was_missing_age" = True/False
    - Then impute the original column
    - Why: Preserves information that data was missing (might be important!)

REAL-WORLD EXAMPLE:
If customer email is missing:
- can't send emails (business problem)
- Might indicate customer doesn't want contact (business insight)
- Could be data entry error (data quality issue)

The solution depends on understanding  WHY it's missing!

"""

print("\n")


# Part 3: Data type issues

"""
What are data type issues?
--------------------------------
Data stored in the wrong type for its intended use. For example:
- Numbers stored as strings ('30' insteadd of 30)
- Dates stored as text
- Categories stored as numbers


Why do they happen?
---------------------
- CSV files have no type information (everything starts as text)
- pandas makes guesses about types when reading
- User input allows text in number fields
- Inconsistent data entry (some rows have '30', others have 30)

Why do they matter?
----------------------
- can't perform mathematical operations on strings
- comparisons work incorrectly ('9' > '10' is True in string comparison!)
- Aggregations (sum, mean) fail or give wrong results
- Memory waste (strings use more memory than numbers)

HOW TO DETECT:
-------------------------
Check the dtypes (data types) of each column and compare to expectation

"""

print("=" * 80)
print("Detecting data type issues")
print("=" * 80)

# Let's examine the 'age' column specifically
# We expect age to be numeric, but let's check each value's type
print("\nExamining 'age' column value types:")
for index, value  in enumerate(df['age']):
    print(f"Row {index}: value={value}, type={type(value)}")



"""
NOTICE THE PROBLEM:
In the age column, we have:
- integers (25, 45)
- None (missing value)
- strings ('30')

This mixed-type column will cause problems in calculations!

COMMON SOLUTIONS FOR DATA TYPE ISSUES:
--------------------------------------------

1. TYPE CONVERSION (Cast to correct type)
    - pd.to_numeric(): Convert to numbers, can handle errors
    - pd.to_datetime(): Convert to dates
    - .astype(): Force conversion to specific type
    - When to use: Data can be meaningfully converted
    - When NOT to use: Conversion loses important information

2. VALIDATION AT INGESTION (Prevent wrong types from entering)
    - Define schemas before reading data
    - Use dtype parameter in pd.read_csv()
    - Reject or flag rows with wrong types
    When to use: You control data entry/import
    When not to use: working with legacy data

3. SEPERATE CLEANING STEP (Fix then convert)
   - Remove non-numeric characters
   - Standardize formats
   - Then convert to proper type
   - When to use: Patterns in bad data (e.g., '1,000' -> 1000)


REAL-WORLD EXAMPLE:
If age is stored as string:
- mean(age) will fail
- age > 18 comparison works incorrectly
- Sorting gives wrong order ('9' > '100' as strings)

Solution: Convert to numeric, handle errors (maybe mark as missing)

"""

# Part 4: Duplicate rows


"""
What are duplicate rows?
----------------------
Two or more rows that are completely identical across all columns

Why do they happen?
----------------------
- Users submit forms multiple times (clicking "submit" twice)
- Data import errors (same file loaded twice)
- System glitches during data collection
- Merge/join operations create unintended duplicates

Why do they matter?
-------------------
- Inflate counts and statistics (total slaes appears higher)
- Duplicate emails/contacts (sending same message twice)
- Waste storage space
- Violate business logic (one order shouldn't appear twice)

HOW TO DETECT:
--------------
pandas can identify duplicate rows across all columns or specific columns

"""

print("=" * 80)
print("Detecting duplicate rows")
print("=" * 80)

# Check if each row is a duplicate of a previous row
# Return True/False for each row (True = this row is a duplicate)
# keep = 'first' means the first occurence is NOT marked as duplicate
duplicate_mask = df.duplicated(keep='first')
print("\nWhich rows are duplicates?")
print(duplicate_mask)

# Count total number of duplicate rows
number_of_duplicates = duplicate_mask.sum()
print(f"\nTotal duplicate rows: {number_of_duplicates}")

# Show the actual duplicates rows
if number_of_duplicates > 0:
    print("\nDuplicate rows:")
    print(df[duplicate_mask])

"""
COMMON SOLUTIONS FOR DUPLICATE ROWS:
------------------------------------------------

1. DROP DUPLICATES (Remove exact copies)
    - df.drop_duplicates(): Keep first occurence, remove rest
    - When to use: Duplicates are clearly errors
    - When not to use: Duplicates might be legitimate (multiple purchases)

2. AGGREGATE DUPLICATES (Combine transformation)
    - Sum amounts for duplicate orders
    - Take most recent date
    - When to use: Duplicates represent same entity, different attributes
    - When NOT to use: Duplicates are independent events

3. FLAG AND INVESTIGATE (Mark but don't remove)
    - Add column: 'is_duplicate' = True/False
    - Manual review of flagged records
    - When to use: Uncertain if duplicates are errors
    - When not to use: clear duplication errors, large volume


REAL WORLD EXAMPLE:
If a customer appears twice with identical info:
- Same customer shouldn't be in database twice
- But two purchases by same customer are valid!

Solution depends on context: customer table vs transaction table

"""

print("\n")


# Part 5: Duplicate identifiers (IDs/KEYS)


"""
What are duplicate identifiers?
---------------------------------
Multiple rows sharing the same ID or unique key, even if other columns differ.
This is MORE SERIOUS than general duplicates because IDs should be unique!

WHY DO THEY HAPPEN?
---------------------------
- Auto-increment ID systems fail or reset
- Manual ID assignment with human error
- Data merges from multiple systems with overlapping IDs
- System bugs in ID generation


WHY DO THEY MATTER?
---------------------------
- Breaks database relationships (foreign keys become ambiguous)
- Can't uniquely identify records
- JOIN operations produce unexpected results
- Violates fundamental data integrity principles
- In our example: customer_id MUST be unique per customer


HOW TO DETECT
Check specific columns that should be unique (IDs, email addresses, etc. )

"""

print("-" * 80)
print("Detecting duplicate identifiers")
print("=" * 80)


# Check for duplicate customer_ids specifically
# subset=['customer_id'] means "only look at this column for duplicates"
duplicate_ids = df.duplicated(subset=['customer_id'], keep=False)
# keep=False means mark ALL occurences as duplicates (not just later ones)

print("\nRows with duplicate customer_id:")
print(df[duplicate_ids])

# Count unique IDs vs total rows
unique_id_count = df['customer_id'].nunique()    # nunique = number of unique values
total_row_counts = len(df)
print(f"Unique customer_ids: {unique_id_count}")
print(f"Total rows: {total_row_counts}")
print(f"Duplicate IDs exist: {unique_id_count < total_row_counts}")

# Find which specific IDs are duplicated 
# value_counts() how many times each ID appears
id_counts = df['customer_id'].value_counts()
# Filter to show only IDs that appear more than once
duplicated_id_values = id_counts[id_counts > 1]
print("\nID Values that appear multiple times: ")
print(duplicated_id_values)

"""
COMMON SOLUTIONS FOR DUPLICATE IDENTIFIERS:
------------------------------------------------

1. REGENERATE IDs (create new unique IDs)
    - generate sequential IDs: 1,2,3 ........
    - generate UUIDs: universally unique identifiers
    - when to use: Old Ids are meaningless or corrupted
    - when not to use: Ids refrence external systems

2. MERGE RECORDS (Combine duplicates into one)
    - take most complete record
    - combine information from all duplicates
    - when to use: duplicates represent same real entity
    - when not to use: duplicates are actually different entities

3. INVESTIGATE AND MANUALLY FIX (requires domain knowledge)
    - are these the same customer or different customer?
    - which record is the correct/most recent?
    - update one ID to be unique
    - when to use: small numbers of duplicates, high-value data
    - when not to use: Large scale, low value per record

4. REJECT DATA (fail the import)
    - don't load data with duplicate IDs
    - force source system to fix
    - when to use: production system with strict requirements
    - when not to use: historical/analytical work


"""

print("\n")




# Part 6: Inconsistent formatting

"""
What is inconsistent formatting?
--------------------------------------------
Same conceptual data represented in different formats:
- "Jhon Doe" vs "jhon doe" vs "JHON DOE" vs "   jhon doe  "
- '123-456-7890' vs '(123) 456-7890' vs '1234567890'
- "New York" vs "NY" vs "new york"


Why does it happen?
----------------------
- Manual data entry (different people, different styles)
- Multiple data sources with different standards
- No validation rules during data collction
- copy-paste from different systems


Why does it matter?
-------------------------
- Grouping/aggregation treats them as different values
- "Jhon Doe" != "jhon doe" to a computer
- Duplicate detection fails
- Joins/matches fail
- User-facing displays look unprofessional

How to detect:
------------
Look for variations that should be the same value

"""

print("=" * 80)
print("Detecting inconsistent formatting")
print("=" * 80)



# Examine the customer_name column
print("\nCustomer name (notice formatting differences)")
print(df['customer_name'].tolist())

# Check for leading/trailing whitespace
# str.strip() removes spaces; if result differs, there were spaces
has_whitespace = df['customer_name'] != df['customer_name'].str.strip()
print("\nRows with leading/trailing whitespace in name:")
print(df[has_whitespace]['customer_name'].tolist())

# Check for case inconsistencies
# Compare original to lowercase version
print("\nUnique name (case-sensitive)")
print(df['customer_name'].unique())

print("\nUnique names (case-insensitive):")
# Convert to lowercase to see if names are duplicates except
print(df['customer_name'].str.lower().unique())



"""
COMMON SOLUTIONS FOR INCONSISTENT FORMATTING
------------------------------------------------------

1. Standardize case (Make consistent)
    - .str.lower(): convert all to lowercase
    - .str.upper(): convert all to uppercase
    - .str.title(): convert to Titile Case
    - when to use: case doesn't matter for meaning (names, cities)
    - when not to use: case is meaningful (product codes, IDs)

2. Strip whitespace (remove extra spaces)
    - .str.strip(): remove leading/trailing spaces
    - .str.replace(): remove all extra spaces
    - when to use: always! whitespace is rarely meaningful
    - when not to use: fixed-width formats where spaces matter

3. Apply standard formats (define rules)
    - Phone: (123) 456-7890
    - Dates: YYYY-MM-DD
    - Country codes: Use ISO standards
    - when to use: you have organizational standards
    - when not to use: accepting external data "as is"

4. FUZZY MATCHING (find similar values)
    - algorithmns to find "close enough" matches
    - "jhon doe" might match "JHON DOE"
    - when to use: high-value data, name matching
    - when not to use: exact matches required, large scale

"""

# Part 7: Constant and empty columns

"""
What are constant/empty columns?
----------------------------------------------
- Empty column: All values are missing (None/NaN)
- Constant column: All values are exactly same

Why do they happen?
-----------------------------------------
- Columns planned but never populated
- Legacy columns no longer used
- Data export includes unused fields
- Feature that hasn't been implemented yet
- All customers have same value from some attribute


Why do they matter?
--------------------------
- Waste storage space and memory 
- slow down processing (unnecessary data to load)
- confuse analysis (why is this column here?)
- No analytical value (can't learn from constants)
- In machine learning: constant features have zero predictive power

How to detect:
-----------
Check if all values in a column are the same or all missing

"""

print("=" * 80)
print("Detecting constant and empty columns")
print("=" * 80)


# Check for completely empty columns
# A column is empty if all values are NaN/None
empty_columns = []
for column in df.columns:
    if df[column].isnull().all():   # .all() = True if ALL values are True
        empty_columns.append(column)

print(f"\nCompletely empty columns: {empty_columns}")

# Check for constant columns (all same value, ignoring NaN)
# A column is constant if it has only one unique value (beside NaN)
constant_columns = []
for column in df.columns:
    # nunique(dropna=True) counts unique values, ignoring missing values
    unique_count = df[column].nunique(dropna=True)
    if unique_count == 1: # Only one unique value
        constant_columns.append(column)
        constant_value = df[column].dropna().iloc[0]    # Get that one value
        print(f"\nColumn '{column}' is constant with value: {constant_value}")

print(f"\nConstant value columns: {constant_columns}")


# Show statistical summary to spot constant/empty columns
print("\nColumn value diversity:")
for column in df.columns:
    unique = df[column].nunique(dropna=False)   # Count including Nan as unique
    total = len(df)
    print(f"{column}: {unique} unique values out of {total} rows")



"""
COMMON SOLUTIONS FOR CONSTANT/EMPTY COLUMNS:
-------------------------------------------------

1. Drop columns (remove from dataset)
    - df.drop(columns=['region', 'status'])
    - when to usez; column provides no value, confirmed with stakeholders
    - when not to use: column might be populated later, documentation value


2. Investigate why (understand root cause)
    - talk to data owners: why is this column empty?
    - is it a temporary state of permanent?
    - should it be populated?
    - when to use: first step, always!
    - when not to use: you are sure it's unused


3. Document and preserve (kep but note)
    - add to data dictionary: "region: unused, all NULL"
    - keep column for schema compatibility
    - when to use: need consistent schema across datasets
    - when not to use: storage/performance is critical

"""


# Part 8: Outliers

"""
What are Outliers?
----------------------
Values that are extremely different from most other values in the same column.
Not necessarily wrong, but unusual enough to investigate.


Why do they happen?
-------------------------
- Legitimate extreme cases (billionaire in income dataset)
- Data entry errors (extra zero: 1,000 - > 10,000)
- Measurement errors (sensor malfunction)
- Different populations mixed together
- Special/test records in production data


Why do they matter?
---------------------
- skew statistical measure (mean, standard deviation)
- affect machine learning model training
- might indicate data quality problems
- might indicate fraud or unusual events (important to catch!)
- can make visualizations hard to read

How to detect:
---------------
Use statistical methods to find values far from the 'normal' range

"""

print("-" * 80)
print("Detecting outliers")
print('-' * 80)

# Focus on purchase_amount column
# First, remove missing value for calculation
purchase_amounts = df['purchase_amount'].dropna()

# Calculate basic statistics
mean_amount = purchase_amounts.mean()
median_amount = purchase_amounts.median()
std_amount = purchase_amounts.std()     # standard deviation



print(f"\nPurchase Amount Statistics")
print(f"Mean (average): {mean_amount}")
print(f"Median (middle value) {median_amount}")
print(f"Standard Deviation: {std_amount}")



# Method 1: Z-Score Method
# Z score measures how many standard deviations away from mean
# Generally, /Z-Score/ > 3 is considered an outlier
print("\nZ-Score Method (|z| > 3 indicates outlier):")
for idx, amount in df['purchase_amount'].items():
    if pd.notna(amount):  # Skip NaN values
        z_score = (amount - mean_amount) / std_amount
        is_outlier = abs(z_score) > 3
        print(f"Row {idx}: ${amount:.2f}, z-score={z_score:.2f}, outlier={is_outlier}")






# Part 9: Suspicious or impossible values

"""
What are suspicious/impossible values?
---------------------------------------
values that violate business rules, physical reality, or logical constraints:
- Negative age
- Age > 150 years
- Future birth dates
- Negative prices (unless refund)
- Email without @ symbol



Why do they matter?
--------------------
- indicate serious data quality problems
- make analysis meaningless
- break business logic and applications
- suggest inadequate data validation
- undermine trust in entire dataset

How to detect:
--------------------
Apply domain knowledge and business rules to validate each field

"""


print("=" * 80)
print("Detecting suspicious or impossible values")
print("=" * 80)

# Check age column for impossible values
print("\nValidating 'age' column:")
print("Checking for negative ages...")
for idx, age in df['age'].items():
    if pd.notna(age) and age != '30':  # Skip NaN and string '30'
        if age < 0:
            print(f"  Row {idx}: age={age} is NEGATIVE (impossible!)")
        elif age > 120:  # Very old but theoretically possible
            print(f"  Row {idx}: age={age} is EXTREMELY HIGH (suspicious!)")
        elif age > 150:
            print(f"  Row {idx}: age={age} is IMPOSSIBLE (no human this old)")



# Part 10: Structural Issues

"""
What are structural issues?
-----------------------------
Problems with the overall shape, organization, or schema of the data:
- unexpected number of columns
- wrong column names
- columns in wrong order
- mixed data in single column
- headers missing or in wrong row

Why do they happen?
---------------------
- File format changes over time
- Different systems export different formats
- Manual Excel manipulation before export
- Concatenating files with different schemas
- Missing or extra columns in source

Why do they matter?
-----------------------
- Code expects specific columns, breaks if missing
- Automated pipelines fail
- can't join/merge with other datasets
- Column mapping becomes ambiguous
- hard to maintain code with changing structures


How to detect:
------------------
Compare actual structure against expected schema

"""


print("=" * 80)
print("Detecting structural issues")
print("=" * 80)



# Define what we EXPECT the data structure to look like
expected_columns = ['customer_id', 'customer_name', 'age', 'email',
                    'purchase_amoutn', 'country', 'signup_date']

# Notice: We expect 'country' and 'signup_date' but they are not in our data
# And we have 'region' and 'status' which aren't expected


actual_columns = df.columns.tolist()


print(f"\nExpected columns: {expected_columns}")
print(f"Actual columns {actual_columns}")


# Find missing columns (expected but not present)
missing_columns = set(expected_columns) - set(actual_columns)
print(f"\nMissing columns (expected but not found): {missing_columns}")

# Find unexpected columns (present but not expected)
unexpected_columns = set(actual_columns) - set(expected_columns)
print(f"\nUnexpected columns (found but not expected): {unexpected_columns}")

# Check column order
if expected_columns[:len(actual_columns)] != actual_columns:
    print("\nWARNING: Column order differs from expected!")
    print("This might cause issues if code relies on column positions.")



# Check total number of columns
print(f"\nExpected {len(expected_columns)} columns, found {len(actual_columns)} columns")

# Show the shape of the data (rows x columns)
print(f"\nDataFrame shape: {df.shape[0]} rows x {df.shape[1]} columns")



"""
COMMON SOLUTIONS FOR STRUCTURAL ISSUES:
----------------------------------------


1. Schema validation (Enforce structure)
    - define schema explicitly (column names, types, order)
    - validate before processing
    - fail fast if structure is wrong
    - when to use: production pipelines, automated processes
    - when not to use: exploratory analysis, adapting to changes


2. Flexible parsing (adapt to structure)
    - check what columns exist, adjust code accordingly
    - use column presence checks: if 'country' in df.columns
    - when to use: handling multiple data sources, versions
    - when not to use: need strict consistenct

3. Column mapping (rename/reorder)
    - df.rename(columns={'old_name': 'new_name'})
    - reorder columns to match expected order
    



"""