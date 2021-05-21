#Load Libraries
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import httplib2
import pandas as pd
from datetime import datetime, timedelta
url="/public"
# daysago=str(datetime.now() - timedelta(days=-7))

# today = datetime.date.today()
daysago = str((datetime.now() - timedelta(days=7)).date()) 
today=str(datetime.today().strftime('%Y-%m-%d'))
#Create service credentials
#Rename your JSON key to client_secrets.json and save it to your working folder
credentials = ServiceAccountCredentials.from_json_keyfile_name('keypath/ppksdailyreport-7d055aac1e17.json', ['https://www.googleapis.com/auth/analytics.readonly'])
  
#Create a service object
http = credentials.authorize(httplib2.Http())
service = build('analytics', 'v4', http=http, discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))
response = service.reports().batchGet(
    body={
        "reportRequests": [
          {
            "viewId": "243407740", 
            "samplingLevel": "DEFAULT",
            "filtersExpression": "ga:pagePath==" +url, 
            "dateRanges": [
              {
                "startDate": daysago,
                "endDate": "today"
              }
            ],
            "metrics": [
              {
                "expression": "ga:pageviews",
                "alias": ""
              }
            ],
            "dimensions": [
             {'name': 'ga:date'}
            ]
          }
        ]
    }
).execute()
 
#create two empty lists that will hold our dimentions and sessions data
dim = []
val = []
date = []
  
#Extract Data
for report in response.get('reports', []):
  
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])
  
    for row in rows:
  
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])
  
        for header, dimension in zip(dimensionHeaders, dimensions):
            dim.append(dimension)
  
        for i, values in enumerate(dateRangeValues):
            for metricHeader, value in zip(metricHeaders, values.get('values')):
                val.append(int(value))
 
#Sort Data
val.reverse()
dim.reverse()
 
df = pd.DataFrame() 
df["Pageviews"]=val

print(daysago)
for row in dim:
    datetimeobject = datetime.strptime(row,'%Y%m%d')
    # print(datetimeobject)
    date.append(datetimeobject)

for n, i in enumerate(date):
  if i == 1:
    date[i] = today
print(today)
   
df["date"]=date

df=df[["date","Pageviews"]]
df
 
#Export to CSV
df.to_csv("page_by_session.csv")