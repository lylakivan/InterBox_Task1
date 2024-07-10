import aiohttp
import asyncio
from prettytable import PrettyTable


class CountryInfo:
    def __init__(self, api_url: str):
        """
        Initializes the CountryInfo class with the provided API URL.

        :param api_url: The URL of the API to fetch country data from.
        """
        self.api_url = api_url

    async def fetch_data(self):
        """
        Fetches data from the API.

        :return: A list of dictionaries containing country data if the request is successful, None otherwise.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        print(f"Error: Unable to fetch data, HTTP status code: {response.status}")
                        return None
            except aiohttp.ClientError as e:
                print(f"Error: {e}")
                return None

    def display_table(self, data):
        """
        Displays the fetched country data in a table format.

        :param data: A list of dictionaries containing country data.
        """
        table = PrettyTable()
        table.field_names = ["Country", "Capital", "Flag URL"]

        for country in data:
            country_name = country.get("name", {}).get("common", "N/A")
            capital = country.get("capital", ["N/A"])[0]
            flag_url = country.get("flags", {}).get("png", "N/A")
            table.add_row([country_name, capital, flag_url])

        print(table)

    async def get_country_info(self):
        """
        Fetches and displays country information.
        """
        data = await self.fetch_data()
        if data:
            self.display_table(data)


if __name__ == "__main__":
    api_url = "https://restcountries.com/v3.1/all"
    country_info = CountryInfo(api_url)

    asyncio.run(country_info.get_country_info())
