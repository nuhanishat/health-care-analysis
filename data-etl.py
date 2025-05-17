import pandas as pd
from handler_funcs import convert_numberobj_to_float

# Load file into dataframe
df = pd.read_csv('sampled_medical_data.csv', low_memory=False)

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


print(df.info())
print(df.shape)
print(df.columns)

# Change the number amounts to numeric float type 

df = convert_numberobj_to_float(df, 'average_submitted_charge_amount')
df = convert_numberobj_to_float(df, 'number_of_beneficiaries')
df = convert_numberobj_to_float(df, 'number_of_services')
df = convert_numberobj_to_float(df, 'number_of_unique_beneficiary_services')
df = convert_numberobj_to_float(df, 'average_medicare_allowed_amount')
df = convert_numberobj_to_float(df, 'average_medicare_payment_amount')
df = convert_numberobj_to_float(df, 'average_medicare_standard_pay')

print(df.info())
