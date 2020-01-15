import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from time import time

# Checks if file exists, if it does, delete and 
# create a blank version, just column headers.

def check_file(repo_path,filename):
    full_file=repo_path+"\\"+filename+".csv"
    if os.path.exists(full_file)==True:
        os.remove(full_file)
    df3=pd.DataFrame(columns=['Event','Date','Start Time','Game','Category','Platform','Runners','Host'])
    return df3.to_csv(full_file)

#def check_donations(repo_path,filename):
#    full_file=repo_path+"\\"+filename+".csv"
#    if os.path.exists(full_file)==True:
#        os.remove(full_file)
#    df_donation=pd.DataFrame(column=)
    
# Scrape GDQ website for a given event, and 
# download the schedule. Cleans up formatting.        

def get_schedule(repo_path,filename,index):
    try:
        url='https://gamesdonequick.com/schedule/'+str(index)
        html=requests.get(url).content
    except:
        print("Connection error. Retrying.")
        time.sleep(5)
    
    get_text=requests.get(url).text
    soup=BeautifulSoup(get_text,"html.parser")
    
    event=soup.find('h1',{'class': 'text-gdq-red extra-spacing'}).text[0:8]
    
    df_list=pd.read_html(html)
        
    for i, df in enumerate(df_list):
        df.to_csv('table {}.csv'.format(i))
        
    df1 = df[::2]
    df2 = df[1::2]
    
    df1.reset_index(inplace=True,drop=True)
    df2.reset_index(inplace=True,drop=True)
    df1.columns = ['Start Time Date','Game','Runners','Setup Time']
    df2.columns = ['Duration','Category','Host','Setup Time2']
    
    df3=df1.join(df2)
    cats=df3["Category"].to_frame()
    cats=pd.DataFrame(cats["Category"].str.split(" — ",1).tolist(),columns=["Category","Platform"])
    cats["Platform"]=cats["Platform"].str.upper()    
    
    df3['Date'] = df3['Start Time Date'].str.slice(0,10)
    df3['Start Time'] = df3['Start Time Date'].str.slice(11,16)
    df3['Event']=event
    
    del df3['Start Time Date'],df3['Setup Time'],df3['Setup Time2'],df3["Category"]
    df3=df3.join(cats)
    df3 = df3[['Event','Date','Start Time','Game','Category','Platform','Runners','Host']][1::]
    
    
    full_path=repo_path+"\\"+ filename +'.csv'
    df3.to_csv(full_path,mode='a',header=False)
    os.remove("table 0.csv")
    return df3

# Standardize console names. Will need evaluated event
# event, to ensure no new variations are present.

def platform_cleanup(dataset):
    dataset['Platform'].replace({
            'ARCADE':'ARC',
            'BATTLETOADS':'NES',
            'DREAMCAST':'DC',
            'FAMICOM':'FC',
            'FAMICOM DISK':'FCD',
            'GAME BOY':'GB',
            'GAME BOY COLOR':'GBC',
            'GAMECUBE':'GCN',
            'GC':'GCN',
            'GENESIS':'GEN',
            'DS':'NDS',
            'MEGADRIVE':'SMS',
            'NEO GEO':'NEO-GEO',
            'NES AND SNES':'NES/SNES',
            'NINTENDO':'NES',
            'NINTENDO 64':'N64',
            'NINTENDO DS':'NDS',
            'NINTENDO SWITCH':'SWITCH',
            'NINTENDO WII':'WII',
            'PC ENGINE':'PCE',
            'PLAYSTATION':'PSX',
            'PLAYSTATION 2':'PS2',
            'PLAYSTATION 3':'PS3',
            'PLAYSTATION 4':'PS4',
            'PLAYSTATION 4 PRO':'PS4',
            'PS1 (ON PS2)':'PS1',
            'SATURN':'SAT',
            'SEGA MASTER':'SMS',
            'SUPER NINTENDO':'SNES',
            'TG-16':'TG16',
            'WII U':'WIIU',
            'WII U VC':'WIIU VC',
            'XBOX 360':'X360',
            'XBOX360':'X360',
            'XBOX ONE':'XBONE',
            'IPAD':'OTHER',
            "IT'S A MYSTERY":'OTHER',
            'TWITCHCON':'OTHER',
            'WSHP':'OTHER',
            'AGDQ':'OTHER'
            },inplace=True)   
    return dataset
    

#function for pulling donation information

def donation_pull(repo_path,filename,index):
    try:
        url='https://gamesdonequick.com/tracker/event/'+str(index)
        html=requests.get(url).content
    except:
        print("Connection error. Retrying.")
        time.sleep(5)
    
    df_donate=pd.read_html(html)
        
    for i, df in enumerate(df_donate):
        df.to_csv('table {}.csv'.format(i))
    
        full_path=repo_path+"\\"+ filename +'.csv'
    df_donate.to_csv(full_path,mode='a',header=False)
    os.remove("table 0.csv")
    return df_donate
    

    
