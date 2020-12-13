# SI507 Final Project
This is a project allowing you to crawl and plot the reports on [GVA](https://www.gunviolencearchive.org/reports).
## Requirements
1. Python
You need a python environment to run the code. The development environment is `Python 3.8.6 64-bit`, but you don't necessarily need to keep the exact same version.
2. Packages
All the necessary packages are saved in `requirements.txt`. You can simply run `pip install -r requirements.txt` to install the required packages. However, note that if you are using some old version of Python, then some packages need to be manually installed.
3. **API Key**
We're using [MapBox](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/) and [MapQuest](https://developer.mapquest.com/) APIs, so you have to provide your own API key. They're both free.
You should create a `secrets.py` at the root directory, the content should be as follow:
```
mapquest_api_key = "${YOUR_MAPQUEST_KEY}"
mapbox_access_token = "${YOUR_MAPBOX_KEY}"
```
4. Proxy
The [GVA](https://www.gunviolencearchive.org/reports) is protected to visits from US only. So if you're running the program in other area, please use a valid proxy to access. 
First you should set a valid Proxy, then change `requests.get` to
```
requests.get(..., proxies=YOUR_PROXY)
```

## How to Run
Simply go to the code directory and run `python main.py`. Then you can follow the instructions within the code. 

At the start of the program, you will see a list of available reports on GVA, then you will be asked to select one specific report.
After selecting a report, you will see the crawled records from the report. The program will ask you to input a state to select the records happened in the state. You will see the selected records and you can choose whether to plot.
We offer both command line interaction and a plot map to show the cases. If you choose to plot, then the program will automatically open a website for you, containing a map of state with the dots representing cases.