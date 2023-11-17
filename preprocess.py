import re
import pandas as pd
import helper

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            # Check if the entry is a phone number
            if re.match(r'\+\d{1,4}-\d{1,12}', entry[1]):
                users.append('phone_number')
            else:
                users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

# Read data from file
with open('chat_dataset.txt', 'r') as file:
    data = file.read()

# Process data
result_df = preprocess(data)

#fetch unique users
user_list = result_df['user'].unique().tolist()
# user_list.remove('group_notification')
user_list.sort()
user_list.insert(0,"Overall")

timeline = helper.monthly_timeline("user3",result_df)
daily_timeline = helper.daily_timeline("user3", result_df)
busy_day = helper.week_activity_map("user3",result_df)
busy_month = helper.month_activity_map("user3", result_df)
user_heatmap = helper.activity_heatmap("user3",result_df)
x,new_df = helper.most_busy_users(result_df)
most_common_df = helper.most_common_words("user3",result_df)

group_notification_messages = result_df[result_df['user'] == 'group_notification']['message']


emoji_df = helper.emoji_helper("Guddi RML",result_df)

# Print the messages
print("EMO:",emoji_df)

#print("most_common_df:",most_common_df)
#print("x:",x)
#print("new_df",new_df)
#print("timeline:",timeline)
#print("daily timeline:",daily_timeline)
#print("busy_day:",busy_day)
#print("busy_month:",busy_month)
#print("user_heatmap:",user_heatmap)
# Print the result
#print(result_df)
print(user_list)
num_messages, words, num_media_messages, num_links = helper.fetch_stats("group_notification",result_df)
print("Numbers of messages :",num_messages)
print("Numbers of words:",words)
print("Numbers of media messages:",num_media_messages,)
print("Numbers of Links:",num_links)
