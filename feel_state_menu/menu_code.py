# Libaries needed
import json
import requests
import numpy as np
import pandas as pd 
import regex as re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string
from pandas.api.types import CategoricalDtype
import time

#Temporary Dictionary
menu_dictionary = {'Type':[],'Brand':[],'Name':[],'Weight':[], 'THC_content':[], 'CBD_content':[],'Price':[]}
# While loop to retrieve data
# Loop tries 3 times if get request was unsucessful
data = ''
while data == '' :
    try:
        site_url = 'https://stlouis.myfeelstate.com/graphql?operationName=FilteredProducts&variables={"includeEnterpriseSpecials":false,"includeCannabinoids":true,"productsFilter":{"dispensaryId":"600f5a29d692585e7ffd25e4","pricingType":"med","strainTypes":[],"subcategories":[],"Status":"Active","types":[],"useCache":false,"sortDirection":1,"sortBy":null,"isDefaultSort":true,"bypassOnlineThresholds":false,"isKioskMenu":false,"removeProductsBelowOptionThresholds":true},"page":0,"perPage":500}&extensions={"persistedQuery":{"version":1,"sha256Hash":"aed681974c9093e0cc3099ef18a8d37e17e4916a9f7743dd372e0be6b13c8f10"}}'
        r= requests.get(site_url)
        data = r.json()
        global product_data
        product_data= data['data']['filteredProducts']['products']
    except:
        time.sleep(2)

# Flower,Pre-Rolls,Concentrate,Vaporizers these are to be displayed showing percentage of thc and cbd
# Tincture,Topicals,CBD,Edible these are to be displayed showing miligrams(mg) of thc and cbd
# Functions to retrieve cleand and upload data to dictionary 
def retrieve_name(item):
    # parses json for the name of product and removes the weight text from the name 
    name = re.sub(weight, '', product)
    menu_dictionary['Name'].append(name.strip())
    menu_dictionary['Weight'].append(weight)


def retrieve_weight_gram(item):
    # assigns weight unit variable from json and weight amount, divides the weight to keep values uniform
    unit_dictionary= {'Milligrams':'g'}
    weight_unit= item['measurements']['netWeight']['unit'].title()
    weight =  str(item['measurements']['netWeight']['values'][0]/1000)+unit_dictionary.get(weight_unit)
    menu_dictionary['Weight'].append(weight)
   
def retrieve_weight_mg(item):  
    # assigns weight unit variable from json and weight amount, concats suffix to measurement value
    unit_dictionary_2= {'Percentage':'%','Milligrams':'mg','Milliliters':'ml'}
    weight_unit= item['measurements']['netWeight']['unit'].title()
    weight=''.join(str(item['measurements']['netWeight']['values']).strip('[]')+unit_dictionary_2.get(weight_unit))
    menu_dictionary['Weight'].append(weight)

def CBD_percentage(item):
    # if statment to verify product has CDB content and larger than 0
    # concats "mg" to value appends to dictionary
    if item['CBDContent'] == None:
        menu_dictionary['CBD_content'].append(' ')
    elif item['CBDContent']['range'] != None and item['CBDContent']['range'][-1] > 0:
        CBD_content =  str(item['CBDContent']['range'][-1]).strip('[]')+'%'
        menu_dictionary['CBD_content'].append(CBD_content)
    else:
        menu_dictionary['CBD_content'].append(' ')

def CBD_content(item):
     # if statment to verify product has CDB content and larger than 0
     #concats "mg" to value appends to dictionary
    if (item['CBDContent']['range'] != None) and (item['CBDContent']['range'][-1] > 0):
        CBD_content =  str(item['CBDContent']['range'][-1]).strip('[]')+'mg'
        menu_dictionary['CBD_content'].append(CBD_content)
    else:
        menu_dictionary['CBD_content'].append(' ')
        
def THC_percentage(item):
    # if statment to verify product has THC content and larger than 0
    # concats "mg" to value appends to dictionary
    if item['THCContent']['range'] != None and (item['THCContent']['range'][-1] > 0):
        THC_content = str(item['THCContent']['range'][-1]).strip('[]')+'%'
        menu_dictionary['THC_content'].append(THC_content)
    else:
         menu_dictionary['THC_content'].append(' ')


def THC_content(item):
    # if statment to verify product has THC content and larger than 0
    # concats "mg" to value appends to dictionary
    if item['THCContent']['range'] != None and (item['THCContent']['range'][-1] > 0):
        THC_content = str(item['THCContent']['range'][-1]).strip('[]')+'mg'
        menu_dictionary['THC_content'].append(THC_content)
    else:
         menu_dictionary['THC_content'].append(' ')


def retrieve_price(item):
    global price
    #if statement to verify if price is float or integar
    #Price needs to be displayed with decimal only when required example $21.50 example $21
    if isinstance(max(item['Prices']), float):
        price = '{:.2f}'.format(max(item['Prices']))
        menu_dictionary['Price'].append('$'+ price)
    else:
        price = max(item['Prices'])
        menu_dictionary['Price'].append('$'+str(price))


# Sets range of table to be used with google sheets api
def get_range(df):
    range_end= [(i,word) for i,word in zip(string.ascii_uppercase, df.columns.values)][-1][0]
    global table_range
    table_range = f'A:{range_end}'

# Function to sort data according to menu layout 
def custom_sort(df):
    house_brands=['Heya','Robust','Lush Labs','Packs Cannabis']
    df.fillna('', inplace=True)
    # How the Categories are to be displayed 
    sort_types = CategoricalDtype(['Vaporizers','Edible','Concentrate','Topicals','Tincture','CBD','Accessories','Apparel'], ordered =True)
    
    # Seperates house brand flowers from non house brands(n_h_flower) sorts them and concats them back together
    house_flower = df.loc[(df['Type'] == 'Flower')&(df['Brand'].isin(house_brands))].sort_values(by=['Brand','Name'], ascending=[False, True])
    n_h_flower = df.loc[(df['Type'] == 'Flower')&(~df['Brand'].isin(house_brands))].sort_values(by=['Brand','Name'])
    flower = pd.concat([house_flower, n_h_flower])

    # Seperates house brand prerolls from non house prerolls(n_h_prerolls) sorts them and concats them back together
    house_prerolls = df.loc[(df['Type'] == 'Pre-Rolls')&(df['Brand'].isin(house_brands))].sort_values(by=['Brand','Name'])
    n_h_prerolls = df.loc[(df['Type'] == 'Pre-Rolls')& (~df['Brand'].isin(house_brands))].sort_values(by=['Brand','Name'])
    prerolls = pd.concat([house_prerolls, n_h_prerolls])

     # Seperates house brand prerolls from non house vaporizers sorts them and concats them back together
    house_vapes = df.loc[(df['Type'] == 'Vaporizers')&(df['Brand'].isin(house_brands))].sort_values(by=['Brand','Name'])
    n_h_vapes = df.loc[(df['Type'] == 'Vaporizers')& (~df['Brand'].isin(house_brands))].sort_values(by=['Brand','Name'])
    vapes = pd.concat([house_vapes, n_h_vapes])

    # Items to be dropped by index
    drop_list = list(flower.index) + list(prerolls.index) + list(vapes.index)
    non_house_brands = df.drop(labels=drop_list)
    non_house_brands['Type'] = non_house_brands['Type'].astype(sort_types)
    
    #sorts table according to Type Then Brand then Name
    non_house_brands= non_house_brands.sort_values(by=['Type','Brand','Name'])

    #concates new sorted categories house brands and non house brands
    clean_data= pd.concat([flower,prerolls,vapes,non_house_brands]).applymap(str)
    clean_data= clean_data.drop_duplicates()

    global menu
    #creates menu variable and ransform data to correct format for googlesheets api 
    menu = clean_data.values.tolist()

    # Main loop that iterates over JSON reponse and filters data
for item in product_data:
    # Types are used to separate how they will be displayed 
    gram_type= ['Flower','Pre-Rolls','Concentrate','Vaporizers']
    mg_type= ['Tincture','Topicals','CBD','Edible']
    
    # Removing brand from name category 
    brand = str(item['brandName'])
    product= str(item['Name']).strip()
    product= re.sub(brand, '', product)
    product= re.sub('[-|]', '', product)

    # Adding type, brand to dictionary 
    menu_dictionary['Type'].append(item['type'])
    menu_dictionary['Brand'].append(brand)
    
    # Functions to clean data then append to dictionary
    retrieve_price(item)

    #Searching name for weight to remove and use as weight
    weight = re.search('\d.\d+g$|\d+g$|\d*mg$|^ \d+.*ck$|\d+ml$', product)
    
    #If statements are based on menu perferences on how menu item are to be displayed (GRAMS vs MILIGRAMS)
    #If producti is to be displayed using grams 
    if (weight != None) and (item['type'] in gram_type):
        weight = weight.group() 
        retrieve_name(item)
        CBD_percentage(item)
        THC_percentage(item)
    # If product is to be displayed using miligrams     
    elif (weight != None) and (item['type'] in mg_type):
        weight = weight.group() 
        retrieve_name(item)
        CBD_content(item)
        THC_content(item)
    # If product CBD and THC content to be displayed in garams 
    elif (item['type'] in gram_type) and (item['measurements']['netWeight']['values'] != []):
        menu_dictionary['Name'].append(product)
        retrieve_weight_gram(item)
        CBD_percentage(item)
        THC_percentage(item)
    # If product CBD and THC content to be displayed in milligarams 
    elif (item['type'] in mg_type) and (item['measurements']['netWeight']['values'] != []):
        menu_dictionary['Name'].append(product)
        retrieve_weight_mg(item)
        CBD_content(item)
        THC_content(item) 
    # Other products such as accessories and apparel do not receive THC or CBD content   
    else:
        menu_dictionary['THC_content'].append(' ')
        menu_dictionary['CBD_content'].append(' ')
        menu_dictionary['Weight'].append(' ')
        menu_dictionary['Name'].append(product.strip())
# Converting dictionary to pandas dataframe    
df =pd.DataFrame.from_dict(data=menu_dictionary)
get_range(df)
custom_sort(df)

# Using json API Key to make connection to google sheets using gspread python library
# json_key will be saved to client computer ACTION REQURIED must insert json key into '' 
client = gspread.service_account(r'C:\Users\bboul\Desktop\feel_state_key.json')
# Opening workbook
workbook= client.open('Feel_State')
# Opening First Worksheet
worksheet = workbook.get_worksheet(0)
# Clearing the Sheet 
worksheet.clear()
# Updating new Data
worksheet.update('A:G', menu)
