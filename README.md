# Information Retrieval Group 16

This Project will be focused on the reviews of the Apple IPhone models from the Amazon Store.

## Modules:
### Crawler
The Crawler Module helps us to crawl the data using our API keys to gather data from the Amazon Store on the Reviews of the IPhone Models. In cases of any new data, this will allow us to update the indexer, with the new incremental indexing shown.

### Search
The Search Module presents the user with five queries, the user can choose either of the five queries to be searched. The results and speed of the query will be displayed.


## Installation
Create a Conda Environment, make sure you're using the correct environment

```bash
conda create -n env-name
conda activate env-name
```

Install all the following packages using the command below:

```bash
pip install -r requirements.txt
```

### Flask
To run the flask, head to app.py and run the python file to get the server up.

### Streamlit UI
To run the streamlit UI, open up terminal and run the command below:

```bash
streamlit run Home.py
```

### Docker (Crawling Only)
As of now, the crawling uses implementations of docker for rendering the html page for scraping,
hence, go to this link to download docker: https://www.docker.com/products/docker-desktop/

After installing docker and restarting your computer, open up Windows Powershell and run:

```bash
docker pull scrapinghub/splash
```

Open docker afterwards and click on run, click on optional settings, type 8050 under the port section.
Press run and you're done!