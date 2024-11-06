import requests

def main():
    """Download a random image from the internet.
    """
    url = 'https://picsum.photos/200/300'  # This gets a random 200x300 image

    response = requests.get(url)

    if response.status_code == 200:
        with open('random_image.jpg', 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image.")

    print("Done.")

if __name__ == "__main__":
    main()
