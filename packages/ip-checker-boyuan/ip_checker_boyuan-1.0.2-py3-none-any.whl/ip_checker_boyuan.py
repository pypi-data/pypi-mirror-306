# ip_checker.py

from html.parser import HTMLParser
import urllib.request

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ip_address = None

    def handle_data(self, data):
        if "Current IP Address:" in data:
            self.ip_address = data.split("Current IP Address:")[1].strip()

def get_ip_address():
    myparser = MyHTMLParser()
    with urllib.request.urlopen('http://checkip.dyndns.org/') as response:
        html = str(response.read())
    myparser.feed(html)
    if myparser.ip_address:
        print("IP Address:", myparser.ip_address)

if __name__ == "__main__":
    get_ip_address()
