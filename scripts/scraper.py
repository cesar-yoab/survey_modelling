import requests
from bs4 import BeautifulSoup
import os


def parse_with_bs4(page):
    # Parse with bs4
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the table tags, which contain information
    try:
        table = soup.findAll('table', {'class': 'pub-table'})[0]

    except IndexError:
        # This happens on an error with requested html
        main()

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
    data_clean = {k.replace("(map)", ""): v[-1]
                  for k, v in data.items() if len(v) != 0}

    return data_clean


def write_data(data, filename, path):
    """ Write data to a selected filename."""

    # Full path of file to be created
    filepath = os.path.join(path, filename)

    # Write data to file with ':' as delimiter
    with open(filepath, 'w+') as f:
        for k, v in data.items():
            f.write(k + ':' + v + '\n')


def main():
    url = 'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901'
    page = requests.get(url)

    if page.status_code == 200:
        data = parse_with_bs4(page)

        write_data(data, 'provinces.txt', os.getcwd())


if __name__ == "__main__":
    main()
