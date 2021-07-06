# GMA Network | Script by @Dichill

import requests
import importlib
import os

"""
    | GMA Network API Script by @Dichill |
    + Notes +
    
    Django API Request
    https://dichill-pinoytv.herokuapp.com/api-v1/extract-link/?url={youtube_url/dailymotion}&quality={360/720/1080}

    GMA Network | API Endpoint Analysist by Dichill

    API_URL: https://data.igma.tv/entertainment/
    VIDEO_URL: https://www.gmanetwork.com/entertainment/tv/{show_details}
    IMAGE_URL: https://aphrodite.gmanetwork.com/entertainment/videos/images/6__20210702184916.jpg

    PAGE 1
    https://data.igma.tv/entertainment/listing/shows.gz | All the shows with the ID | Show this as Popular on GMA

    https://data.igma.tv/entertainment/tv/{show_id}/show_details.gz | Shows all the details about that show.


    PAGE 2
    # Show all episodes
    https://data.igma.tv/entertainment/tracker/list_tv_{show_id}_episodes.gz # Returns the length of the episodes.
    https://data.igma.tv/entertainment/listing/tv/{show_id}/episodes/{count}.gz # Returns all the episodes based the list provided.

    # This json's result below can be achieved via PAGE 1-2 | show_details.gz and {count}.gz

    "video" : { 
        "youtube": "{code}",
        "dailymotion": "{code}",
    }

    # Links to episodes via Dailymotion and Youtube
    https://www.youtube.com/watch?v=<video.youtube>
    https://www.dailymotion.com/video/<video.dailymotion>
    
    # PAGE 3
    
    POSTERS_URL = https://aphrodite.gmanetwork.com/entertainment/shows/images/{picture}
    POSTERS_ORIGINAL_URL = https://aphrodite.gmanetwork.com/entertainment/shows/images/original/{picture}
    
"""


class GMATV:
    def __init__(self):
        # Get Current Directory to save data (So we don't waste data usage.)
        self.current_dir = os.getcwd()

        self.dr_count_path = self.current_dir + "/data/"

        # Gets how many Shows are there in GMA | returns a {count}
        self.counts_url = 'https://data.igma.tv/entertainment/tracker/list_tv.gz'

        # Gets the details of each list in a {count} | Reminder that each {count} is a
        # list that has 3 or more shows embedded to it.
        self.details_url = 'https://data.igma.tv/entertainment/listing/tv/index/{}.gz'

        # Lets add the count variable and change it if we can get the data
        self.count_data = None

        # Check if 'count' is already saved to avoid data waste.
        if os.path.exists(self.dr_count_path + 'count_data.dr'):
            dr_count = open(self.dr_count_path + 'count_data.dr', "r")
            data = dr_count.read()
            self.count_data = data
            dr_count.close()
        else:
            # Creates a new file
            dr_count = open(self.dr_count_path + 'count_data.dr', "w")
            dr_count.close()

        # Get the json data of self.counts_url so we don't have to call it again when requesting for one.
        dr_count = open(self.dr_count_path + 'count_data.dr', 'r')
        data = dr_count.read()

        # Make one request to count to avoid data waste.
        self.counts_request = requests.get(self.counts_url)

        if data == "":
            if self.counts_request.status_code == 200:
                count_json = self.counts_request.json()

                # Write data to txt
                self.count_data = open(
                    self.dr_count_path + 'count_data.dr', "w")
                self.count_data.write(count_json['count'])
                self.count_data.close()
        else:
            if self.counts_request.status_code == 200:
                count_json = self.counts_request.json()

                # Check whats inside the dr file.
                self.count_data = open(
                    self.dr_count_path + 'count_data.dr', 'r')
                if self.count_data.read() != count_json['count']:

                    # Close it to avoid Memory Leaks
                    self.count_data.close()

                    # Open it again to make it writeable.
                    self.count_data = open(
                        self.dr_count_path + 'count_data.dr', 'w')
                    self.count_data.write(count_json['count'])
                    self.count_data.close()
        # close dr_count after doing this task.
        dr_count.close()

    def getTVShowCount(self):
        # Open the file first and then return it.
        f = open(self.dr_count_path + 'count_data.dr', 'r')
        return f.read()

    def parseTVShow(self):
        parseShow = importlib.import_module('parse_shows')
        parseShows = parseShow.parseShows()

        return parseShows()

    def getTVShow(self, shows):
        getTVShow = importlib.import_module('parse_shows')
        getTVShows = getTVShow.getShows(shows)

        return getTVShows()
