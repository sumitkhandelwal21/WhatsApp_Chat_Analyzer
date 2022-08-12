import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern,data)[1:]
    
    dates = re.findall(pattern,data)
    
    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'],format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date':'date'},inplace=True)
    
    # Seperate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])   # user_name
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
           
    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'],inplace=True)
    
    # Extracting years,month,day,time(hr,min) from date column
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year

    # Converting time(hour,minute)
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    # Dropping the group_notification messages
    df.drop(df[df['user']=='group_notification'].index,axis=0,inplace=True)
    df.reset_index(drop=True,inplace=True)
    
    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour == 0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
        
    df['period']=period
    return df