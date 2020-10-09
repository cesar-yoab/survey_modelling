# Data generation methodology
We generated stratified samples with provinces used as stratums.
The assumption of the existence of a list of addresses that are used as the sampling frame, 
is made to simplfy the data generation process.
The design followed is Stratified Simple Random Sampling using simple random sampling without replacement(SRSWOR).
The overall sample size is set to n = 10,000 with population
size N = 38,005,238, the current estimate for Canadian population as of 
Q3 2020 ([source](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)).

## Data Generation Procedure.
Populations for each province in Canada are scraped from this [website](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901), data is written to a .txt file. Then to help model the COVID-19 related questions we gather some data from
10 youtube videos in which members of the Liberal party address COVID-19 related issues. 
To gather this information we call the YouTube data API. You will
need a key to use this script, documentation on how to get such a key can be found [here](https://developers.google.com/youtube/v3/docs/?apix=true), 
more documentation on the API can be found [here](https://developers.google.com/youtube/v3/docs/videos/list).
To use this script you will need to have a working Python 3.8+ installation, we also recommend
setting up a virtual environemnt which can be done with the command
```bash
python -m venv yourenvname
```
upgrade pip and download the required libraries 
with the command:

```bash
pip install -r requirements.txt
```

then call the python script with a path to a directory where to place the .txt and .json files, 
your api key is also required. For example:

```bash
python data_gen.py --dir='/your/path/to/directory' --api-key='YOUR_API_KEY'
```

you can also do
```bash
python data_gen.py --api-key='YOUR_API_KEY'
```
if you want the .txt and .json files in your current directory.
For more information on how to use this script you can call

```bash
python data_gen.py --help
```
Once this is done ith this data you can generate the simulation data for the survey. We recommend installing
[rstudio](https://rstudio.com/), or using [rstudio cloud](https://rstudio.cloud/) and using it for the following steps. Open modeling_script.R in rstudio or upload to rstudio cloud together with the .json and .txt file and
run the script. To do this select all the code (Ctr + a) and run the script (Ctr+Enter). A .csv file will be 
generated.

## List of video links
* [Trudeau promises more support for local public health units in COVID-19 hot spots](https://www.youtube.com/watch?v=i-aX4NJR9jU&ab_channel=CBCNews)
* [Trudeau announces measures to help businesses survive lockdowns](https://www.youtube.com/watch?v=x0baobXKkIM&ab_channel=CBCNews)
* [Canada's COVID-19 messaging isn't reaching young people: expert](https://www.youtube.com/watch?v=rQgQJ2kYnqo&t=36s&ab_channel=CBCNews)
* [Liberals, NDP reach deal on sick leave, avoiding immediate election](https://www.youtube.com/watch?v=n_O0uPgdUDM&ab_channel=CBCNews)
* [CERB expires this weekend](https://www.youtube.com/watch?v=r2PP76dihcs&ab_channel=CBCNews)
* [COVID-19 update: Trudeau addresses Canadians](https://www.youtube.com/watch?v=FSOZrt3tTho&ab_channel=CBCNews)
* [Trudeau tested negative for COVID-19 last month](https://www.youtube.com/watch?v=BsSL8Oh63BI&ab_channel=CBCNews)
* [Thanksgiving and COVID: advice by region](https://www.youtube.com/watch?v=5j4nezuvfpc&ab_channel=CBCNews)
* [Justin Trudeau addresses United Nations says that COVID-19 has set back gender equality worldwide](https://www.youtube.com/watch?v=eMbfZPqU3xc&ab_channel=CTVNews)
* [Trudeau issues a stark warning to the United Nations: 'The system is broken, the world is in crisis'](https://www.youtube.com/watch?v=yR2XIOAoiDs&ab_channel=CTVNews)