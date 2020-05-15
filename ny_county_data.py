import pandas as pd

ny_data = pd.read_csv("/Users/smruthi/Downloads/New_York_State_Statewide_COVID-19_Testing.csv")
county_codes = pd.read_csv("/Users/smruthi/Downloads/NY_Municipalities_and_County_FIPS_codes.csv")
county_data = pd.read_csv("https://raw.githubusercontent.com/JieYingWu/COVID-19_US_County-level_Summaries/master/data/counties.csv")

#fixing name error
county_codes.replace("St Lawrence","St. Lawrence",inplace=True)

#joining infection data with county code data
ny_data_fips = ny_data.set_index("County").join(county_codes.set_index("County Name")).astype({'County FIPS': 'int32'})

#setting columns we will use for SES and infection related variables
relevant_ses_columns = ["Median_Household_Income_2018","transit_scores - population weighted averages aggregated from town/city level to county"]
relevant_infection_columns = ['Test Date','New Positives','Cumulative Number of Positives','Total Number of Tests Performed','Cumulative Number of Tests Performed',]

#data for testing is divided into municipalities for each county - we are aggregating it into county level data
grouped_county_inf = ny_data_fips.groupby(['County FIPS','Test Date'])[relevant_infection_columns].sum().reset_index()

#joining infection and SES data
ses_and_infection = county_data[county_data['State']=='NY'].set_index('FIPS').join(grouped_county_inf.set_index('County FIPS'))

#selecting relevant columns
ses_and_infection = ses_and_infection[relevant_ses_columns+relevant_infection_columns].drop(36000)

#saving data
ses_and_infection.to_csv("./ny_county_data/ny_county_data.csv")

