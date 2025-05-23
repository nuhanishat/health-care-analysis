import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Connect to sql database
sql_filename = 'medicare_database.db'
sql_connect = sqlite3.connect(sql_filename)
cursor = sql_connect.cursor()

print('[SQL] Connected to the database successfully!')

def top_procedures_by_provider(sql_connect, limit):
    """
    Generates a bar chart showing the top procedures for established patients, grouped by provider specialty
    
    args: 
        sql_connect: The SQLite connection object

    """

    query = f"""
    SELECT
        provider_type,
        hcpcs_description,
        SUM(number_of_services) AS total_services,
        AVG(average_medicare_allowed_amount) AS average_cost
    FROM
        medicare_database
    WHERE
        hcpcs_description LIKE '%Established patient office or other outpatient visit%'
    GROUP BY
        provider_type, hcpcs_description
    ORDER BY
        total_services DESC
    LIMIT {limit};
    """

    # Read results in df
    df = pd.read_sql_query(query, sql_connect)

    # Plot code
    # Plot code here
    plt.figure(figsize=(14, 8))
    plt.bar(df['provider_type'], df['total_services'], color='skyblue')
    plt.xlabel("Medical Providers", size=14)
    plt.ylabel("Number of Medical Procedures", size=14)
    plt.title('Medical Provider vs Procedures', size=16)
    plt.grid(True)
    plt.show()


def analyze_cost_by_speciality_and_state(sql_connect, specialty, limit_show = 10):
    """ Analyzes and visualizes the total spends by a specialty

    Args:
        sql_connect: the SQLite connection object
        specialty : medical speciality or provider type name
    Raises:
        Exceptions from trying to connect to non valid entries.
    """
    query = f"""
    SELECT
        provider_type,
        provider_state_abbreviation AS state,
        AVG(average_medicare_allowed_amount) AS average_cost,
        SUM(number_of_services) AS total_services,
        (AVG(average_medicare_allowed_amount) * SUM(number_of_services)) AS total_spending
        FROM
            medicare_database
        WHERE provider_type = "{specialty}"
        GROUP BY state
        ORDER BY
            total_spending DESC;
        """
    
    df = pd.read_sql_query(query, sql_connect)
    shorten = df[:limit_show]

    sns.barplot(x=shorten["provider_type"], y=shorten["total_spending"], hue=shorten["state"])
    plt.show()


# top_procedures_by_provider(sql_connect, 10)

top_providers = { "Internal Medicine" : 10,
                    "Family Practice": 5, 
                    "Nurse Practitioner": 5,
                    "Cardiology" : 5,
                    "Physicians Assistant": 5,
                    "Dermatology": 5 }

specialty = ["Internal Medicine", "Family Practice", "Nurse Practitioner", "Cardiology", "Physicians Assistant", "Dermatology"]
                    
# Run the function here
# for name in top_providers:
#     try: 
#         analyze_cost_by_speciality_and_state(sql_connect, name, limit_show=top_providers[name])
#     except sqlite3.OperationalError:
#         print(f"OperationalError! Please check the {name} call")


def generate_pie_charts_by_provider(sql_connect, provider_list):
    """
    Generates pie charts showing the geographic distribution of
    "Established patient office or other outpatient visit" claims
    for each provider specialty in provider_list.

    Args:
        db (str): Path to the SQLite database file.
        provider_list (list): A list of provider specialty names to analyze.
    """
    #Iterate for each provider, show them the world
    for provider in provider_list:
        try:
            # SQL Query
            query = f"""
                SELECT
                    provider_state_abbreviation AS state,
                    SUM(number_of_services) AS total_services
                FROM
                    medicare_database
                WHERE
                    hcpcs_description LIKE '%Established patient office or other outpatient visit%'
                    AND provider_type = "{provider}"
                GROUP BY
                    state
                ORDER BY
                    total_services DESC;
                """
            #Load it to panda and see
            df = pd.read_sql_query(query, sql_connect)

            #If no SQL connection, crash
        except sqlite3.OperationalError as msg:
            #If bad entry tell what object it is then skip.
            print("This type of call does not exist, will skip to generate other calls : " + str(msg))
            continue

        try: #Check that the chart can exist

            total = df['total_services'].sum()
            
            if total > 0 :
                percentage = 0.029

                #Filter out points that satisfy the "Less Than 2.9%" value
                small_df = df[df['total_services'] < percentage*total]
                main_df = df[df['total_services'] >= percentage*total]

                #Determine
                small_total = small_df["total_services"].sum()
                other_state = pd.DataFrame([{"state": "Other (combined states < 2.9%)", "total_services": small_total}])
                df = pd.concat([main_df, other_state], ignore_index = True)

                # Create a pie chart
                plt.figure(figsize=(8, 8))
                plt.pie(df['total_services'], labels=df['state'], autopct='%1.1f%%', startangle=140) #Fill in the code
                plt.title(f"Geographic Distribution of {provider} (Established Pt Visits)")
                plt.tight_layout()
                plt.show() #Show the graph

            else:
                print("No data to present!")

            #Close it and end to generate another object
        except KeyError as msg:#If chart does not exist, skip.
            print("There is not a way to draw a "+name+" chart, will skip")

generate_pie_charts_by_provider(sql_connect, specialty)


sql_connect.close()