# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import json 
import requests 
import pandas as pd


api_token = 'wR6uVuJhdEqHqCn7f6ZOKaHAy2mK2AfYCeAwVqCb'
workspace_id = 'c2f4db82-a46e-4128-862f-f0531ce8de03'

auth_url = 'https://eu-svc.leanix.net/services/mtm/v1/oauth2/token' 
request_url = 'https://eu-svc.leanix.net/services/mtm/v1/workspaces/%s/users?page=0'%(workspace_id) 

# Get the bearer token - see https://dev.leanix.net/v4.0/docs/authentication
response = requests.post(auth_url, auth=('apitoken', api_token),
                         data={'grant_type': 'client_credentials'})
response.raise_for_status() 
access_token = response.json()['access_token']
auth_header = 'Bearer ' + access_token
header = {'Authorization': auth_header}

# General function to call GraphQL given a query
def call():
  response = requests.get(url=request_url, headers=header)
  response.raise_for_status()
  return response.json()

#user['id'] + " " + 
email_list = []
first_name_list = []
last_name_list =[]
last_login_list = []

funct = call()

for user in funct['data']:
    email_list.append(user['email'])
    first_name_list.append(user['firstName'])
    last_name_list.append(user['lastName'])
    #last_login_list.append(user['lastLogin'])
    
df = pd.DataFrame()
df['First_Name'] = first_name_list
df['Last_Name'] = last_name_list
df['Email'] = email_list
df = df.set_index('First_Name')

first = []
current_login = []

for user in funct['data']:
    if len(user.keys())>15:
        first.append(user['firstName'])
        current_login.append(user['currentLogin'])

df1 = pd.DataFrame()
df1['First_Name'] = first
df1['currentLogin'] = current_login

df1 = df1.set_index('First_Name')

df = df.join(df1)
df.to_csv('output.csv')