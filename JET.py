import requests


def get_restaurant_data(postcode):

    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = response.json()["restaurants"][:10]
        return data
    else:
        print(response.status_code)


def display_restaurants(data):

    for restaurant in data:
        print("Name: " + str(restaurant["name"]))
        print("restaurant rating: " + str(restaurant["rating"]["starRating"]))
        # For each restuarent we need to create a list of its cuisines to print on one line
        cuisineList = []
        for cuisine in restaurant["cuisines"]:
            cuisineList.append(cuisine["name"])
        print(f"cuisine: {', '.join(cuisineList)}")
        print(
            "address: {}, {}, {}".format(
                restaurant["address"]["firstLine"],
                restaurant["address"]["city"],
                restaurant["address"]["postalCode"],
            )
        )
        print()


def main():
    # Replace with your desired postcode
    postcode = "UB56LH"

    restaurants = get_restaurant_data(postcode)

    if restaurants:
        display_restaurants(restaurants)
    else:
        print("Failed to fetch restaurant data.")


if __name__ == "__main__":
    main()
