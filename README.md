# Information Retrieval Group 16

This Project will be focused on the reviews of the Apple IPhone models from the Amazon Store.

## Modules:
### Crawler
The Crawler Module helps us to crawl the data using our API keys to gather data from the Amazon Store on the Reviews of the IPhone Models. In cases of any new data, this will allow us to update the indexer, with the new incremental indexing shown.

### Search
The Search Module presents the user with five queries, the user can choose either of the five queries to be searched. The results and speed of the query will be displayed.


## Setting up of Environment
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