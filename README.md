CLASSES


 - PageParser

Made for getting links from page content


 - PageCacher

Keeps downloaded pages with unique URLs


 - RequestMaker

Downloads pages, checks content type


 - Crawler

Main class.
Uses methods of requester, parser and cacher to get work done.
Also has method "dump downloaded pages".
Logging goes here.



TODO:

Handle form tags

Add retries

Add query args sorting

Dump after url is fetched, remove content from memory

More logging

CLI interface using argparse

Use http lib with session support

Separate session for every worker

Add custom request headers

Add referrer to every query

Random sleep interval

Make it using browser (GreaseMonkey etc)