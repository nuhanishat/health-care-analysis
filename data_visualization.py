import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# Connect to sql database
sql_filename = 'medicare_database.db'
sql_connect = sqlite3.connect(sql_filename)
cursor = sql_connect.cursor()

print('[SQL] Connected to the database successfully!')

## Data Exploration

# Number of rows (we know this from creating table so double-checking -> 47524 rows)
query = "SELECT COUNT(*) FROM medicare_database;"
cursor.execute(query)
num_rows = cursor.fetchone()[0]
print(f"Number of rows: {num_rows}")

# Number of columns (we know this from creating table so double-checking)
query = "PRAGMA table_info(medicare_database);"
cursor.execute(query)
columns = cursor.fetchall()
# print("Columns: ")
# for column in columns:
#     print(column)

# Get the first 5 rows to see data 
query = "SELECT * FROM medicare_database LIMIT 5;"
df = pd.read_sql_query(query, sql_connect)
# print(df)

## Function to find the top 10 most expensive procedure
def top_procedures_by_medicare_cost(sql_connect, limit=10):
    """
    Retrieves and visializes the top N most expensive procedures based on average medicare allowed amount.

    args: 
        sql_connect: SQLite connection object
        limit: number of top procedures to display
    """
    query = f"""
    SELECT hcpcs_description, AVG(average_medicare_allowed_amount) AS average_cost
    FROM medicare_database
    GROUP BY hcpcs_description
    ORDER BY average_cost DESC
    LIMIT {limit}
    """
    df = pd.read_sql_query(query, sql_connect)

    plt.figure(figsize=(12, 6))
    sns.barplot(x='average_cost', y='hcpcs_description', data=df)
    plt.xlabel('Average Medicare Allowed Amount')
    plt.ylabel('Procedure')
    plt.title(f'Top {limit} Most Expensive Procedures')
    # plt.tight_layout()
    plt.show()

# top_procedures_by_medicare_cost(sql_connect)

## Function to find which procedures are the most common and most expensive
def top_procedures_by_total_cost(sql_connect, limit):
    """
    Retrieves and visializes the top N most expensive procedures based on total expense.

    args: 
        sql_connect: SQLite connection object
        limit: number of top procedures to display
    """
    query = f"""
    SELECT 
    hcpcs_description, 
    AVG(average_medicare_allowed_amount) AS average_cost,
    SUM(number_of_services) AS total_services,
    (AVG(average_medicare_allowed_amount) * SUM(number_of_services)) AS total_spending
    FROM medicare_database
    GROUP BY hcpcs_description
    ORDER BY total_spending DESC
    LIMIT {limit}
    """
    df = pd.read_sql_query(query, sql_connect)

    # Assign colors to unique hcpcs_description categories
    unique_desc = df['hcpcs_description'].unique()
    color_map = plt.cm.get_cmap('tab20', len(unique_desc))
    colors = [color_map(i) for i in range(len(unique_desc))]
    color_dict = dict(zip(unique_desc, colors))

    # Plot
    plt.figure(figsize=(12, 8))

    #Plot bubbles 
    for desc in unique_desc:
        subset = df[df['hcpcs_description'] == desc]
        total_spending = subset['total_spending'].iloc[0]
    
        # Format the legend
        label = f"{desc} (${total_spending:,.0f})"
        plt.scatter(x=subset['average_cost'], y=subset['total_services'],
                    s=subset['total_spending']/10000,
                    alpha=0.5,
                    color=color_dict[desc],
                    label=label)
        
    plt.xlabel('Average Medicare Allowed Amount')
    plt.ylabel('Total Number of Services')
    plt.title('Procedure Cost vs. Volume (Bubble Size = Total Spending)')
    plt.grid(True)

    # Add a legend
    plt.legend(scatterpoints=1, frameon=False, labelspacing=1, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout(rect=[0, 0, 0.85, 1])

    plt.show()



# top_procedures_by_total_cost(sql_connect, 20)

def top_procedures_by_total_cost_bubble(sql_connect, limit):
    """
    Retrieves and visializes the top N most expensive procedures based on total expense.

    args: 
        sql_connect: SQLite connection object
        limit: number of top procedures to display
    """
    query = f"""
    SELECT 
    hcpcs_description, 
    AVG(average_medicare_allowed_amount) AS average_cost,
    SUM(number_of_services) AS total_services,
    (AVG(average_medicare_allowed_amount) * SUM(number_of_services)) AS total_spending
    FROM medicare_database
    GROUP BY hcpcs_description
    ORDER BY total_spending DESC
    LIMIT {limit}
    """
    df = pd.read_sql_query(query, sql_connect)

   # Calculate the rank based on total_spending
    df['rank'] = df['total_spending'].rank(ascending=False, method='dense').astype(int)

    # Determine the size of the 'base' bubble (to scale other bubbles with the same value)
    max_spending = df['total_spending'].max()

    # Generate the figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Assign colors to unique hcpcs_description categories
    unique_descriptions = df['hcpcs_description'].unique()
    color_map = plt.cm.get_cmap('tab20', len(unique_descriptions))
    colors = [color_map(i) for i in range(len(unique_descriptions))]
    color_dict = dict(zip(unique_descriptions, colors))

    # Plot each procedure bubble, using the ranks instead of the names, with appropriate label
    # Store each the values to add in the custom chart, including labels, plots etc

    for index, row in df.iterrows():
        # Get circle color for labels
        label_value = row["hcpcs_description"]

        #Plot each entry
        scatter = ax.scatter(x=row['average_cost'],
                        y=row['total_services'],
                        s=row['total_spending']/10000, # Bubble scale
                        alpha=0.5,
                        color = color_dict[label_value],
                        label=str(row['rank'])) #Only label the ranks

        # Add the rank number inside the bubble
        ax.text(x=row['average_cost'], y=row['total_services'], s=str(row['rank']),
                ha='center', va='center', fontsize=9, color='black') #Show each entry

    # Add Labels and title
    plt.xlabel('Average Medicare Allowed Amount($)')
    plt.ylabel('Total Number of Services')
    plt.title('Procedure Cost vs. Volume (Bubble Size = Total Spending)')
    plt.grid(True)

    # Custom legend
    legend_elements = []
    # For each of those label values, create a bubble using the corresponding
    for label_value, color in color_dict.items():
        #Find the corresponding row entry, assuming at least one hit
        corresponding_entry = df[df["hcpcs_description"] == label_value].iloc[0]

        #Determine label's

        area = 100

        # plot circle
        circle = mpatches.Circle((0,0), radius=area**0.5, color=color, alpha=0.5, transform=ax.transData) #The colormap should be based on the original scatter

        #Add the label
        legend_elements.append((circle, f"{corresponding_entry['rank']}. {label_value} (${corresponding_entry['total_spending']:,.0f})"))

    #Plot it
    ax.legend(handles=[i[0] for i in legend_elements], #Transpose all of our legend elements to graph on a legend
            labels=[i[1] for i in legend_elements],
            loc='upper left',
            bbox_to_anchor=(1.05, 1),
            ncol=1, #Column label
            fontsize='medium',
            title="Procedure Ranks and Total Spending", #Label Title
            borderpad=1,  #Padding size in pixel
            handlelength=3, #Line up the right hand side
            labelspacing=1.5 #Spread out the spacing
            )

    # Tweak layout
    fig.tight_layout(rect=[0, 0, 0.75, 1]) #Make space for graph again

    # Show and close
    plt.show()


# top_procedures_by_total_cost_bubble(sql_connect, 10)

## Plot Procedure by state


