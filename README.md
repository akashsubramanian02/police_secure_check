# police_secure_check
Anonymized police check post log data with stop details, driver demographics, vehicle info, search/drug indicators, violations, outcomes, and durations. Ideal for law enforcement analytics, traffic stop trends, and predictive modeling.


Police Log Project — Simple README

This project shows how I processed a police stops dataset using Jupyter Notebook, Python, MySQL, and Streamlit. Below is a simple step‑by‑step description of the full workflow.

✅ Step-by-Step Process
1. Created .ipynb file (police_log.ipynb)

Loaded the dataset

Displayed the data

2. Cleaned the dataset

Removed/handled null values

Converted NaN values into Python None (for MySQL compatibility)

3. Created a new timestamp column

Combined Stop Date and Stop Time into one column

4. Connected to MySQL from VS Code

Used mysql-connector-python

Established connection using database name: secure_check, table: policelog

5. Inserted cleaned data into MySQL

Wrote insert code in Python

Inserted row-by-row 

6. Created .py helper file (police_log.py)

Added functions for:

Database connection

Insert operations

Running SQL queries with fetchall()

7. Connected .ipynb and .py

Imported functions from police_log.py

Executed queries from the notebook using helper functions

8. Wrote and executed SQL queries

Both basic and advanced queries

Used fetchall() to collect and display results

9. Built Streamlit Application

Created UI with select box for predefined queries

Added custom query text area for advanced SQL

Displayed results in an interactive table

10. Final Output

Fully working Streamlit dashboard

Supports both simple and complex SQL queries

Connected end‑to‑end: Dataset → Cleaning → MySQL → Python → Streamlit
