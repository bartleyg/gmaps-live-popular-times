import requests
import ujson as json


class LivePop(object):
    """ Google Maps Live Popular Times for places we have a pre-recorded magic pb parameter """
    
    URL = 'https://www.google.com/maps/preview/entity'
    USER_AGENT = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
                            "AppleWebKit/604.1.38 (KHTML, like Gecko) "
                            "Version/11.0 Safari/604.1.38"}
    
    def __init__(self, pb_param, lang_param='en', user_agent=USER_AGENT):
        """
        Initialize default values and parameters
            pb_param = string value for 'pb' for the particular place from
                       previously recorded requests to google maps in the browser
            lang_param = language in 2 character abbreviation
            user_agent = the agent we tell Google Maps we are
        """
        self.pb_param = pb_param
        self.lang_param = lang_param
        self.user_agent = user_agent

        # values that most places will populate
        self.currentHour = None
        self.currentDay = None
        self.poptimesWeek = None

        # values that populate depending on available data
        self.livePop = None
        self.liveDesc = None
        self.usualDesc = None

        # helpful status from our request for data from the place
        self.status = None

    def get_live_data(self):
        """ Send the request to Google Maps and parse the data """

        # parameters to pass to google maps preview entity
        params_url = {
            'authuser': 0,
            'hl': self.lang_param,
            'pb': self.pb_param
        }

        # send request to google maps preview entity with proper parameters
        r = requests.get(LivePop.URL, params=params_url, headers=self.user_agent)

        # drop first and last part of response to get data formatted for json parsing
        resp = r.text[5:-1]
        
        try:
            data = json.loads(resp)

            # where Google Popular Times data resides. this will break if it moves.
            poptimesData = data[0][1][0][14][84]

            self.poptimesWeek = poptimesData[0] # week data: [day, [hour, popularity 0-100]
            self.currentDay = poptimesData[1] # 1-7 (1 = Monday)
            # poptimesdata[2] = None
            # poptimesdata[3] = 1
            self.currentHour = poptimesData[4] # 13 = 1-2PM
            # poptimesdata[5] = ['12a', '3a', '6a', '9a', '12p', '3p', '6p', '9p']

        except ValueError:
            print("Error getting popular times data. Google sent bad response.")
            print(r.text)
            self.status = "Error: Google may have blocked and requested captcha.\n" + r.text
            return self
        except (TypeError, IndexError):
            print("Error getting popular times data")
            self.status = "Error getting popular times data"
            return self

        # place has live data
        if len(poptimesData) == 8:
            self.liveDesc = poptimesData[6] # busy description ie: 'Not too busy'
            liveData = poptimesData[7] # [currentHour, livePopularity] ie: [9, 39]
            self.livePop = liveData[1]      # live popularity 0-100+ (can go above 100)
            self.status = "Place has live popularity data"
        
        # place has no live popularity data
        elif len(poptimesData) == 7:
            self.usualDesc = poptimesData[6] # 'Now: Usually a little busy'
            self.status = "Place has usual data but no live popularity data"
        
        # place is not open. no live popularity data. no usual busyness data.
        elif len(poptimesData) == 6:
            self.status = "Place not open. No live or usual data."

        # return LivePopularTimes class object
        return self


    def historical_popular_value(self):
        """
        Get the historical popular times numerical value from stored results.
        This assumes getLivePopularTimes() is called recently
            and value will be for the current hour.
        Value returned is in range 0-100.
        """

        if self.poptimesWeek is not None and \
                self.currentDay is not None and \
                self.currentHour is not None:
            # hour index of array doesn't start from 0.
            # get the first hour of current day for indexing
            startHour = self.poptimesWeek[self.currentDay][1][0][0]

            # get the historical popularity value for current hour
            historicalPop = self.poptimesWeek[self.currentDay][1][self.currentHour-startHour][1]

            return historicalPop
        else:
            return None
