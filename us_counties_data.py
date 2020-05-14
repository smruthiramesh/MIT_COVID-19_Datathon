#!/usr/bin/env python
# coding: utf-8

import pandas as pd

#reading in relevant csv files
county_data = pd.read_csv("https://raw.githubusercontent.com/JieYingWu/COVID-19_US_County-level_Summaries/master/data/counties.csv")
infections_data = pd.read_csv("https://raw.githubusercontent.com/JieYingWu/COVID-19_US_County-level_Summaries/master/data/infections_timeseries.csv")

#list of states with state-wide lockdown (as seen on https://www.businessinsider.com/us-map-stay-at-home-orders-lockdowns-2020-3)
state_wide = ['CA','WA','OR','NV','NM','MN','WI','MI','KY','LA','VA','MD','VT','NH','NJ','MA','NY','CT','DE','DC','PR']
#dates of implementation
dates = ['031920','032320','032320','040120','032420','032520','032520','032420','032620','032020','032520','033020','032520','032720','032120','032320','032220','032320','032420','032720','033020']

#conversion to datetime format
dates = [pd.to_datetime(x,infer_datetime_format=True).date() for x in dates]

#dict mapping state to date of stay-at-home order
state_date = dict(list(zip(state_wide,dates)))


#relevant county-level socioeconomic and transit data columns
columns = ["State","Median_Household_Income_2018","transit_scores - population weighted averages aggregated from town/city level to county"]

#selecting counties from states with state-wide lockdown
infections_data = infections_data[infections_data['FIPS'].isin(county_level_data['FIPS'])].drop('Combined_Key',axis=1)

#collecting available dates for infection data
datecols_str = infections_data.drop(['FIPS','Combined_Key'],axis=1).columns
datecols = [pd.to_datetime(x,infer_datetime_format=True).date() for x in datecols]

#gets x dates before and after a given intervention
def get_dates(available_dates, intervention_date, number):
    before_dates = list(filter(lambda x:x<intervention_date, available_dates))
    after_dates = list(filter(lambda x:x>intervention_date, available_dates))
    return before_dates[-number:], after_dates[:number]

#converts a list of dates to a list of strings
def date_to_str(datelist):
    return [x.strftime("%-m/%-d/%y") for x in datelist]

#gets SES columns and infection observations if given state and number of dates required
def ses_and_infection(state, number, ses_columns):
    #getting x dates before and after stay at home order date
    before_dates_state, after_dates_state = get_dates(datecols, state_date[state], number)
    
    #converting dates to str type
    before_dates_str = date_to_str(before_dates_state)
    after_dates_str = date_to_str(after_dates_state)
    
    #getting infection data for those dates
    infections_state = infections_data[['FIPS']+before_dates_str+after_dates_str].set_index('FIPS')
    
    #getting ses data for the state
    ses_state = county_data[county_level_data['State']=='CA'].set_index('FIPS')[ses_columns]
    
    return ses_state.join(infections_state)

for state in state_wide:
    state_df = ses_and_infection(state,20,columns)
    state_df.to_csv("./"+str(state)+".csv")

