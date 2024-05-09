from html.parser import HTMLParser


class SimpleHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(SimpleHTMLParser, self).__init__(*args, **kwargs)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr_name, attr_value in attrs:
                if attr_name == "href":
                    self.hrefs.append(attr_value)
                    break
