Real Estate Auction Crawler
==============================

What Is This?
-------------
A simple Python crawler used to gather all real estate auction documents from a specific site. <br>
The crawler will find all posted auctions between two set dates. The auction documents are downloaded and filtered (removed) based on keywords. <br>

Should I Use This?
-------------
This is a personal project written for a specific site based in a specific country - not many will find it useful. <br><br>
It is used as an aid in a personal side business. Its purpose is to automate manual clicking/downloading and sorting through hundreds of PDF files. <br>

How To Use This
---------------
Open project with editor of choice. <br>
Manually edit the start (d1) and end (d2) dates in the config file.<br>
Run the following Python command in terminal to install all dependencies:<br>
```
python setup.py
```
Run the following Python command in terminal to start the crawler:<br>
```
python crawler.py
```