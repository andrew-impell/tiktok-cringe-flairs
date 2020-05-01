from psaw import PushshiftAPI
import pandas as pd
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

POST_LIMIT = 10000000

api = PushshiftAPI()


start_epoch = int(datetime(2019, 4, 20).timestamp())

# grab data from api

pushresp = list(api.search_submissions(after=start_epoch,
                                       subreddit='TikTokCringe',
                                       filter=['link_flair_text'],
                                       limit=POST_LIMIT))

submission_list = []

# organize data

for t in pushresp:
    try:
        time = datetime.utcfromtimestamp(t.created).strftime('%Y-%m-%d')
        flair = t.link_flair_text
        submission_list.append([time, flair])
    except AttributeError:
        pass

print('Got Submissions...')

all_dates = []
for sub in submission_list:
    date = sub[0]
    all_dates.append(date)

date_set = list(set(all_dates))

# Create a df with flairs as columns and index of dates; vals are percentages

final_day_list = []

for date in date_set:
    temp_day_list = []
    for pair in submission_list:
        if pair[0] == date:
            temp_day_list.append(pair[1])
    count = Counter(temp_day_list).items()
    percentages = \
        {x: int(float(y) / len(temp_day_list) * 100) for x, y in count}
    final_day_list.append(percentages)


df = pd.DataFrame(final_day_list, index=date_set)
df.sort_index(inplace=True)


# Plot the data frame
x_ticks = list(df.index.values)
x_ticks = x_ticks[::25]

plt.stackplot(df.index, df['Humor'], df['Humor/Cringe'],
              df['Cringe'], df['Wholesome'],
              labels=['Humor', 'Humor/Cringe', 'Cringe', 'Wholesome'])
plt.legend(loc='upper right')
plt.title('TikTokCringe flairs over time')
plt.xticks(ticks=x_ticks, rotation=(45))
plt.xlabel('Date')
plt.ylabel('Percent of posts')
plt.show()
