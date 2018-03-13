import requests 
import json
import time
from itertools import chain


class StackApi(object):
    def __init__(self, site="stackoverflow", version="2.2", **kwargs):
        """
        :param site:(required) A valid "api_site_parameter"
        default sould be stackoverflow
        :param version:(opt) the version of the API by default it is 2.2
        :param max_pages: the maximun number of pages to retrive
        default is 100
        :param page_size: the number of elements perpage
        default is 100
        :param key: a api key
        """
        if not site:
            raise ValueError("Please give a site name!!!")
 
        self.proxy = kwargs.get('proxy', None)
        self.max_pages = kwargs.get('max_pages', 100)
        self.page_size = kwargs.get('page_size', 100)
        self.key = kwargs.get('key', None)
        self.access_token = kwargs.get('access_token', None)
        self._endpoint = None
        self.version = version
        self._base_url = 'https://api.stackexchange.com/{}/'.format(version)
        self.site = site
        self._api_key = None
        self._previous_call = None
        self._filter = None

    def fetch(self, endpoint=None, page=1, key=None, filter='default', **kwargs):
        """
        once need "comments_count of anster", need filter to be "!9Z(-x)63B"
        """
        if not endpoint:
            raise ValueError('No end point provided')

        self._endpoint = endpoint

        self._filter = filter

        params = {
                "pagesize": self.page_size,
                "page": page,
                "filter": self._filter,
                "site": self.site
                }

        #this block translate time fom human read type to Unix Timestamp
        date_time_keys = ['fromdate', 'todate', 'since', 'min', 'max']

        for k in date_time_keys:
            if k in kwargs and kwargs[k] != None:
                kwargs[k] = int(time.mktime(time.strptime(kwargs[k], '%Y-%m-%d %H:%M:%S')))

        params.update(kwargs)

        if self._api_key:
            params["site"] = self._api_key
        
        data = []
        cur_page = 1
        backoff = 0
        total = 0

        while cur_page <= self.max_pages:

            cur_page += 1

            #update url according to No. of page 
            base_url = self._base_url + endpoint

            try:
                response = requests.get(base_url, params=params, proxies=self.proxy)
            except requests.exceptions.ConnectionError as e:
                raise StackAPIError(self._previous_call, str(e), str(e), str(e))

            self._previous_call = response.url

            try:
                response.endcoding = 'utf-8'
                response = response.json()
            except ValueError as e:
                raise StackAPIError(self._previous_call, str(e), str(e), str(e))

            if key:
                data.append(response[key])
            else:
                data.append(response)

            if len(data) < 1:
                break
               
            #sleep backoff seconds in case timing issues 
            backoff = 0
            if "backoff" in response:
                backoff = int(response["backoff"])
                sleep(backoff)
            
            #check if there is more page, if not stop the loop
            if "has_more" in response and response["has_more"] is True:
                params["page"] += 1
            else:
                break
        
        r = []
        for d in data:
            r.extend(d["items"])
        #total No. of returned items
        total = len(r)

        result = {
                "backoff": backoff,
                "has_more": data[-1]["has_more"],
                "page": params["page"],
                "quota_max": data[-1]["quota_max"],
                "total": total,
                "items": list(chain(r))
                }

        return result

    def calAve(self, data=None, value=None):
        """
        :param data: (Required) Data is the list of Items
        questions key is answer_count to count 
        """
        return float(sum(map(lambda x: x[value], data)))/len(data)

    def __sort___(self, data=None, value=None, reverse=True):
        """
        :param data: (required) data items list to be sorted
        :param value: (required) the data items's element to be sorted
        input should be data["items"] aray, value is the sorted target, reverse default is true
        """

        data.sort(key = lambda X: x[value], reverse=reverse)

    def calAnswers(self, answers=None):
        """
        :param: (required) answers, must be a list (items of answers)
        response should be a dictionary{} which contains basic information of 
        return type: a list, 1st value is a value of "total_accepted_answers", 
                             2nd value is accept answers averange score
        """
        #sort the result by "scores" to get top 10 answers's comment_count
        answers.sort(key = lambda x: x["score"], reverse=True)
        top_ten = {str(answers[x]["answer_id"]): answers[x]["comment_count"] for x in range(10)}

        #filter the "is_accepted = Ture" answers only
        accepted = filter(lambda x: x["is_accepted"], answers)
    
        #total_accepted_answers
        total = len(accepted)
        
        #accepted_answers_averange_score
        ave_score = float(sum(map(lambda x: x["score"], accepted)))/total

        result = {
                "total_accepted_answers": total,
                "accepted_answers_averange_score": ave_score,
                "top_ten_answers_comment_count": top_ten
                }

        return result
