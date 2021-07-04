# GMA Network | Script by @Dichill

from tqdm import tqdm
import aiohttp
import importlib
import time
import asyncio
import json
import os

"""
    Documentation for using GMA API PYTHON | Script by Dichill
"""

# If you're having problems with importing the module you can use importlib.
# very useful module if the problem really persist.
api = importlib.import_module('gma')

# Calling our class which is GMATV so we can access its child.
gma = api.GMATV()

# Images
thumbnails = []
tv_shows_name = []
tv_shows_id = []
results = []

POSTERS_URL = "https://aphrodite.gmanetwork.com/entertainment/shows/images/{}"
POSTERS_ORIGINAL_URL = "https://aphrodite.gmanetwork.com/entertainment/shows/images/original/{}"
NO_POSTER_URL = "https://dichill-pinoytv.herokuapp.com/static/img/no_thumbnail.png"

poster_links = []


def get_tasks(session, image_url):
    tasks = []
    for c in image_url:
        tasks.append(asyncio.create_task(
            session.get(c, ssl=False)))
    return tasks


def is_url_image(session):
    try:
        if session.status == 200:
            return True
        return False
    except:
        return False


def getShows(shows):
    for x in range(0, len(shows)):
        data = shows[x]['data']
        for i in range(0, len(data)):
            thumbnails.append(data[i]['image_name'])
            tv_shows_name.append(data[i]['show_title'])
            tv_shows_id.append(data[i]['id'])

    start = time.time()

    async def check_poster():
        async with aiohttp.ClientSession() as session:
            print("[Debug-Busy] Seperating Images... It might take a while.")
            print("[Debug-Info] Links to Seperate: " + str(len(thumbnails)))

            for x in tqdm(thumbnails):
                poster = [POSTERS_URL.format(x)]
                tasks = get_tasks(session, poster)
                responses = await asyncio.gather(*tasks)
                if x != "":
                    for response in responses:
                        if is_url_image(response) == True:
                            poster_links.append(POSTERS_URL.format(x))
                        elif is_url_image(response) == False:
                            poster_links.append(POSTERS_ORIGINAL_URL.format(x))
                else:
                    poster_links.append(NO_POSTER_URL)

        for i in range(0, len(tv_shows_id)):
            results.append(
                {"id": tv_shows_id[i], "name": tv_shows_name[i], "image": poster_links[i]})

    data = {
        "data": results, "total_shows": len(thumbnails)
    }

    if os.path.exists(gma.dr_count_path + 'json/results.json'):
        f = open(gma.dr_count_path + 'json/results.json')
        json_data = json.load(f)

        with open(gma.dr_count_path + 'json/results.json') as fp:
            data = json.load(fp)
            if len(thumbnails) != len(json_data['data']):
                print("[Debug-Info] Server Links: " + str(len(thumbnails)
                                                          ) + " | Current Links: " + str(len(json_data['data'])))
                print(
                    "[Debug-Warning] Links != Results")
                print("[Debug-Warning] Updating results.json")
                asyncio.set_event_loop_policy(
                    asyncio.WindowsSelectorEventLoopPolicy())
                asyncio.run(check_poster())
                with open(gma.dr_count_path + 'json/results.json', 'w') as fp:
                    json.dump(data, fp, sort_keys=True, indent=4)
                print("[Debug-Finished] Finished updating results.json")
                f.close()
                return data
            else:
                print(
                    "[Debug-Finished] results.json has no updates.")
                f.close()
                return json_data

    elif os.path.exists(gma.dr_count_path + 'json/results.json') == False:
        print("[Debug-Info] results.json is missing, creating file.")

        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(check_poster())
        with open(gma.dr_count_path + 'json/results.json', 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)
            print("[Debug-Finished] results.json created.")

    end = time.time()

    total_time = end - start

    print("[Debug-Finished] Image Seperated: " + str(len(poster_links)) +
          " Links | Total time to seperate: " + str(total_time) + "s" + "")

    TVshow_total_time = open(
        gma.dr_count_path + 'logs/show_total_time.logs', 'r').read()

    estimated_time = len(poster_links) / \
        int(gma.getTVShowCount()) * float(TVshow_total_time)

    print("[Debug-Log] TV Show Count Time: " + str(TVshow_total_time) + "s | Seperation Time: " +
          str(total_time) + "s | Estimated Time to finish: " + str(estimated_time) + "s")

    print("[Debug-Info] Please do contact me, or issue a code that can minimize the total time spent.")

    print("[Debug-Finished] Seperation of Images Completed.")

    return data


# OLD SAMPLE CODES
# Create tvshowsquery.dr | (For Autocompletion when searching for a teleserye)
# with open("data/tvshowsquery.dr", 'w') as output:
#     for row in tv_shows_name:
#         output.write(str(row) + '\n')

# print("[Testing] First ID: " + api.getShows()[0]['data'][0]['id'])
# api.getShows()[0] -> 0 to 27
