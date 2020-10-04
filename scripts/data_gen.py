import requests
from bs4 import BeautifulSoup
import os
import click
import json


# List of videos to get information
vids = ['SIPCAhS0xjw', 'rQgQJ2kYnqo',
        'FSOZrt3tTho', 'x0baobXKkIM', 'UVuk-qGQb2A']


def parse_with_bs4(page):
    # Parse with bs4
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the table tags, which contain information
    try:
        table = soup.findAll('table', {'class': 'pub-table'})[0]

        # Extract data from the table
        data = {  # We use dictionary comprehension to quickly extract data
            row.th.get_text(strip=True):  # This selects the name of the row, province name
            # This extracts all the values in the row
            [val.text for val in row('td')]
            for row in table.findAll('tr')  # Iterating over each row
        }

        # Clean the data contained in the table
        # Remove '(map)' link from province name
        # Remove instances that contain empty lists as values and
        # Only select the last item in the list of population numbers
        # this corresponds to data of Q4
        data_clean = {k.replace("(map)", ""): v[-1].replace(",", "")
                      for k, v in data.items() if len(v) != 0}

        return data_clean

    except IndexError:
        # This happens on an error with requested html
        parse_with_bs4(requests.get(
            'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901'))


def write_data(data, filename, path):
    """ Write data to a selected filename."""

    # Full path of file to be created
    filepath = os.path.join(path, filename)

    # Write data to file with ':' as delimiter
    with open(filepath, 'w+') as f:
        for k, v in data.items():
            f.write(k + ':' + v + '\n')


def call_api(key):
    """Generates query for the API and calls the API"""
    url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='

    for v in vids:
        url += v + ','

    url = url.rstrip() + "&key=" + key

    # Call the API
    resp = requests.get(url)

    if resp.status_code == 200:
        return resp.json()

    return {}


def write_response(data, filename, path):
    """ Write json data to json file."""

    # Full path for new json file
    filepath = os.path.join(path, filename)

    with open(filepath, 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@click.command()
@click.option('--dir', default=os.getcwd(),
              type=click.Path(exists=True),
              help='Full path of directory to store data.')
@click.option('--api-key', help="Your unique YouTube API key.", default=False)
@click.option('--no-provinces', is_flag=True, help="Not include provinces file.")
def main(dir, api_key, no_provinces):
    """Script to crawl current province census and gather data for modelling from the YouTube API.
    A key is required."""
    if not api_key:
        ctx = click.get_current_context()
        ctx.fail("You need to include your API key to call the YouTube API")
        return

    # Code to generate provinces file
    # Scrapes website
    if not no_provinces:
        url = 'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901'
        page = requests.get(url)
        if page.status_code == 200:
            data = parse_with_bs4(page)

            write_data(data, 'provinces.txt', os.getcwd())

    data = call_api(api_key)
    write_response(data, "yt-response.json", dir)


if __name__ == "__main__":
    main()
