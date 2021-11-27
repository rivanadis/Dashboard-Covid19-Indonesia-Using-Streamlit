import datetime
from instabot import Bot
bot = Bot()
bot.login(username="imigrasi.jogja", password="tikkim2021")

def get_media_posts(start_date, end_date):
   all_posts = bot.get_your_medias()
   filtered_posts = []
   
   for post in all_posts:
       post_info = bot.get_media_info(post) #the media info for the post
       post_timestamp = post_info[0].get('taken_at') #get the timestamp of the post
       post_date = datetime.datetime.fromtimestamp(post_timestamp).date() #convert timestamp to date
       
       if post_date >= start_date and post_date <= end_date:
           filtered_posts.append(post) #or you can also use: filtered_posts.append(post_info)
    
   return filtered_posts

get_media_posts(2021-10-1, 2021-10-5)