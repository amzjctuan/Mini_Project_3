#!/usr/bin/env python
# encoding: utf-8
#Author - Jessie Tuan

# Twitter API
import tweepy
import json
import csv
import urllib.request
import io
import os
# ffmpeg
import ffmpeg
# Google API
import argparse
import sys
from google.cloud import videointelligence
import io
#MongoDB
import pymongo
from pymongo import MongoClient

import mysql.connector

## Twitter API credentials
consumer_key = 'OSyoPl5h5woBUX0x1vnYUjNQR'
consumer_secret = 'ibwVbguvtMmcIlM3AdMJ3WPq0yd8HjfczRunoblYHLPGIKMVId'
access_token = '1039645304008597510-WkpUCiV1m6yLoq54im2heOiNQXFsZs'
access_token_secret = 'qk817bo5pkrW2z2zVZi9sO9BQ1zEWwsc8MZMgfQOGMsld'


class mini_project_1:

    def __init__(self,twitterID):
        self.twitterID = twitterID

    # Step 1: Tweet API
    def tweet_api(self):

        print("\n========== Start Twitter Photo Capturing ==========")

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # #print all the tweets from twitter
        # public_tweets = api.home_timeline()
        # for tweet in public_tweets:
        #     print (tweet.text)

        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=self.twitterID, count=1)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:

            print("getting tweets before %s" % (oldest))

            #all subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(
                screen_name=self.twitterID, count=200, max_id=oldest)

            #save most recent tweets
            alltweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print("...%s tweets downloaded so far" % (len(alltweets)))

        #go through all found tweets and remove the ones with no images
        outtweets = []  #initialize master list to hold our ready tweets
        for tweet in alltweets:
            #not all tweets will have media url, so lets skip them
            try:
                print(tweet.entities['media'][0]['media_url'])
            except (NameError, KeyError):
                #we dont want to have any entries without the media_url so lets do nothing
                pass
            else:
                #got media_url - means add it to the output
                outtweets.append([
                    tweet.id_str, tweet.created_at,
                    tweet.text.encode("utf-8"),
                    tweet.entities['media'][0]['media_url']
                ])

        #write the csv
        with open('%s_tweets.csv' % self.twitterID, 'w') as f:
            writer = csv.writer(f)
            # writer.writerow(["id","created_at","text","media_url"])
            writer.writerows(outtweets)

        pass

        with open('%s_tweets.csv' % self.twitterID) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            url_mem = []

            for row in readCSV:
                url = row[3]
                url_mem.append(url)

    # download image from url
        x = 0
        for index in url_mem:
            file_name = "image_" + str(x)
            full_path = file_name + '.jpg'
            urllib.request.urlretrieve(url_mem[x], full_path)
            x = x + 1

        return url_mem, x

    # Step 2: ffmpeg assemble images to video
    def ffmpeg(self):
        print("\n========== Start Making Video ==========")
        (ffmpeg.input(
            '/home/justin/Desktop/Jessie/mini_project/*.jpg',
            pattern_type='glob',
            framerate=0.1).output(self.twitterID + '.mp4').run())

        videoName = self.twitterID+'.mp4'

        return videoName


	# Step 3: Google API
    def google_analyze(self):

        print("\n========== Start Google Analyze ==========")

        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.enums.Feature.LABEL_DETECTION]

        with io.open(self.twitterID + '.mp4', 'rb') as movie:
            input_content = movie.read()
        try:
            operation = video_client.annotate_video(
                features=features, input_content=input_content)
            print('\nProcessing video for label annotations:')
            result = operation.result(timeout=90)
        except Exception as e:
            print("Video Intelligence error")
            exit()
        print('\nFinished processing\n')

        # Process video/segment level label annotations
        
        segment_labels = result.annotation_results[0].segment_label_annotations
        GoogleAnalysis = []
        for i, segment_label in enumerate(segment_labels):
            
            print(i)
            print('Video label description: {}'.format(
                segment_label.entity.description))

            GoogleAnalysis.append(segment_label.entity.description) 
              
            for category_entity in segment_label.category_entities:
                print("Label category description: " +
                      category_entity.description)
        return GoogleAnalysis
            

            # for i, segment in enumerate(segment_label.segments):
            #     confidence = segment.confidence
            #     print("The accuracy of the identification in this case is " +
            #           str(confidence) + "\n")

        # analyze(self.name+'.mp4')
    def shotChange(self):
        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.enums.Feature.SHOT_CHANGE_DETECTION]
        operation = video_client.annotate_video('./' + self.twitterID + '.mp4', features=features)
        print('\nProcessing video for shot change annotations:')

        result = operation.result(timeout=90)
        print('\nFinished processing.')

        # first result is retrieved because a single video was processed
        for i, shot in enumerate(result.annotation_results[0].shot_annotations):
            start_time = (shot.start_time_offset.seconds +
                        shot.start_time_offset.nanos / 1e9)
            end_time = (shot.end_time_offset.seconds +
                        shot.end_time_offset.nanos / 1e9)
            print('\tShot {}: {} to {}'.format(i, start_time, end_time))

class mini_project_3():

    def __init__(self):
        client = MongoClient('localhost:27017')
        self.db = client.UserInfo


    def delete(self):
        self.db.Users.delete_many({})
        print ('\nDeletion successful\n')


    def write(self,twitterID,URL,photoNumber,video,GoogleAnalysis):
        self.db.Users.insert_one(
            {
                "UserID": self.userID,
                "TwitterID": twitterID,
                "URL": URL,
                "photoNumber": photoNumber,
                "video": video,
                "GoogleAnalysis": GoogleAnalysis
                
            })
        print ('\n========== Inserted data successfully ==========\n')


    def update(self,twitterID,URL,photoNumber,video,GoogleAnalysis):
        self.db.Users.update_one(
            {"UserID": self.userID},
            {
                "$set": {
                    "TwitterID": twitterID,
                    "URL": URL,
                    "photoNumber": photoNumber,
                    "video": video,
                    "GoogleAnalysis": GoogleAnalysis
                }
            }
        )

    def read(self):
        userinfo = self.db.Users.find()
        print ('\n========== All data from User =========== \n',)
        for data in userinfo:
            print ('\n',data)

    def search(self):
        userinfo = self.db.Users.find({"GoogleAnalysis": self.searchword})
        userlist = []


        for data in userinfo:
            userlist.append(data["UserID"])

        print ('\nUser {} has {}'.format(userlist,self.searchword))

    def test(self):
        userinfo = self.db.Users.find()
        print ('\n========== Number of images per feed =========== \n',)
        for data in userinfo:
            print ('UserID: {} has {} photos'.format(self.userID,data["photoNumber"]))


        print ('\n========== Most popular descriptors =========== \n',)
        

        # self.db.Users.aggregate([
        #     {$group: {_id: "$digit", count: {$sum: 1}}},    // 统计每个数字出现的次数
        #     {$sort: {count: -1}},    // 逆序排列
        #     {$limit: 1}    // 取第1条记录
        # ]);

class sql:
    def __init__(self, host, user, passwd, database, user_id):
        self.db = mysql.connector.connect(
            host = host,
            user = user,
            passwd = passwd,
            database= database
        )
        self.user_id = user_id
        print (self.db)

    def write(self, twitterID, URL, photoNumber, video, GoogleAnalysis):
        mycursor = self.db.cursor()
        self.insertWordTb(GoogleAnalysis)
        sql = "INSERT INTO user (UserID, TwitterID, URL, photoNumber, video, GoogleAnalysis) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (self.user_id, twitterID, self.mergeString(URL), photoNumber, video, self.mergeString(GoogleAnalysis))
        mycursor.execute(sql, val)
        self.db.commit()
        print(mycursor.rowcount, "record inserted.")
    
    def searchword(self, word):
        mycursor = self.db.cursor()
        mycursor.execute("SELECT * FROM user WHERE GoogleAnalysis = \'" + word + "\'")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
    
    def mergeString(self, input_array):
        string = ""
        for s in input_array:
            string = string + s + ";"
        return string
    
    def insertWordTb(self, input_array):
        sql_insert = "INSERT INTO search_table (word, num) VALUES (%s, %s)"
        sql_update = "UPDATE search_table SET num = %s WHERE word = %s"
        merged_array = {}
        for data in input_array:
            if data in merged_array:
                 merged_array[data] += 1
            else:
                merged_array.update({data:1})
        mycursor = self.db.cursor()
        mycursor.execute("SELECT * FROM search_table")
        myresult = mycursor.fetchall()
        for key in merged_array:
            exist = False
            for x in myresult:
                if x[0] == str(key):
                    exist = True
                    break
            val = ()
            if (exist): 
                val = (x[1]+merged_array[key], x[0])
                mycursor.execute(sql_update, val)
            else:
                val = (key, merged_array[key])
                mycursor.execute(sql_insert, val)
            self.db.commit()
            

        
    # def getMostword(self):
    #     mycursor = self.db.cursor()
    #     command = \
    #     "SELECT word , COUNT(*) total " + \
    #         "FROM " + \
    #             "( SELECT DISTINCT GoogleAnalysis " + \
    #                 ", SUBSTRING_INDEX(SUBSTRING_INDEX(line,' ',i+1),' ',-1) word " + \
    #             "FROM user " + \
    #                 ", ints " + \
    #             ") x " + \
    #         "GROUP " + \
    #             "BY word " + \
    #     "HAVING COUNT(*) > 3 " + \
    #     "ORDER " + \
    #     "BY total DESC " + \
    #     ", word; "
    #     mycursor.execute(command)
    #     myresult = mycursor.fetchall()
    #     for x in myresult:
    #         print(x)


    def deleteALL(self):
        mycursor = self.db.cursor()
        sql = "DELETE FROM user"
        mycursor.execute(sql)
        self.db.commit()
        sql = "DELETE FROM search_table"
        mycursor.execute(sql)
        self.db.commit()
        print("all record(s) deleted")
    
    def printAll(self):
        mycursor = self.db.cursor()
        mycursor.execute("SELECT * FROM user")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

    def printAllSearchTb(self):
        mycursor = self.db.cursor()
        mycursor.execute("SELECT * FROM search_table")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

if __name__ == '__main__':
    userData = mini_project_3()
    # m_sql.write("justin", "123", "456", "video123", ["google1", "google2", "google3"])
    # m_sql.deleteALL()
    # m_sql.printAll()
    # m_sql.searchword("google1111")

    # m_sql.insertWordTb(["google1", "google2", "google3"])
    # m_sql.insertWordTb(["google1", "google", "google"])
    # m_sql.printAllSearchTb()

    auto = True
    if(auto):
        userData.userID = "wayne"
        twitterID = "amzjc"
        userData.searchword = "skyscraper"

    else:
        userID = input('Enter userID: ')
        user.twitterID = input('Enter the twitter account:')

    user = mini_project_1(twitterID)
    

    # MiniProject_1:
    URL,photoNumber = user.tweet_api()
    video = user.ffmpeg()
    GoogleAnalysis = user.google_analyze() 
    # user.shotChange() 
    
    # MySQL
    m_sql = sql("localhost", "root", "pev", "user", userData.userID)
    m_sql.write(twitterID,URL,photoNumber,video,GoogleAnalysis)
    m_sql.printAll()
    m_sql.printAllSearchTb()


    # # MiniProject_3:
    # # userData.delete()
    # # userData.write(twitterID,URL,photoNumber,video,GoogleAnalysis)
    # # userData.update(twitterID,URL,video,GoogleAnalysis)
    # # userData.read()
    # # # userData.search()
    # # userData.test()

    
