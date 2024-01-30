import json
import pandas as pd
import datetime as dt
import  requests
from requests.auth import HTTPBasicAuth
import xmltodict
from datetime import datetime, timedelta
import os, requests
from sqlalchemy import create_engine
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

proxyDict = {
              "http"  : os.environ.get('FIXIE_URL', ''),
              "https" : os.environ.get('FIXIE_URL', '')
            }

date = dt.datetime.today()-  timedelta(1)
date_1 = date.strftime("%Y-%m-%d")

def send_mail(send_from,send_to,subject,text,server,port,username='',password=''):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(recipients)
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    
    smtp = smtplib.SMTP_SSL(server, port)
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

sender = "sakethg250@gmail.com"
recipients = ["sakethg250@gmail.com","marcos@crystalwg.com"]
password = "xjyb jsdl buri ylqr"


r = requests.get(f'https://admin.crystalwgpartners.com/feeds.php?FEED_ID=25&FROM_DATE={date_1}&TO_DATE={date_1}',\
                auth = HTTPBasicAuth('SakethGV', 'CWGfg2023!'), proxies=proxyDict)

data_dict = xmltodict.parse(r.text)

json_data = json.dumps(data_dict)

df = json.loads(json_data)

df = pd.DataFrame(df)

df_1 = pd.json_normalize(df['EARNINGS']['USER'])

df_1.rename(columns = {'@USER_ID': 'Affiliate_ID',\
                       'PLAN.@PLAN_ID': 'Plan_ID','PLAN.PLAYER_GROUP.@PLAYER_GROUP_ID': 'PLAYER_GROUP_ID',\
                      'PLAN.PLAYER_GROUP.ABSOLUTE_EARNINGS':'ABSOLUTE_EARNINGS',\
                      'PLAN.PLAYER_GROUP.EFFECTIVE_EARNINGS':'EFFECTIVE_EARNINGS'}, inplace = True)

df_1['date'] = date_1

try:
    engine = create_engine('postgresql://orpctbsqvqtnrx:530428203217ce11da9eb9586a5513d0c7fe08555c116c103fd43fb78a81c944@ec2-34-202-53-101.compute-1.amazonaws.com:5432/d46bn1u52baq92',\
                           echo = False)

    df_1.to_sql('my_affiliates_commission', con = engine, if_exists='append')
    
    subject = f'My Affiliates commission data ingestion for {date_1} is Successful'
    body = f"My Affiliates commission data ingestion for {date_1} is Successful"
    send_mail(sender, recipients, subject,body, "smtp.gmail.com", 465,sender,password)
except Exception as ex:
    subject = f'My Affiliates commission data ingestion for {date_1} is Failed'
    body = f"My Affiliates commission data ingestion for {date_1} is failed due to \n {str(ex)}"
    send_mail(sender, recipients, subject,body, "smtp.gmail.com", 465,sender,password)