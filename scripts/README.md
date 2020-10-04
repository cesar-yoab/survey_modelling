# Data generation methodology
We generated stratified samples with provinces used as stratums.
The assumption of the existence of a list of addresses that are used as the sampling frame, 
is made to simplfy the data generation process.
The design followed is Stratified Simple Random Sampling (SRSWOR).
The overall sample size is set to n = 10,000 with overall stratum population
assummed to be N = 38,005,238 the current population Canadian population estimate as of
Q3 2020 ([source](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)).

## Data Generation Procedure.
First we will need the current populations for each province in Canada to do so we will scrape this [website](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)
and write the collected data to a .txt file. Then to help model the COVID-19 related questions we gather some data from
5 youtube videos in which the Prime Minister as well as Ontario's Premier address the Canadian population on the COVID-19 
pandemic. The oldest video is from Sep 23. To gather this information we call the YouTube data API. You will
need a key to use this script, documentation on how to get such a key can be found [here](https://developers.google.com/youtube/v3/docs/?apix=true), more documentation on the API can be found [here](https://developers.google.com/youtube/v3/docs/videos/list). Moreover, you will need to have a working Python 3.8+ installation and download the required libraries 
with the command:

```bash
pip install -r requirements.txt
```

then call the python script with a path to create the .txt and .json files, and your api key. For example:

```bash
python data_gen.py --dir='/your/path/to/directory' --api-key='YOUR_API_KEY'
```

for more information on how to use this script you can call

```bash
python data_gen.py --help
```

Now with this data we can start generatig the actual simulation data for the survey. We recommend installing
[rstudio](https://rstudio.com/), or using [rstudio cloud](https://rstudio.cloud/) and using it for the following steps. Open modeling_script.R in rstudio or upload to rstudio cloud. 