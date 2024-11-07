import requests

def download():
    """Download a random image from the internet.
    """
    url = 'https://picsum.photos/600/900'  # This gets a random 600*900 image

    response = requests.get(url)

    if response.status_code == 200:
        with open('random_image.jpg', 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image.")

def main():
    print("Hello, welcome to the random image downloader.")
    download()


if __name__ == "__main__":
    main()
