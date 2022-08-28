from os import environ
import requests
import json

class Locator:
    def detect_language_request(self, request):
        language = self.get_language(request)
        return language
    
    def get_language(self, request):
        try:
            ip = request.environ["HTTP_X_REAL_IP"]
            token = environ["GEO_LOC_TOKEN"]
            requests.get("https://timezoneapi.io/api/ip/?ip=%s&token=%s" % (ip, token))
            request = json.loads(requests.text)
            print(request)
            return request["data"]["languages"].split(",")[0]
        except:
            return "en-US"


