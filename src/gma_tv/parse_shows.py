# GMA Network | Script by @Dichill

"""
    | GMA Network API Script by @Dichill |
    + Features +
    - Auto updates tv_shows.json if GMA added a new show.
    - Uses less data to save data.
    - Asnychronous Task, fast API request in < 1.
    - Gets data from actual GMA Network APIs (Check gma.py for further more instructions)
"""

from tqdm import tqdm
import importlib
import asyncio
import time
import aiohttp
import json
import os


# If you're having problems with importing the module you can use importlib.
# very useful module if the problem really persist.
api = importlib.import_module('gma')

# Calling our class which is GMATV so we can access its child.
gma = api.GMATV()

tv_count = gma.getTVShowCount()

count = []
results = []


def get_tasks(session):
    tasks = []
    print("[Debug-Busy] Creating Task ./.")
    for c in count:
        tasks.append(asyncio.create_task(
            session.get(gma.details_url.format(c), ssl=False)))
    print('[Debug-Finished] Task done, gathering data ./.')
    return tasks


def parseShows():
    print("[Debug-Starting] Starting Proccess")

    start = time.time()

    for x in range(1, int(tv_count) + 1):
        count.append(str(x))

    async def get_data():
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks(session)
            responses = await asyncio.gather(*tasks)
            for response in tqdm(responses):
                results.append(await response.json())

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_data())

    if os.path.exists(gma.dr_count_path + 'json/tv_shows.json'):
        with open(gma.dr_count_path + 'json/tv_shows.json') as fp:
            data = json.load(fp)

            print("[Debug-Verification] TV Count: " + tv_count +
                  " | Called Count: " + str(len(data)))

            if int(tv_count) != len(data):
                print(
                    "[Debug-Warning] TV Count != Current Count")
                print("[Debug-Warning] Updating tv_shows.json")
                with open(gma.dr_count_path + 'json/tv_shows.json', 'w') as fp:
                    json.dump(results, fp, sort_keys=True, indent=4)
                print("[Debug-Finished] Finished updating tv_shows.json")
            else:
                print(
                    "[Debug-Finished] tv_shows.json has no updates.")
    elif os.path.exists(gma.dr_count_path + 'json/tv_shows.json') == False:
        print("[Debug-Info] tv_shows.json is missing, creating file.")
        with open(gma.dr_count_path + 'json/tv_shows.json', 'w') as fp:
            json.dump(results, fp, sort_keys=True, indent=4)
            print("[Debug-Finished] tv_shows.json created.")

    end = time.time()
    total_time = end - start

    with open(gma.dr_count_path + 'logs/show_total_time.logs', 'w') as tm:
        tm.write(str(total_time))

    print("[Debug-Finished] Parsed: " + tv_count +
          " Links | Total time spent to parse: " + str(total_time) + "s" + "")

    return results
