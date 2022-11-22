import requests
# from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import numpy as np
import base64
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from pandas.io.json import json_normalize
from datetime import date, time
import json
import tkinter as tk

from urllib3.util import url

from statedata import us_state_to_abbrev
from statedata import us_state_list
from statedata import us_state_fip
from countydata import us_state_county

_ENABLE_PROFILING = False

if _ENABLE_PROFILING:
    import cProfile, pstats, io
    from pstats import SortKey

    pr = cProfile.Profile()
    pr.enable()

today = date.today()



##URL for webscraping National U.S COVID Data
#response = Request(url)
#response = requests.get('https://www.nytimes.com/interactive/2021/us/covid-cases.html')
#webpage = urlopen(response).read()
#html = soup(webpage, "html.parser")
#webscrapenum = soup.findall('li', class_='#maincounter-number')
#headers = {
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}


print('COVID-19 Utility Application')
print("""
* **Data source (COVID Data API):** [COVID-Act-Now.com](https://apidocs.covidactnow.org/), [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19), [New York Times](https://github.com/nytimes/covid-19-data)""")
print("""
This application uses COVID Data API to gather accurate data and present it in one place.

**This is an early version of the program, please do not take COVID data presented here as an accurate reflection.**
***
""")

# Johns Hopkins University COVID Data
def get_data():
    US_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    US_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
    confirmed = pd.read_csv(US_confirmed)
    usdeaths = pd.read_csv(US_deaths)
    return confirmed, usdeaths
confirmed, usdeaths = get_data()

# New York Times COVID Data API
def get_data():
    # U.S Death Data
    USA_deaths = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    usadeaths = pd.read_csv(USA_deaths)
    # U.S COVID Case Data
    USA_cases = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    usacases = pd.read_csv(USA_cases)
    # U.S State COVID Death Data
    State_deaths = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    statedeaths = pd.read_csv(State_deaths)
    # U.S State COVID Case Data
    State_cases = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    statecases = pd.read_csv(State_cases)
    # U.S County COVID Death Data
    County_deaths = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    countydeaths = pd.read_csv(County_deaths)
    # U.S County COVID Case Data
    County_cases = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    countycases = pd.read_csv(County_cases)

    return usadeaths, usacases, statedeaths, statecases, countydeaths, countycases
usadeaths, usacases, statedeaths, statecases, countydeaths, countycases = get_data()


FIPSs = confirmed.groupby(['Province_State', 'Admin2']).FIPS.unique().apply(pd.Series).reset_index()
FIPSs.columns = ['State', 'County', 'FIPS']
FIPSs['FIPS'].fillna(0, inplace = True)
FIPSs['FIPS'] = FIPSs.FIPS.astype(int).astype(str).str.zfill(5)

##State COVID Data **needs fixing**
state_url = "https://api.covidactnow.org/v2/states.json?apiKey=c4edd54144b943c68a637a1b64194c0c"
response = requests.get(state_url)
data = response.json()
#State-level stats
states = [x["state"] for x in data]
cases = [x["actuals"]["cases"] for x in data]
deaths = [x["actuals"]["deaths"] for x in data]


##County-level COVID Data **needs fixing**
county_url = "https://api.covidactnow.org/v2/counties.json?apiKey=c4edd54144b943c68a637a1b64194c0c"
response = requests.get(county_url)
data = response.json()
#County-level stats
counties = [x["county"] for x in data]
cases = [x["actuals"]["cases"] for x in data]
deaths = [x["actuals"]["deaths"] for x in data]


print(cases)
print(deaths)


STATEfips = us_state_fip(dict("fips"))
fips = STATEfips


dictionary_1 = dict(zip(states, cases))
dictionary_2 = dict(zip(counties, cases))
dictionary_3 = dict(zip(states, deaths))
dictionary_4 = dict(zip(counties, deaths))

dictionary_5 = dict(zip(states, confirmed))
dictionary_6 = dict(zip(counties, confirmed))
dictionary_7 = dict(zip(states, usdeaths))
dictionary_8 = dict(zip(counties, usdeaths))

# New York Times COVID Data API Dict 9 - 13
#dictionary_9 = dict(zip(countries, usadeaths))
dictionary_9 = dict(STATEfips(fips, statedeaths))
dictionary_10 = dict(zip(states, statedeaths))
dictionary_11 = dict(zip(counties, countydeaths))
dictionary_12 = dict(zip(states, statecases))
dictionary_13 = dict(zip(counties, countycases))




## U.S State Input
inp = False
state_key = ""

while (inp == False):
    try:
        state = input("Please enter a state: ")
        state = state.lower()
        state = state.title()
        state_key = us_state_to_abbrev[state]
        state_key = us_state_list[state]
        state_key = us_state_fip[state]
        state_key = FIPSs
        state_key = us_state_list
        print(state_key)
        inp = True
    except:
        print("Try again")

## US State County Input
inp = False
county_key = ""

while (inp == False):
    try:
        county = input("Please enter a county: ")
        county = county.lower()
        county = county.title()
        county_key = us_state_county[county]["name"]
        print(county_key)
        inp = True
    except:
        print("Try again")

# mainline console print
print("There are " + str(dictionary_1[state_key]) + " total confirmed COVID-19 cases in " + state)
print("There are " + str(dictionary_2[county_key]) + " total confirmed COVID-19 cases in " + county)
print("There are " + str(dictionary_3[state_key]) + " total deaths in " + state)
print("There are " + str(dictionary_4[county_key]) + " total deaths in " + county)

print("There are " + str(dictionary_5[state_key]) + " total confirmed COVID-19 cases in " + state + " according to [Johns Hopkins University]")
print("There are " + str(dictionary_6[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to [Johns Hopkins University]")
print("There are " + str(dictionary_7[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to [Johns Hopkins University]")
print("There are " + str(dictionary_8[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to [Johns Hopkins University]")

#temporary line
print("There are " + str(dictionary_9[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to [NYT]")

print("There are " + str(dictionary_10[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to [New York Times]")
print("There are " + str(dictionary_11[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to [New York Times]")
print("There are " + str(dictionary_12[state_key]) + " total confirmed COVID-19 cases in " + state + " according to [New York Times]")
print("There are " + str(dictionary_13[county_key]) + " total confirmed COVID-19 cases in " + county + " according to [New York Times]")





print('# COVID-19 Utility Data Dashboard')

print("""
    **Built by Arian Kharazmi**
    """)

print(f"""
    The COVID-19 Utility Application was developed to track and monitor data regarding the Coronavirus Pandemic to better understand the data surrounding it, in an easy-to-use, friendly manner.

    COVID Data traced from:
    [COVID-19 Data Repository](https://github.com/CSSEGISandData/COVID-19)[*Johns Hopkins University*]
    https://covidactnow.org/[*COVIDActNow Org*]  

    Utility data last updated on {str(today)}. 
    """)

# Stat Sorter
if _ENABLE_PROFILING:
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    ts = int(time.time())
    with open(f"perf_{ts}.txt", "w") as f:
        f.write(s.getvalue())

# end