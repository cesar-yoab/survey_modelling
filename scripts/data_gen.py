import requests
from bs4 import BeautifulSoup
import os
import json
import click
import time


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


def write_profiles(data, filename, path):
    """ Write json data to json file."""

    # Full path for new json file
    filepath = os.path.join(path, filename)

    with open(filepath, 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_profiles(api_url, params):
    """Call profiles API 2 times to create 10,000 fake
    samples."""
    api_call = api_url + '?'

    for k, v in params.items():
        api_call += k + '=' + str(v) + '&'

    resp = requests.get(api_call.rstrip())

    if resp.status_code == 200:
        return resp.json()['results']

    print("Call to API returned status code: ", resp.status_code)
    return []


@click.command()
@click.option('--dir', default=os.getcwd(),
              type=click.Path(exists=True),
              help='Full path of directory to store data.')
@click.option('--no-profiles', is_flag=True, help="Not include profiles file.")
@click.option('--no-provinces', is_flag=True, help="Not include provinces file.")
def main(dir, no_profiles, no_provinces):
    """Script to generate data for modelling survey responses.
        Script generates a json file with 10,000 randomly generated fake profiles,
        and a txt file with Canadas provinces and corresponding populations.\n
        Note: You cannot use both the --no-profiles and --no-provinces flags simultaneously."""
    if no_profiles and no_provinces:
        ctx = click.get_current_context()
        ctx.fail("You cannot select both flags.")
        return

    # Code to generate provinces file
    # Scrapes website
    if not no_provinces:
        url = 'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901'
        page = requests.get(url)
        if page.status_code == 200:
            data = parse_with_bs4(page)

            write_data(data, 'provinces.txt', os.getcwd())

    # Code to generate fake profile list
    if not no_profiles:
        api_url = 'https://randomuser.me/api/'
        # Ask for 5000 results each with Canadian nationality
        params = {'results': 5000, 'nat': 'ca',
                  'exc': 'login,registered,picture'}

        # The API only allows 5000 samples per call, so we make two
        # and merge them into a single dictionary
        p1 = get_profiles(api_url, params)
        time.sleep(2)
        p2 = get_profiles(api_url, params)

        profiles = {'results': p1 + p2}

        write_profiles(profiles, 'profiles.json', os.getcwd())


if __name__ == "__main__":
    main()
