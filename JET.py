import requests
from tabulate import tabulate


def call_api(postcode):

    # Calling api with formatted string
    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)


    # response object could be "None" or calling Json() could fail, so we try and serialise the response. 
    try:
        data = response.json()

        # if there is a successful response (HTTP code 200), we can then check to make sure the server hasn't sent back empty data (which is the case with invalid postcode input)
        # This can be checked by looking at the resultCount value withint he servers response
        if response.status_code == 200:
            if data['metaData']['resultCount'] > 0:
                # if we have data to return, we return the first 10 restaurants
                return data["restaurants"][:10]
            else:
                # if there is not restaurant returned, it means we entered the postcode incorrectly or there is nothing being served in this area. 
                print("There are no Restaurants currently serving within this postcode.")
                return
        else:
            # If the response was able to serialise but the HTTP status code indicates an error, then we need to handle it
            # API endpoint/Server responds with Json object for some erroneous status' such as 401, 429, 500.
            # If it does, this contains an error code and description we will try to access and print.
            print(f"Error code: {data["errors"]["errorCode"]}\nReason: {data["errors"]["description"]}")
    except:
        # If the json serialisation fails, which can happen if there is, for example, a 402 error with no content, 
        # then we can return the error code and reason using the requests library
        print(f"{response.status_code} ERROR .\nReason: {response.reason}")

    


def format_response_data(data):

    # store each row of the table in a list as a list of lists
    tableData = []
    for restaurant in data:
        # Each restaurant can have multiple cuisines, so we store these in another list
        cuisineList = []
        for cuisine in restaurant["cuisines"]:
            cuisineList.append(cuisine["name"])

        # Once we have all the cusines of the corresponding restaurant, 
        # then we can format each row of the table so that each line of the address and each type of cuisine is clearly seen on a new line
        tableData.append([
                restaurant["name"],
                "\n".join(cuisineList),
                restaurant["rating"]["starRating"],
                f"{restaurant["address"]["firstLine"]}\n{restaurant["address"]["city"]}\n{restaurant["address"]["postalCode"]}"
                ])

    # return the table data for each row
    return tableData

def print_table(tableData):
    # Requested data points to display. These will be the headings of the table
    headers = ["Restaurant name", "Cuisines", "rating", "Address"]
    print(tabulate(tableData, headers, tablefmt="grid", numalign="center", stralign="center"))


def main():
    # if the wrong postcode is entered, then data is still returned by the API but its empty data, so we need to handle that
    # we do that by checking if data is no null
    data = call_api("UB56LH")
    if data:
        print_table(format_response_data(data))

    

if __name__ == "__main__":
    main()

