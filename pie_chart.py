import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# Connect to sql database
sql_filename = 'medicare_database.db'
sql_connect = sqlite3.connect(sql_filename)
cursor = sql_connect.cursor()

print('[SQL] Connected to the database successfully!')

def generate_pie_chart_for_proc_by_state(sql_connect):

    #procedure to analyze
    procedures = {
        "Cataract Extraction": "Removal of cataract with insertion of prosthetic lens",
        "AMD Injection 1": "Injection, aflibercept",
        "AMD Injection 2": "Injection, faricimab-svoa"
    }

    # Loop and create a graph for every procedure entry
    for name, procedure in procedures.items():

        query = f""" 
        SELECT
            provider_state_abbreviation AS state, 
            SUM(number_of_services) AS total_services
        FROM
            medicare_database
        WHERE
            hcpcs_description LIKE "%{procedure}%"
        GROUP BY
            state
        ORDER BY
            total_services DESC;
        """

        # Execute the query and load the results into a df
        df = pd.read_sql_query(query, sql_connect)

        # Remove rows with NaN values in 'total_services'
        df = df.dropna(subset=['total_services'])

        #Data Filter
        total = df['total_services'].sum()
        percentage = 0.029

        small_df = df[df['total_services'] < percentage*total] #Small points
        main_df = df[df['total_services'] >= percentage*total] #Main points

        #Add new "Other state" entry
        small_total = small_df["total_services"].sum()
        other_state = pd.DataFrame([{"state": "Other", "total_services": small_total}])
        df = pd.concat([main_df, other_state], ignore_index = True)

        # Data is None
        if (len(df) == 0):
            print(f"There are not entries for procedure {name}")
            continue

        # Create a pie chart
        plt.figure(figsize=(8, 8))

        plt.pie(df['total_services'], labels=df['state'], autopct='%1.1f%%', startangle=140)
        plt.title(f'Geographic Distribution of {name}')
        plt.show()



generate_pie_chart_for_proc_by_state(sql_connect)

sql_connect.close()