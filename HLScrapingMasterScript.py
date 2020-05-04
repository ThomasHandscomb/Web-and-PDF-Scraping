############################################
# Title: Hargreaves Lansdown webpage scraper
# Author: Thomas Handscomb
############################################

################
# Import modules
################
import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Define url here
url = 'http://www.hl.co.uk/funds'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Extract the most viewed mutual funds 

def HLViewedScraper():
    webpage = requests.get(url)
    # Get webpage output
    soup = BeautifulSoup(webpage.content, "lxml")
    # 1. Find the daily most viewed funds
    ViewedFunds = soup.findAll("span", {"class": "title"})
    
    #print(ViewedFunds)   
    
    now = datetime.datetime.now()   
    
    df_page = pd.DataFrame(columns = ['Class', 'Date'])
        
    for i in range (0, 10):
        #print(pd.DataFrame({'Class':[ViewedFunds[i].get_text()], 'Date':[now.strftime("%Y-%m-%d")]}))
        df_page = df_page.append(pd.DataFrame({'Class':[ViewedFunds[i].get_text()], 'Date':[now.strftime("%Y-%m-%d")]}))
        df_page.reset_index(drop = True, inplace = True)
    return(df_page)
       
HLViewedScraper()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Extract the most bought mutual funds

def HLBoughtScraper():
    webpage = requests.get(url)
    # Get webpage output
    soup = BeautifulSoup(webpage.content, "lxml")
    # 1. Find the weekly most purchased funds
    BoughtFunds = soup.findAll("ul", {"class": "list-standard-styled list-blue-dot li-no-indent li-spacer-dbl"})
    
    now = datetime.datetime.now()
    text = ''
    for i in range (0, 2):
        textdynamic1 = BoughtFunds[i].get_text()
        textdynamic2 = " ".join(textdynamic1.split())
        textdynamic3 = textdynamic2.replace(") ", ")" + ",").lstrip()
        #text = text + "\n" + textdynamic3 + "," + now.strftime("%Y-%m-%d")
        text = text + "\n" + textdynamic3
        
    # Create and Transpose text data frame
    textdf = pd.read_csv(pd.compat.StringIO(text), header = -1).transpose()
    #textdf.columns = ['A', 'B']
    #textdf1 = pd.DataFrame(data = textdf)
    
    # Cut the two columns into 2 separate data frames
    textdf1 = pd.DataFrame(data = textdf.loc[:,0])
    textdf1.columns = ['Funds']
    
    textdf2 = pd.DataFrame(data = textdf.loc[:,1])
    textdf2.columns = ['Funds']
    
    # Append the two data frames together
    textdf3 = textdf1.append(textdf2, ignore_index=True)
    textdf3 = pd.DataFrame(data = textdf3)
    
    #print(textdf3)
    #print(textdf3.shape)
    
    # Add in date column
    textdf3['Date'] = now.strftime("%Y-%m-%d")
    #textdf3 = textdf3.reset_index()
    
    # Add in rank column
    textdf3.insert(2, 'Rank', range(1, 1 + len(textdf3)))
    
    # Reorder data frame columns
    textdf3 = textdf3[['Date', 'Funds', 'Rank']]
    
    print(textdf3)      

HLBoughtScraper()
