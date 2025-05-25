# Healthcare claims Data Analysis

## Project Overview 
This project aimed to analyze publicly available Medicare claims data to identify key drivers of healthcare utilization and costs. The goal was to explore patterns and trends that could inform decision-making for healthcare providers, payers, and policymakers. The analysis focused on identifying high-cost procedures, examining geographic variations in healthcare spending, and gaining more insight into limited data by classifying the services provided during established patient visits.

## Data Source
The project utilized the Centers for Medicare & Medicaid Services (CMS) Medicare Provider Utilization and Payment Data (Physician and Other Supplier PUF). [Found here](https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider-and-service)

The raw dataset contained over 9.6 million data points.

## Methology

### 1. Data Sampling (Reservoir Sampling)
Due to the size of the dataset (9,660,647 data points), reservoir sampling was employed to reduce the dataset to a manageable size of 50,000 data points while preserving the overall distribution of the data. Reservoir sampling is an algorithm that sequentially processes each record, maintaining a representative sample without requiring the entire dataset to be loaded into memory. Please look at the file ```reservoir_sampling.py``` for detailed implementation. The original dataset file was too big to upload here so you will only the sampled dataset in this repo, see file```sampled_medicare_data.csv```. 

If you want to use my reservoir sampling code, please set the variable ```file_name``` to your raw data csv file name in ```reservoir_sampling.py```.

### 2. Data Extraction and ETL
The sampled CMS data was loaded into SQLite database using Python and Pandas. Data cleaning and transformation stpes were performed to handle missing values, standardize data types and create new calculated fields. 

### 3. SQL Analysis: 
SQL queries were used to analyze the data and generate insights, such as identifying the most expensive procedures, calculating average costs, and summing the total number of services.

### 4. Data Visualization: 
Matplotlib and Seaborn were used to create visualizations to effectively communicate the findings.

## Data Exploration Process:

The data exploration followed these key steps:

### 1. Identified Most Expensive Procedures: 
The initial analysis focused on identifying the procedures with the highest average Medicare allowed amount.
![image](https://github.com/user-attachments/assets/c914f048-c84f-4cf4-acb8-84f39dbc8339)


### 2. Analyzed Procedures with Highest Total Spending: 
Shifted focus to identify those procedures with the highest total spending (average cost * volume), revealing that high spending was more related to high-volume, lower-cost procedures.
![image](https://github.com/user-attachments/assets/0434f374-58f4-4769-9328-e9e784e85e5e)

### 3. Explored Geographic Variation: 
Investigated potential geographic patterns for a mix of commonly performed and higher spending procedures. Two top proecedures were **establised patient visits** and **age-related eye treatments**
For age-related macular degenertation, there were no clear trend in the geographic variation. For established patient visits, this was done after classifying the data (discussed in the next step).
![image](https://github.com/user-attachments/assets/e7962ebe-d9a8-44c3-8559-9cf2cc054982)

### 4. Classified Established Patient Visits: 
Established patient visit data was very limited - no other information was provided except for the type of provider. So the data was classified by provider specialties with the highest volume. 
![image](https://github.com/user-attachments/assets/cab6384f-7745-4508-80c9-0d1dfb252554)

Lastly, looked at this data by states to see if there is a overall pattern, and found that across all specialties, four major states - CA, NY, FL and TX consistently had the highest volume of services. 
![image](https://github.com/user-attachments/assets/07895880-6ae5-49db-a782-ea37e7c8fefc)


## Key Findings:

### 1. Established Patient Visits Dominate Healthcare Expenditures: 
"Established patient office or other outpatient visits" were found to be the most frequent type of encounter, highlighting the importance of primary care and preventive care.

### 2. Geographic Patterns Influence Volume:: 
The four states California, Florida, New York and Texas consistently had higher service volumes across all top provider specialties. This most likely tied to the fact that these states are the top four states with the highest population in the US ([source](https://worldpopulationreview.com/states)). Also 25% of all elderly population reside in California, Florida, and Texas leading to frequent utilization of healthcare by this population ([source](https://www.prb.org/resources/which-us-states-are-the-oldest/#:~:text=More%20than%2055%20million%20Americans,California%2C%20Florida%2C%20and%20Texas.)). 

## Recommendations:

### 1. Implement Enhanced Data Collection for Patient and Provider Characteristics:
The dataset is incomplete to accurately understand what is driving the high volume and consequently high cost for established patient visits since this is the type of service with the highest spending utilization. It is important to expand the current dataset to include additional data points on both patient, providers and the procedure performed, in compliance with all privacy and legal obligations. This can show further insights to see if the current findings are valid and more actions that can be taken to understand these high costs and find ways to reduce it. 

### 2. Targeted Audit of E/M Coding Practisces in High-Volume States:



