# Camry in the Car Lot
# Automotive Business Intelligence Tool Prototype
# Developed by Carston Koziol
# SI 699 Big Data Mastery Course 2023



###API KEY INPUT (########################################################################################################

marketstack_api_key =  #####paste Marketstack API key here
news_api_key =  ######paste News API key here



###### Running Application (Copy and paste in terminal without # sign) #################################################

#python -m streamlit run ccl_streamlit_app.py



###APPLICATION REQUIRES INTERNET ACCESS#################################################################################

## package installation as needed (uncomment line)
#pip install -r requirements.txt

##analytics libraries
import pandas as pd
import numpy as np
import re

##API Requesting libraries
import requests

##Web Scrapping Libraries
from bs4 import BeautifulSoup

##text summarization library
from summarizer import Summarizer

#dashboard libraries
import streamlit as st
from datetime import datetime



#### INITIAL DASHBOARD SETUP ##########################################################################################

st.set_page_config(layout='wide')

#title
col1, mid, col2 = st.columns([1,1,4])
with mid:
    st.image('Logo.jpg', width=85)
with col2:
    st.markdown("### **Camry in the Car Lot**")

    #Refresher with button
    st.markdown(f"##### Retrieval Date: {'{:%Y-%m-%d  %H:%M:%S}'.format(datetime.now())}")
    refresh_button = st.button('Refresh')
    if refresh_button:
        st.experimental_rerun()



##### STOCK MARKET DATA EXTRACTION ##################################################################################

## initial stock variable setup
### 3 markets, 8 companies available
### 5 markets, 22 companies total


## Market Tickers - 3 markets available, 5 markets with working krx and tyo market
nyse_market = 'XNYS'
nasdaq_market = 'XNAS'
otc_market ='PINC'
#krx_market = 'XKRX'    #relevant companies in market not available with API
#tyo_market = 'XTKS'    #relevant companies in market not available with API


## New York Stock Exchange (NYSE) Auto Tickers - 6 companies available, 8 companies total
general_motors = 'GM'
ford = 'F'
toyota = 'TM'
honda = 'HMC'
ferrari = 'RACE'
#tata = 'TTM'
#stellantis = 'STLA'    #company data not available with API
#lucid = 'LCID'         #company data not available with API
nyse_auto_list = {nyse_market: [general_motors, ford, toyota, honda, ferrari]}   #auto_list with accessible company data
#nyse_auto_list = {nyse_market: [general_motors, ford, stellantis, toyota, lucid, honda, tata, ferrari]}    #full auto list if all company data was accessible
        

## NASDAQ Auto Tickers - 1 company available, 2 companies total
tesla = 'TSLA'
#rivian = 'RIVN'    #company data not available with API
nasdaq_auto_list = {nasdaq_market: [tesla]}     #auto_list with accessible company data
#nasdaq_auto_list = {nasdaq_market: [tesla, rivian]}    #full auto list if all company data was accessible


## Over The Counter (OTC) Auto Tickers - 2 companies available, 10 companies total
bmw = 'BMWYY'
volvo = 'VLVLY'
#mazda = 'MZDAY'    #company data not available with API
#subaru = 'FUJHY'   #company data not available with API
#aston_martin = 'ARGGY' #company data not available with API
#nissan = 'NSANY'   #company data not available with API
#hyundai = 'HYMTF'  #company data not available with API
#volkswagen = 'VWAGY'   #company data not available with API
#porsche = 'POAHY'  #company data not available with API
#mercedes_benz = 'MBGYY'    #company data not available with API
otc_auto_list = {otc_market: [bmw, volvo]}  #auto_list with accessible company data
#otc_auto_list = {otc_market: [bmw, mazda, subaru, aston_martin, nissan, hyundai, volvo, volkswagen, porsche, mercedes_benz]}  #full auto list if all company data was accessible


## Korean Exchange (KRX) Auto Tickers - 0 companies available, 1 company total
#kia = '000270'     #company data not available with API
#krx_auto_list = {krx_market: [kia]}    #full auto list if all company data was accessible


## Tokyo Exchange (TFX) Auto Tickers - 0 companies available, 1 company total
#mitsubishi = '7211'    #company data not available with API
#tfx_auto_list = {tyo_market: [mitsubishi]}    #full auto list if all company data was accessible


all_markets_companies = [nyse_auto_list, nasdaq_auto_list, otc_auto_list]   #list of markets and adjacent companies with data available
#all_markets_companies = [nyse_auto_list, nasdaq_auto_list, otc_auto_list, krx_auto_list, tfx_auto_list]    #full list of markets and adjacent companies if all data available



#### INITAL DATA LANDSCAPE ASSESSMENT ##################################################################################

def company_stock_info(market_exchange, company):

    '''
    Accesses MarketAPI for specific company and returns relevant stock data on company

        market_exchange = specific exchange ticker for company
        company = company ticker 

    returns dictionary with company stock information to include open price, high price, low price,
    last price as of retrieval time, close price, volumne, date and time when data was retrieved, 
    ticker symbol, and exchange
    '''

    #real time parameters
    main_url = 'https://api.marketstack.com/v1/'    #request website
    test_symbol = company   #specific company
    test_exchange = market_exchange     #market company stock is in
    real_time = 'intraday/latest'   #object
    interval = '30min' #parameter (options 1min, 5min, 10min, 30min, 1hour, 3hour, 12hour, 24hour) 
    limit = 1
    real_time_params = {'access_key': marketstack_api_key, 'symbols': test_symbol, 'interval': interval,
                        'exchange': test_exchange, 'limit':limit}
    
    api_result = requests.get(main_url + real_time, real_time_params)
    api_response = api_result.json()

    try:
        return api_response['data'][0]
    except:
        print(f'issue with {company} ticker')


nyse_return_results = []
nasdaq_return_results = []
otc_return_results = []
krx_return_results = []
tyo_return_results = []

for auto_list in all_markets_companies: 
    for market, company_list in auto_list.items():
        for company in company_list:
            if market == 'XNYS':
                nyse_return_results.append(company_stock_info(nyse_market, company))
            elif market == 'XNAS':
                nasdaq_return_results.append(company_stock_info(nyse_market, company))
            elif market == 'PINC':
                otc_return_results.append(company_stock_info(nyse_market, company))
            elif market == 'XKRX':
                krx_return_results.append(company_stock_info(nyse_market, company))
            elif market == 'XTKS':
                tyo_return_results.append(company_stock_info(nyse_market, company))
            else:
                raise

company_ticker_name_dict = {'GM': 'General Motors', 'F': 'Ford', 'STLA': 'Stellantis',
                            'TM': 'Toyota', 'LCID': 'Lucid', 'HMC': 'Honda', 'TTM': 'Tata',
                            'RACE': 'Ferrari', 'TSLA': 'Tesla', 'RIVN': 'Rivian', 'BMWYY': 'BMW',
                            'MZDAY': 'Mazda', 'FUJHY': 'Subaru', 'ARGGY': 'Aston Martin',
                            'NSANY': 'Nissan', 'HYMTF': 'Hyundai', 'VLVLY': 'Volvo', 'VWAGY': 'Volkswagen',
                            'POAHY': 'Porsche', 'MBGYY': 'Mercedes Benz', '000270': 'KIA', '7211': 'Mitsubishi'}

auto_landscape_df = pd.concat([pd.DataFrame(nyse_return_results), 
                               pd.DataFrame(nasdaq_return_results), 
                               pd.DataFrame(otc_return_results), 
                               pd.DataFrame(krx_return_results), 
                               pd.DataFrame(tyo_return_results)])

auto_landscape_df['date'] = pd.to_datetime(auto_landscape_df['date'])
auto_landscape_df['company_name'] = auto_landscape_df['symbol'].apply(lambda x: company_ticker_name_dict[x])

try:
    auto_landscape_df.reset_index(inplace=True)
except:
    pass  

placement_levels = pd.Series(['1rst' , '2nd', '3rd', '4th'])


## performance level
def increase_v_decrease(row):

    '''
    Takes row of of data and determines whether number is considered a increase or decrease

        row = row of specified column

    returns either 'increase', 'decrease', or 'same'
    '''
    if row > 0:
        return 'increase'
    elif row < 0:
        return 'decrease'
    else:
        return 'same'

auto_landscape_df['close_v_open_diff'] = auto_landscape_df['open'] - auto_landscape_df['close']
auto_landscape_df['close_v_open_inc_dec'] = auto_landscape_df['close_v_open_diff'].apply(increase_v_decrease)
auto_landscape_df['last_v_open_diff'] = auto_landscape_df['last'] - auto_landscape_df['open']
auto_landscape_df['last_v_open_inc_dec'] = auto_landscape_df['last_v_open_diff'].apply(increase_v_decrease)

performance_level = auto_landscape_df[['company_name', 'close_v_open_inc_dec', 'last_v_open_inc_dec',
                                     'close_v_open_diff', 'last_v_open_diff']]

top_performing = performance_level.sort_values(['last_v_open_diff', 'close_v_open_diff'], ascending=[False, False])
top_performing = top_performing[['company_name', 'close_v_open_inc_dec', 'last_v_open_inc_dec']].head(4)
top_performing.set_index(placement_levels, inplace=True)

worst_performing = performance_level.sort_values(['last_v_open_diff', 'close_v_open_diff'], ascending=[True, True])
worst_performing = worst_performing[['company_name', 'close_v_open_inc_dec', 'last_v_open_inc_dec']].head(4)
worst_performing.set_index(placement_levels, inplace=True)


## stability level
auto_landscape_df['high_v_low_diff'] = auto_landscape_df['high'] - auto_landscape_df['low'] #if small number then stable, if larger number then unstable

most_stable = auto_landscape_df[['company_name', 'high_v_low_diff']].sort_values(by='high_v_low_diff', ascending = True).head(4)
most_stable.set_index(placement_levels, inplace=True)
least_stable = auto_landscape_df[['company_name', 'high_v_low_diff']].sort_values(by='high_v_low_diff', ascending = False).head(4)
least_stable.set_index(placement_levels, inplace=True)


## anomoly companies
def anomoly_determination(row):
    '''
    determines whether a companys performance could be considered an anomoly depending on threshold

        row = row of dataframe

    returns either 'anomoly' or 'normal':
    '''
    for change in ['close_v_open_pct_change', 'last_v_open_pct_change', 'high_v_low_pct_change']:
        if row[change] > 1.02 or row[change] < .99:
            return 'anomoly'
    
    return 'normal'

auto_landscape_df['close_v_open_pct_change'] = auto_landscape_df['open'] / auto_landscape_df['close']
auto_landscape_df['last_v_open_pct_change'] = auto_landscape_df['last'] / auto_landscape_df['open']
auto_landscape_df['high_v_low_pct_change'] = auto_landscape_df['high'] / auto_landscape_df['low']
auto_landscape_df['anomoly_status'] = auto_landscape_df.apply(anomoly_determination, axis=1)
anomoly_companies_list = list(auto_landscape_df[auto_landscape_df['anomoly_status'] == 'anomoly']['company_name'])
anomoly_companies_df = pd.DataFrame(anomoly_companies_list, columns=['companies'])
anomoly_companies_df.index += 1

st.markdown("#### Industry Overview")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    #Table 1 - Top Performing
    st.write(f"Top Performing")
    st.table(data=top_performing)

with col2:
    #Table 2 - Worst Performing
    st.write(f"Worst Performing")
    st.table(data=worst_performing)

with col3:
    #Table 3 - Most Stable
    st.write(f"Most Stable")
    st.table(data=most_stable)

with col4:
    #Table 4 - Most Volatile
    st.write(f"Most Volatile")
    st.table(data=least_stable)

with col5:
    #Table 5 - Anomoly Companies
    st.write(f"Anomoly Companies")
    st.table(data=anomoly_companies_df)


###### Specific Company Rating Assessment ########################################################################### 

st.write(' ')
st.write(' ')
st.markdown("#### Individual Company Status")

option = st.selectbox('Select Company', auto_landscape_df['company_name'])

comp_spec_1, comp_spec_2, comp_spec_3, comp_spec_4, comp_spec_5 = st.columns(5)
comp_spec_1.metric('Closing', auto_landscape_df[auto_landscape_df['company_name'] == option]['close'])
comp_spec_2.metric('Opening', auto_landscape_df[auto_landscape_df['company_name'] == option]['open'])
comp_spec_3.metric('Last', auto_landscape_df[auto_landscape_df['company_name'] == option]['last'])
comp_spec_4.metric('High', auto_landscape_df[auto_landscape_df['company_name'] == option]['high'])
comp_spec_5.metric('Low', auto_landscape_df[auto_landscape_df['company_name'] == option]['low'])



###### NEWS UPDATE CONSOLIDATION ####################################################################################

def text_summarization(url):

    '''
    Takes the url provided and utlizies BeautifulSoup inorder to access article and scrap content. The content is then
    run through the Bert Extractive Summarizer which produces a shortened story with the key takeaway elements.

        url = url of the given story for the specific company

    returns the summarized story text that gets added to the tuple with the other information regarding the story
    '''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraphs = soup.find_all('p')

    text = ''
    for paragraph in paragraphs:
        text += paragraph.get_text()

    try:
        bert_model = Summarizer()
        bert_summary = ''.join(bert_model(text, min_length=15))
        return bert_summary
    except:
        return text
    

def news_article_retrieval_technology(company_name):

    '''
    Accesses News API for headline news focused on technology based on company name provided and returns story title, the publisher, 
    the release date, and the url

        company_name = specific company that is being put into the API

    returns a list of all available stories for the given company with each story's
    relevant information wrapped in a tuple
    '''

    country = 'us'
    category = 'technology'

    q = company_name

    main_url = f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&q={q}&apiKey={news_api_key}'
    api_result = requests.get(main_url)
    api_response = api_result.json()

    if api_response['status'] == 'ok' and api_response['totalResults'] == 0:
        return f'No Results Found For {company_name}'
    elif api_response['status'] != 'ok':
        return 'Error with Retrieval'
    elif api_response['status'] == 'ok' and api_response['totalResults'] != 0:

        article_collection = []

        for story in api_response['articles']:
            story_title = story['title']
            story_publisher = story['source']['name']
            story_release_date = story['publishedAt']
            story_url = story['url']
            story_debrief = text_summarization(story_url)
            article_collection.append((story_title, story_publisher, story_release_date, story_debrief, story_url))  

        return article_collection
    
    else:
        raise


def news_article_retrieval_business(company_name):

    '''
    Accesses News API for headline news focused on business based on company name provided and returns story title, the publisher, 
    the release date, and the url

        company_name = specific company that is being put into the API

    returns a list of all available stories for the given company with each story's
    relevant information wrapped in a tuple
    '''

    country = 'us'
    category = 'business'

    q = company_name

    main_url = f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&q={q}&apiKey={news_api_key}'
    api_result = requests.get(main_url)
    api_response = api_result.json()

    if api_response['status'] == 'ok' and api_response['totalResults'] == 0:
        return news_article_retrieval_technology(company_name)
    elif api_response['status'] != 'ok':
        return 'Error with Retrieval'
    elif api_response['status'] == 'ok' and api_response['totalResults'] != 0:

        article_collection = []

        for story in api_response['articles']:
            story_title = story['title']
            story_publisher = story['source']['name']
            story_release_date = story['publishedAt']
            story_url = story['url']
            story_debrief = text_summarization(story_url)
            article_collection.append((story_title, story_publisher, story_release_date, story_debrief, story_url))  

        return article_collection
    
    else:
        raise

resulting_stories = []

for company in anomoly_companies_list:
    if ' ' in company:
        company = '_'.join(company.split(' '))
        company_info = news_article_retrieval_business(company)
        resulting_stories.append(company_info)
    else:
        company_info = news_article_retrieval_business(company)
        resulting_stories.append(company_info)



#### DASHBOARD NOTIFICATION UPDATER #################################################################################################

st.write(' ')
st.write(' ')
st.write(' ')
st.markdown("#### Automotive Updates")
with st.container():
        for company_stories in resulting_stories:
                if len(company_stories) >= 1 and 'No Results Found' not in company_stories:
                        for story in company_stories:
                                st.write(' ')
                                title = story[0]
                                publisher = story[1]
                                release_date = story[2]
                                story_debrief = story[3]
                                story_url = story[4]

                                st.markdown(f'##### {title}')
                                st.markdown(f'###### {publisher, release_date}')                        
                                st.write(story_debrief)
                                st.write(story_url)
                                st.write(' ')
                else:
                    st.write(' ')
                    st.write(company_stories)
                    st.write(' ')