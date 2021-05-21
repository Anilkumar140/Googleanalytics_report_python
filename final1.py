from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import httplib2, json
import pandas as pd
from datetime import datetime, timedelta
def getGoogleAnalyticsReport():
    try:
        url="/public"
        daysago=str(datetime.now() + timedelta(days=-6))

        credentials = ServiceAccountCredentials.from_json_keyfile_name('keypath/ppksdailyreport-7d055aac1e17.json'  , ['https://www.googleapis.com/auth/analytics.readonly'])

        #Create a service object
        http = credentials.authorize(httplib2.Http())
        service = build('analytics', 'v4', http=http, discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))
        response = service.reports().batchGet(
            body={
                "reportRequests": [
                {
                    "viewId": "242438292", 
                    "samplingLevel": "DEFAULT",
                    "filtersExpression": "ga:pagePath==" +url, 
                    "dateRanges": [
                    {
                        "startDate": daysago[0:10],
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
        # val.reverse()
        # dim.reverse()
        
        df = pd.DataFrame() 
        df["Pageviews"]=val
        for row in dim:
            datetimeobject = datetime.strptime(row,'%Y%m%d')
            date.append(datetimeobject.strftime("%Y-%m-%d"))
        df["date"]=date
        df=df[["date","Pageviews"]]

        # df_list = df.values.tolist()
        # df_list = list(df.values.flatten())
        df_list = json.loads(df.to_json(orient='records'))
        for i in range(0,7):
            if datetime.today().strftime("%Y-%m-%d") == df_list[i]['date']:
                df_list[i]['date'] = "Today"
        return df_list
    except:
        response_object = {
            "status": "fail",
            "message": "Google Analytics Report could not be fetched."
        }
        return response_object, 400
      
print(getGoogleAnalyticsReport())