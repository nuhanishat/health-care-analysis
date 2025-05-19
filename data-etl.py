import pandas as pd
import sqlite3
from handler_funcs import convert_numberobj_to_float

## Load file into pandas dataframe to clean and transform data

# Read data into pandas dataframe
df = pd.read_csv('sampled_medicare_data.csv', low_memory=False)




# Rename colums to readable and SQL-friendly headings
df.rename(columns = { 'Rndrng_NPI': 'national_provider_identifier', 
                    'Rndrng_Prvdr_Last_Org_Name' : 'provider_last_org_name', 
                    'Rndrng_Prvdr_First_Name' : 'provider_first_name',
                    'Rndrng_Prvdr_MI' : 'provider_middle_name_initial',
                    'Rndrng_Prvdr_Crdntls' : 'provider_credentials',
                    'Rndrng_Prvdr_Ent_Cd' : 'provider_entity_type',
                    'Rndrng_Prvdr_St1' : 'provider_street_address_1',
                    'Rndrng_Prvdr_St2' : 'provider_street_address_2',
                    'Rndrng_Prvdr_City' : 'provider_city',
                    'Rndrng_Prvdr_State_Abrvtn' : 'provider_state_abbreviation',
                    'Rndrng_Prvdr_State_FIPS' : 'provider_fips_code',
                    'Rndrng_Prvdr_Zip5' : 'provider_zip_code',
                    'Rndrng_Prvdr_RUCA' : 'provider_ruca_code',
                    'Rndrng_Prvdr_RUCA_Desc' : 'provider_ruca_description',
                    'Rndrng_Prvdr_Cntry' : 'provider_country',
                    'Rndrng_Prvdr_Type' : 'provider_type',
                    'Rndrng_Prvdr_Mdcr_Prtcptg_Ind' : 'provider_medicare_participation_indicator',
                    'HCPCS_Cd' : 'hcpcs_code',
                    'HCPCS_Desc' : 'hcpcs_description',
                    'HCPCS_Drug_Ind' : 'hcpcs_drug_indicator',
                    'Place_Of_Srvc' : 'place_of_service',
                    'Tot_Benes' : 'number_of_beneficiaries',
                    'Tot_Srvcs' : 'number_of_services',
                    'Tot_Bene_Day_Srvcs' : 'number_of_unique_beneficiary_services',
                    'Avg_Sbmtd_Chrg' : 'average_submitted_charge_amount',
                    'Avg_Mdcr_Alowd_Amt' : 'average_medicare_allowed_amount',
                    'Avg_Mdcr_Pymt_Amt' : 'average_medicare_payment_amount',
                    'Avg_Mdcr_Stdzd_Amt' : 'average_medicare_standard_pay'}, inplace=True)


# print(df.info())
# print(df.shape)
# print(df.columns)

# Remove duplicate rows for national_provider_identifier
df.drop_duplicates(subset=['national_provider_identifier'], keep='first', inplace=True)
print('Duplicates removed!')


# Change the number amounts to numeric float type 

df = convert_numberobj_to_float(df, 'average_submitted_charge_amount')
df = convert_numberobj_to_float(df, 'number_of_beneficiaries')
df = convert_numberobj_to_float(df, 'number_of_services')
df = convert_numberobj_to_float(df, 'number_of_unique_beneficiary_services')
df = convert_numberobj_to_float(df, 'average_medicare_allowed_amount')
df = convert_numberobj_to_float(df, 'average_medicare_payment_amount')
df = convert_numberobj_to_float(df, 'average_medicare_standard_pay')

# print(df.info())

#***********************************************************************************

## Create and load data in a SQL database

# Create database filename
database_file = 'medicare_database.db'

# Create the file and connect to sqlite 
sql_connect = sqlite3.connect(database_file)

# Cursor object to execute sql commands
cursor = sql_connect.cursor()

print("[SQL] Connected to the database successfully!")

# Create the sql table
create_table_sql = """
CREATE TABLE medicare_database (
    national_provider_identifier INTEGER PRIMARY KEY, 
    provider_last_org_name TEXT, 
    provider_first_name TEXT,
    provider_middle_name_initial TEXT,
    provider_credentials TEXT,
    provider_entity_type TEXT,
    provider_street_address_1 TEXT,
    provider_street_address_2 TEXT,
    provider_city TEXT,
    provider_state_abbreviation TEXT,
    provider_fips_code TEXT,
    provider_zip_code TEXT,
    provider_ruca_code REAL,
    provider_ruca_description TEXT,
    provider_country TEXT,
    provider_type TEXT,
    provider_medicare_participation_indicator TEXT,
    hcpcs_code TEXT,
    hcpcs_description TEXT,
    hcpcs_drug_indicator TEXT,
    place_of_service TEXT,
    number_of_beneficiaries INTEGER,
    number_of_services REAL,
    number_of_unique_beneficiary_services INTEGER,
    average_submitted_charge_amount REAL,
    average_medicare_allowed_amount REAL,
    average_medicare_payment_amount REAL,
    average_medicare_standard_pay REAL
);
"""

# Execute CREATE TABLE in database
cursor.execute(create_table_sql)
sql_connect.commit()

print("[SQL] Table created successfully!")

print(len(df))

df.to_sql('medicare_database', sql_connect, if_exists='append', index=False, chunksize=len(df))

print("[SQL] Data loaded successfully!")

#Close the connection to the database
sql_connect.close()