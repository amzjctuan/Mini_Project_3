# EC601-Mini_Project_3: Mangodb / MySQL
2018 Fall - Boston University - EC601 #project_3

1. Twitter API: 
   Use twitter API to grab the photos form the twitter account.
   
2. ffmpeg:
   Transfer the photos downloaded from twitter into video.
   
3. Google Visial API:
   Describe each of the photos from the video made in the previous step.
   
4. Mnagodb (pymongo) / MySQL (mysql):
   Store all the information for each user.
   Calcuate the number of photos from the twitterID the user asked for.
   Find out the most popular google analysis description among all users.

# System Environment 
- Python 3.6.5
- ffmpeg 3.4.4
- Tweepy 3.6.0
- google-cloud-videointelligence 1.3.0
- Ubuntu 18.04.1 LTS
- pymongo
- pysql

   
# Program Description

There are three functions made in the mini_project_api.py.
- tweet_api
- ffmpeg
- google_analyze
- pymongo / pysql

You need to type the twitter account that you wanna grab the photos from.
Then, it will automatically help you to download all the photos from the account and translate each of the photos.
The data base will store all the infomation for each users and then you can retrieve the number of photos from each users.




# Note
Google application credentials:
```
export GOOGLE_APPLICATION_CREDENTIALS='google_application_credentials.json'
```
Make sure file 'google_application_credentials.json' has correct path.



