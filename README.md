## INSTALLATION


> pip install requests pytest pytest-asyncio


## RUNNING

> python __main__.py http://localhost ~/tmpdir/

## CLASSES


### [PageParser](source/page_parser/page_parser.py)

Made for getting links from page content

*Here we can fetch more links getting form tags*


### [PageCacher](source/page_cacher/page_cacher.py)

Keeps downloaded pages with unique URLs

*We can use some key-value facility, may be it is possible to use filesystem to store content*


### [RequestMaker](source/request_maker/request_maker.py)

Downloads pages, checks content type

*TODO: Add sessions, add custom request headers, act more human-like. Use referrers, generate real track*

### [Crawler](source/crawler.py)

Main class.
Uses methods of requester, parser and cacher to get work done.
Also has method "dump downloaded pages".
Logging goes here.

*TODO: Spread requests to other hosts, url_to_request queue may be some MQ server*


## TODO:

Handle form tags

Add retries

Add query args sorting

Dump after url is fetched, remove content from memory

More logging

CLI interface using argparse

Input arguments validation

Use http sessions

Separate session for every worker

Add custom request headers

Add referrer to every query

Random sleep interval

Make it using browser (GreaseMonkey etc)
