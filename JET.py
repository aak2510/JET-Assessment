import requests
from tabulate import tabulate


def call_api(postcode):

    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["restaurants"][:10]
    else:
        print("Something went wrong... {}".format(response.status_code))



    


def format_response_data(data):

    tableData = []
    for restaurant in data:
        cuisineList = []
        for cuisine in restaurant["cuisines"]:
            cuisineList.append(cuisine["name"])

        tableData.append([
                restaurant["name"],
                "\n".join(cuisineList),
                restaurant["rating"]["starRating"],
                f"{restaurant["address"]["firstLine"]}\n{restaurant["address"]["city"]}\n{restaurant["address"]["postalCode"]}"
                ])


    return tableData

def print_table(tableData):

    headers = ["Restaurant name", "Cuisines", "rating", "Address"]
    print(tabulate(tableData, headers, tablefmt="grid", numalign="center", stralign="center"))


def main():
    print_table(format_response_data(call_api("UB56LH")))

    

if __name__ == "__main__":
    main()

