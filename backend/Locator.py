from os import environ
import requests
import json

class Locator:
    def detect_language_from_ip(self, request):
        ip_info = self.get_ip_info(request)
        language = ip_info["data"]["languages"].split(",")[0]
        return language
    
    def get_ip_info(self, request):
        try:
            ip = request.environ["HTTP_X_REAL_IP"]
            token = environ["GEO_LOC_TOKEN"]
            requests.get("https://timezoneapi.io/api/ip/?ip=%s&token=%s" % (ip, token))
            return json.loads(requests.text)
        except:
            return "en-US"


