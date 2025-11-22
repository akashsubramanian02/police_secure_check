import streamlit as st
import pandas as pd
import mysql.connector
import datetime


# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='secure_check',
        )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None


# Fetch data from database
def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result)
        finally:
            connection.close()
    else:
        return pd.DataFrame()


# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="SecureCheck Police Dashboard", layout="wide")

st.title("🚨 SecureCheck: Police Check Post Digital Ledger")
st.markdown("Real-time monitoring and insights for law enforcement 🚓")

# -------------------- Navigation --------------------
page = st.radio(
    "Navigation",
    ["Dashboard", "Advanced Insights", "Complex Insights", "Existing Police Records"]
)

# Load data
query = "SELECT * FROM secure_check.policelog"
data = fetch_data(query)


# ==================== DASHBOARD PAGE ====================
if page == "Dashboard":

    st.header("📋 Police Logs Overview")
    st.dataframe(data, use_container_width=True)


# ==================== ADVANCED INSIGHTS PAGE ====================
elif page == "Advanced Insights":

    st.header("🧩 Advanced Insights")
    st.dataframe(data, use_container_width=True)

    selected_query = st.selectbox("Select a Query to Run", [
        "What are the top 10 vehicle_Number involved in drug-related stops",
        "Which vehicles were most frequently searched",
        "Which driver age group had the highest arrest rate",
        "What is the gender distribution of drivers stopped in each country",
        "Which race and gender combination has the highest search rate",
        "What time of day sees the most traffic stops",
        "What is the average stop duration for different violations",
        "Are stops during the night more likely to lead to arrests",
        "Which violations are most associated with searches or arrests",
        "Which violations are most common among younger drivers (<25)",
        "Is there a violation that rarely results in search or arrest",
        "Which countries report the highest rate of drug-related stops",
        "What is the arrest rate by country and violation",
        "Which country has the most stops with search conducted"
    ])

    query_map = {
        "What are the top 10 vehicle_Number involved in drug-related stops": """
            SELECT vehicle_number, COUNT(*) AS stop_count 
            FROM Secure_Check.policelog 
            WHERE drugs_related_stop = 1 
            GROUP BY vehicle_number 
            ORDER BY stop_count DESC LIMIT 10
        """,

        "Which vehicles were most frequently searched": """
            SELECT vehicle_number, COUNT(*) AS search_count 
            FROM secure_check.policelog 
            WHERE search_conducted = 1 
            GROUP BY vehicle_number 
            ORDER BY search_count DESC
        """,

        "Which driver age group had the highest arrest rate": """
            SELECT driver_age,
            COUNT(CASE WHEN stop_outcome = "Arrest" THEN 1 END) * 100.0 / COUNT(*) AS is_arrested
            FROM policelog
            GROUP BY driver_age
            ORDER BY is_arrested DESC
        """,

        "What is the gender distribution of drivers stopped in each country": """
            SELECT country_name, driver_gender, COUNT(*) AS stop_count 
            FROM policelog 
            GROUP BY country_name, driver_gender 
            ORDER BY country_name, stop_count DESC
        """,

        "Which race and gender combination has the highest search rate": """
            SELECT driver_race, driver_gender,
            COUNT(CASE WHEN search_conducted = 1 THEN 1 END) * 100.0 / COUNT(*) AS search_rate
            FROM policelog
            GROUP BY driver_race, driver_gender
            ORDER BY search_rate DESC
        """,

        "What time of day sees the most traffic stops": """
            SELECT DATE_FORMAT(stop_time, '%H') AS hour, COUNT(*) AS stop_count
            FROM policelog
            GROUP BY hour
            ORDER BY stop_count DESC
        """,

        "What is the average stop duration for different violations": """
            SELECT violation, AVG(stop_duration) AS avg_duration 
            FROM policelog 
            GROUP BY violation 
            ORDER BY avg_duration DESC
        """,

        "Are stops during the night more likely to lead to arrests": """
            SELECT CASE
                WHEN HOUR(stop_time) BETWEEN 20 AND 23 THEN 'Night'
                WHEN HOUR(stop_time) BETWEEN 0 AND 5 THEN 'Night'
                ELSE 'Day'
                END AS time_of_day,
                COUNT(CASE WHEN stop_outcome = 'Arrest' THEN 1 END) * 100.0 / COUNT(*) AS arrest_rate
            FROM policelog
            GROUP BY time_of_day
        """,

        "Which violations are most associated with searches or arrests": """
            SELECT violation,
            COUNT(CASE WHEN search_conducted = 1 THEN 1 END) AS search_count,
            COUNT(CASE WHEN is_arrested = 1 THEN 1 END) AS arrest_count
            FROM policelog
            GROUP BY violation
            ORDER BY (search_count + arrest_count) DESC
        """,

        "Which violations are most common among younger drivers (<25)": """
            SELECT violation, COUNT(*) AS stop_count 
            FROM policelog 
            WHERE driver_age < 25 
            GROUP BY violation 
            ORDER BY stop_count DESC
        """,

        "Is there a violation that rarely results in search or arrest": """
            SELECT violation, COUNT(*) AS total_stops,
            AVG(CASE WHEN search_conducted = 1 OR is_arrested = 1 THEN 1 ELSE 0 END) AS action_rate
            FROM policelog
            GROUP BY violation
            ORDER BY total_stops DESC
        """,

        "Which countries report the highest rate of drug-related stops": """
            SELECT country_name, COUNT(*) AS drug_related_stops
            FROM policelog
            WHERE drugs_related_stop = 1
            GROUP BY country_name
            ORDER BY drug_related_stops DESC
        """,

        "What is the arrest rate by country and violation": """
            SELECT country_name, violation_raw,
            COUNT(CASE WHEN is_arrested = 1 THEN 1 END) * 100.0 / COUNT(*) AS arrest_rate
            FROM policelog
            GROUP BY country_name, violation_raw
            ORDER BY arrest_rate DESC
        """,

        "Which country has the most stops with search conducted": """
            SELECT country_name, COUNT(*) AS search_stop_count
            FROM policelog
            WHERE search_conducted = 1
            GROUP BY country_name
            ORDER BY search_stop_count DESC
        """
    }

    if st.button("Run Query"):
        result = fetch_data(query_map[selected_query])
        if not result.empty:
            st.write(result)
        else:
            st.warning("No results found.")


# ==================== COMPLEX INSIGHTS PAGE ====================
elif page == "Complex Insights":

    st.header("🧩 Complex Insights")
    st.dataframe(data, use_container_width=True)

    selected_complex_query = st.selectbox("Select a Query to Run", [
        "Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)",
        "Driver Violation Trends Based on Age and Race (Join with Subquery)",
        "Time Period Analysis of Stops",
        "Violations with High Search and Arrest Rates",
        "Driver Demographics by Country",
        "Top 5 Violations with Highest Arrest Rates"
    ])

    complex_query_map = {
        "Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)": """
            SELECT country_name, year, total_stops, arrests,
            SUM(arrests) OVER (PARTITION BY country_name ORDER BY year) AS running_arrests
            FROM (
                SELECT country_name, YEAR(stop_time) AS year,
                COUNT(*) AS total_stops,
                COUNT(CASE WHEN is_arrested = 1 THEN 1 END) AS arrests
                FROM policelog
                GROUP BY country_name, year
            ) t
            ORDER BY country_name, year
        """,

        "Driver Violation Trends Based on Age and Race (Join with Subquery)": """
            SELECT p.driver_age, p.driver_race, p.violation,
            COUNT(*) AS stop_count
            FROM policelog p
            JOIN (
                SELECT driver_age, driver_race
                FROM policelog
                GROUP BY driver_age, driver_race
            ) t
            ON p.driver_age = t.driver_age
            AND p.driver_race = t.driver_race
            GROUP BY p.driver_age, p.driver_race, p.violation
            ORDER BY stop_count DESC
        """,

        "Time Period Analysis of Stops": """
            SELECT YEAR(STR_TO_DATE(p.stop_date, '%Y-%m-%d')) AS year,
            MONTH(STR_TO_DATE(p.stop_date, '%Y-%m-%d')) AS month,
            CAST(SUBSTRING_INDEX(p.stop_time, ':', 1) AS UNSIGNED) AS hour,
            COUNT(*) AS stop_count
            FROM policelog p
            WHERE p.stop_date IS NOT NULL AND p.stop_time IS NOT NULL
            GROUP BY year, month, hour
            ORDER BY year, month, hour
        """,

        "Violations with High Search and Arrest Rates": """
            SELECT violation, search_rate, arrest_rate,
            RANK() OVER (ORDER BY (search_rate + arrest_rate) DESC) AS rank_order
            FROM (
                SELECT violation,
                COUNT(CASE WHEN search_conducted = 1 THEN 1 END) * 100.0 / COUNT(*) AS search_rate,
                COUNT(CASE WHEN is_arrested = 1 THEN 1 END) * 100.0 / COUNT(*) AS arrest_rate
                FROM policelog
                GROUP BY violation
            ) t
            ORDER BY rank_order
        """,

        "Driver Demographics by Country": """
            SELECT country_name, driver_age, driver_gender,
            driver_race, COUNT(*) AS stop_count
            FROM policelog
            GROUP BY country_name, driver_age, driver_gender, driver_race
            ORDER BY country_name, stop_count DESC
        """,

        "Top 5 Violations with Highest Arrest Rates": """
            SELECT violation, COUNT(*) AS total,
            SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS arrests,
            SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS arrest_rate
            FROM policelog
            GROUP BY violation
            ORDER BY arrest_rate DESC LIMIT 5
        """
    }

    if st.button("Run Complex Query"):
        result = fetch_data(complex_query_map[selected_complex_query])
        st.write(result)


# ==================== PREDICTION FORM PAGE ====================
elif page == "Existing Police Records":

    st.title("🚔 Police Log Based on Existing Details")
    st.dataframe(data, use_container_width=True)

    st.write("Select values. System will find matching row and show result.")

    # ---- FORM START ----
    with st.form("match_form"):

        StopDate = st.selectbox("Stop Date", sorted(data['stop_date'].unique()))
        CountryName = st.selectbox("Country Name", sorted(data['country_name'].unique()))
        DriverGender = st.selectbox("Driver Gender", sorted(data['driver_gender'].unique()))
        DriverAge = st.selectbox("Driver Age", sorted(data['driver_age'].unique()))       
        SearchConducted = st.selectbox("Search Conducted", sorted(data['search_conducted'].unique()))      
        DrugsRelatedStop = st.selectbox("Drugs Related Stop", sorted(data['drugs_related_stop'].unique()))
        StopDuration = st.selectbox("Stop Duration", sorted(data['stop_duration'].unique()))
        VehicleNumber = st.selectbox("Vehicle Number", sorted(data['vehicle_number'].unique()))

        submitted = st.form_submit_button("Predict Outcome & Violation")

    # ---- FORM SUBMIT ----
    if submitted:

        #data['search_type'] = data['search_type'].fillna("None")

        filtered = data[
            (data['stop_date'] == StopDate) &
            (data['country_name'] == CountryName) &
            (data['driver_gender'] == DriverGender) &
            (data['driver_age'] == DriverAge) &           
            (data['search_conducted'] == SearchConducted) &
            (data['drugs_related_stop'] == DrugsRelatedStop) &
            (data['stop_duration'] == StopDuration) &
            (data['vehicle_number'] == VehicleNumber)
        ]

        if filtered.empty:
            st.error("❌ No matching row found. Check your inputs.")
        else:
            row = filtered.iloc[0]
            st.success("✔ Match Found!")

            st.markdown(f"""
            ### 🔮 Prediction Result
            **Outcome:** `{row['stop_outcome']}`  
            **Violation:** `{row['violation']}`  
            """)


            st.markdown(f"""
            🚔 **Prediction Summary**
                        
            🗒️ A {DriverAge}-year-old {DriverGender} driver in {CountryName} was stopped on {StopDate}.  
          
            Stop duration: **{StopDuration}**.  
            Vehicle Number: **{VehicleNumber}**.
            """)

            st.write(row)