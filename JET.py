import requests
from tabulate import tabulate

def call_api(postcode):
    """Calling/Consuming the API and checks to see that the response received was successful. If not, an error message is displayed and the program ends."""

    # Format endpoint string with postcode arguement and create custom header with user agent information so that we can bypass "403 forbidden error"
    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    # make a call to the API
    response = requests.get(url, headers=headers)

    # If block handle successful calls to the API, else block handles errors.
    if response.status_code == 200:
        # Serialise to json after ensuring a successful call
        data = response.json()
        # Server can still respond with a "200" code if given an invalid postcode by returning an empty JSON object as a "failed" response 
        # So we check to see if there are restaurants to return 
        if data['metaData']['resultCount'] > 0:
            # if there are restaurants to return then we only return the first 10 restaurant objects
            return data["restaurants"][:10]
        else:
            # otherwise if we do get an empty JSON object i.e. no restaurants, we tell the user there are no restaurants in that given postcode area
            print("There are no Restaurants currently serving within this postcode.\n\n")
            return
    # (ERROR handling) If the call to the API was unsuccessful, we return/print information about that error 
    else:
        try:
           # API endpoint/Server responds with Json object for some erroneous status' such as 401, 429, 500. If it does, this contains an error code and description we will try to access and print.
            errorResponse = response.json()["errors"]
            print(f"Error code: {errorResponse["errorCode"]}.\nReason: {errorResponse["description"]}.\n\n")
        except:
            # If the API endpoint/Server doesn't or can't return an Object for a failed call, then the json() function will throw an exception which we will catch. 
            # We then print the requests library's HTTP error code and reason instead of the endpoint's. 
            print(f"Error code: {response.status_code}.\nReason: {response.reason}.\n\n")



def format_response_data(data):
    """Formatting the response data so that it can be displayed properly in each row of the table."""

    # store each data row of the table in a list, as a list of lists
    tableData = []
    for restaurant in data:
        # Each restaurant can have multiple cuisines, so we store these in another temporary list so that we can correctly formulate and print the table
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
    """Printing the table with headers and row data. Headers are the requested data points, while row data is the response from the API."""

    # Requested data points to display. These will be the headings of the table
    headers = ["Restaurant name", "Cuisines", "rating", "Address"]
    print(tabulate(tableData, headers, tablefmt="grid", numalign="center", stralign="center") + "\n")


def main():

    # run function until user wants to quit
    while True:
       
        # Ask the user to input a postcode, this is formatted to remove all types of spaces including tabs and newlines, then converted to upper for use in the API
        userInput = "".join(input("Please enter your postcode or \"q\" to quit: ").split()).upper()
        # If the user inputs a single 'q' they quit the program
        if userInput == 'Q':
            break
        
        # if the wrong postcode is entered, then data is still returned by the API but its empty data, so we need to handle that
        # we do that by checking if data is no null
        data = call_api(userInput)
        if data:
            print_table(format_response_data(data))




if __name__ == "__main__":
    main()

