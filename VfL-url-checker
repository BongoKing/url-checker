#Import stuff
import pandas as pd
from bs4 import BeautifulSoup,SoupStrainer
import urllib.request
import colorama,re,queue,threading
from colorama import Fore
from urllib.parse import *
from datetime import date

#load dataframe from csv
df = pd.read_csv("C:/Users/hille/Downloads/vfu-artikeleintragung-2020-05-18.csv")

#print dataframe
print(df)

#select url
links = df['Zum Dokument']

#url checker function
def check(address):
    try:
        req=urllib.request.Request(url=address)
        resp=urllib.request.urlopen(req)
        if resp.status in [400,404,403,408,409,501,502,503]:
            print(Fore.RED + resp.status + "-" + resp.reason + "-->" + address)
        else: 
            print(Fore.GREEN + "no problem in-->" + address)
            
    except Exception as e:
            print(Fore.RED + "{}-{}".format(e,address))
            pass

#show results of url checker function and export it to a txt file
output = open("vfu_linkcheck" + str(date.today()) +".txt","w")
i=1
for link in links:
    print(str(check(link)))
    output.write(str(i) + ": " + str(check(link)) + "\n")
    i = i + 1
output.close()
