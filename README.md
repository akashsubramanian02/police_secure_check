# police_secure_check
Anonymized police check post log data with stop details, driver demographics, vehicle info, search/drug indicators, violations, outcomes, and durations. Ideal for law enforcement analytics, traffic stop trends, and predictive modeling.
This project shows how I processed a police stops dataset using Jupyter Notebook, Python, MySQL, and Streamlit. Below is a simple step‑by‑step description of the full workflow.

✅ Step-by-Step Process

Created .ipynb file (police_log.ipynb) Loaded the dataset

Displayed the data

Cleaned the dataset Removed/handled null values

Converted NaN values into Python None (for MySQL compatibility)

Created a new timestamp column Combined Stop Date and Stop Time into one column

Connected to MySQL from VS Code Used mysql-connector-python

Established connection using database name: secure_check, table: policelog

Inserted cleaned data into MySQL Wrote insert code in Python

Inserted row-by-row

Created .py helper file (police_log.py) Added functions for:

Database connection

Insert operations

Running SQL queries with fetchall()

Connected .ipynb and .py Imported functions from police_log.py

Executed queries from the notebook using helper functions

Wrote and executed SQL queries Both basic and advanced queries

Used fetchall() to collect and display results

Built Streamlit Application Created UI with select box for predefined queries

Added custom query text area for advanced SQL

Displayed results in an interactive table

Final Output Fully working Streamlit dashboard

Supports both simple and complex SQL queries

Connected end‑to‑end: Dataset → Cleaning → MySQL → Python → Streamlit
