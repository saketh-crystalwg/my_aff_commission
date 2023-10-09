import json
import pandas as pd
import datetime
import  requests
from requests.auth import HTTPBasicAuth
import xmltodict


r = requests.get('https://admin.crystalwgpartners.com/feeds.php?FEED_ID=25&FROM_DATE=2023-09-01&TO_DATE=2023-09-07',\
                auth = HTTPBasicAuth('SakethGV', 'CWGfg2023!'))

data_dict = xmltodict.parse(r.text)

json_data = json.dumps(data_dict)

df = json.loads(json_data)

print(df)

df_1 = pd.DataFrame(df)

print(df_1)