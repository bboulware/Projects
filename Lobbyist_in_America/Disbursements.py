#Importing Libraries needed
import requests 
import pandas as pd 
import numpy as np 
import time 
import json 

# The Api key used to gain access to endpoint assigned to user.
api_key = 'ENTER API KEY' 

# End point url for the FEC distribution API. 
endpoint_url=f'https://api.open.fec.gov/v1/schedules/schedule_b/?sort=-disbursement_date&sort_null_only=false&sort_hide_null=false&api_key={api_key}&per_page=40'

# This excel file contains the information of the top lobbying organzations and id(fec.gov) numbers in the country according to stastic.com  
df=pd.read_excel(r'C:\Users\bboul\Downloads\committees.xlsx') 
 
# List of urls to request data by committee.  
url_request_list=[]
  
# Class to create list of request, get request and retrieve data, and save to CSV.
class Disbursements_Data:
    def __init__(self):
        self.committee_parameter()
        for self.url in url_request_list:
            self.data_list=[]
            self.first_requests()
            if self.pages > 1:
                self.page_request()
            else:
                pass
            self.create_csv()
  
# Function retrieves ids from excel document 'committee.xlsx'
# Groups the IDs together by name then creates endpoint for those committee groups.
    def committee_parameter(self):
        committees=df['committee_id'] 
        seperater = '&committee_id=' 
        for self.id in committees: 
            parameter= seperater+str(self.id)
            url_request_list.append(endpoint_url+parameter)
 
# Creates first request from URL in url_request_list endpoints
    def first_requests(self): 
        #Making the request with the url created      
        r = requests.get(self.url) 
        first_data = r.json()         
        # Retrieves amount of pages and next page information (last_date, last_index)
        self.pages=first_data['pagination']['pages']
        self.next_page_info=first_data['pagination']['last_indexes']
        # Adding data to list        
        for results in  first_data['results']: 
            self.data_list.append(results)
        #Printing feedback information         
        print('first_data: '+ str(r.status_code))
        print('Pages: '+str(self.pages))
        print('\n') 
	 
# Uses next_page_data from first_request adds it to endpoint to request next page data  
    def page_request(self):
        # Looping through correct amount of pages
        for page in range(self.pages):
            time.sleep(2)
        
            # Creating string from page information to append to url for next page.
            keys=list(self.next_page_info.keys())
            values=list(self.next_page_info.values())
            page_info=keys[0]+'='+values[0]+'&'+keys[1]+'='+values[1][:10]
            try:
                #Making request from url and next page information    
                r2=requests.get(str(self.url)+'&'+str(page_info))
                page_data=r2.json()
                self.next_page_info = page_data['pagination']['last_indexes']
            except:
                r2=requests.get(str(self.url)+'&'+str(page_info))
                page_data= json.loads(r2.text)
                self.next_page_info = page_data['pagination']['last_indexes']
                
            for results in page_data['results']:
                self.data_list.append(results)            
            # Printing feedback information
            print('Page_data: ' + str(r2.status_code))
            print('Page Number: '+str(page+1) +' of '+ str(self.pages))
            print(str(self.url)+'&'+str(page_info))
            print('\n')

# Function to create and save data to CSV saved as the type of request followed by the pages             
    def create_csv(self):
        if self.data_list != []:
            data=pd.DataFrame(self.data_list)
            data.to_csv(f'C:/Users/bboul/OneDrive/Documents/fec_distributions_data/disbursements_{data["committee_id"][0]}.csv', index=False)
            time.sleep(120)
        else:
            pass

Disbursements_Data() 
