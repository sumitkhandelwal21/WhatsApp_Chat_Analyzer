from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract=URLExtract()
def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
        
    # 1. fetch the no. of messages
    num_messages = df.shape[0]
    
    # 2. fetch the total no. of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
    
    # 3. fetch the no. of media shared
    num_media_msg = df[df['message']=='<Media omitted>\n'].shape[0]
    
    # 3. fetch the no. of links shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))       
    return num_messages,len(words),num_media_msg,len(links)


def most_busy_users(df):
    
    top5 = df['user'].value_counts().head()
    
    df_percent = round((df['user'].value_counts()/df.shape[0])*100,3).reset_index().rename(columns={'index':'name','user':'percent'})
    return top5,df_percent


def create_wordcloud(selected_user,df):
    
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    # Excluding 'Media omitted>\n' from df
    temp=df[df['message'] != '<Media omitted>\n']
    
    # Removing the hinglish stop_words
    def remove_stop_words(message):
        words=[]
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
        
    wc = WordCloud(width=400,height=400,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))  
    return df_wc


def most_common_words(selected_user,df):
    
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    # Excluding 'Media omitted>\n' from df
    temp=df[df['message'] != '<Media omitted>\n']
    
    # Excluding the hinglish stop_words
    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.distinct_emoji_list(message)])
      
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
        
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
        
    timeline['time']=time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
        
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
        
    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap