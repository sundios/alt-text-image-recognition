# Image recognition Alt text Generator

Foobar is a Python library for dealing with word pluralization.

This Python script get the top 15 images on a URL and check the current alt text and the scans each image URL and recommends a new alt text based on what Google vision API see.


## Installation

To use this script there are a some libraries and some setup to do in order tu run it succesfully.

### Requirements.txt

First we need to install the important libraries we are using for that we can run our `requirements.txt`

```bash
pip install requirements.txt
```

### Selenium chromedriver

Once we have our libraries installed, we need to install chromedriver and on line 50 we need to specify the `executable_path='` 

```python
driver = webdriver.Chrome(options=chrome_options,executable_path='/usr/local/bin/chromedriver')  # <----Here
```

To learn more about how to set up this you can [click here](https://chromedriver.chromium.org/getting-started)

### Google Vision API

Finally we need to get our Google vision API activated and get our `.json` file with our keys.
To activate the API and get the .json api with your private key please follow [Google instructions here](https://cloud.google.com/vision/docs/setup). If you have any problem please create an issue and I will be happy to help.

Once you have the file you need to update line 223 and add your path to you .json file

```python
    client = vision.ImageAnnotatorClient.from_service_account_json("add your PATH here")
```


## Usage

Using this script is very easy. You can import it and set a new url variable and then call the get_url(ulr) function.


```python
import alt


url = 'https://www.uselessthingstobuy.com/gifts/gifts-under-25/' # Overwrites url in the script
get_images(url) #call function with our new URL

```

Once you run this it will go and look for top 15 images and alt text that your page have and will createa  DataFrame with current alt text, URL and recommended alt text.


| alt text                     | img src                                                                                                         | recommended alt                                                                    |
|------------------------------|-----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Image of the month: November | https://www.uselessthingstobuy.com/logos/November.png                                                           | steve the jumping dinosaur Dinosaur                                                |
|                              | https://www.uselessthingstobuy.com/wp-content/uploads/2020/10/Screen-Shot-2020-10-17-at-11.50.20-AM-300x300.png | grip and tricks all five rider box Grip & Tricks Finger Roller                     |
|                              | https://www.uselessthingstobuy.com/wp-content/uploads/2020/10/Screen-Shot-2020-10-17-at-11.50.05-AM-300x300.png | grip and tricks inline skates 4 pack GRIP&TRICKS                                   |
|                              | https://www.uselessthingstobuy.com/wp-content/uploads/2020/10/Screen-Shot-2020-10-14-at-10.15.47-AM-300x300.png | titanic tea infuser Tea                                                            |
|                              | https://www.uselessthingstobuy.com/wp-content/uploads/2020/10/Screen-Shot-2020-10-14-at-10.15.36-AM-300x300.png | Brand: Fred & Friends Fred Tea Infuser Tea                                         |
|                              | https://www.uselessthingstobuy.com/wp-content/uploads/2020/08/b8gqhjx3uwf51-300x300.jpg                         | chicken feet socks Chicken                                                         |
|                              | https://www.uselessthingstobuy.com/wp-content/uploads/2020/08/Screen-Shot-2020-08-09-at-10.17.25-PM-300x300.png | calcetas de pollo MOXY Socks Girl's Chicken Legs Knee-High Fitness   Novelty Socks |
| trump putin 2020 car shade   | https://www.uselessthingstobuy.com/wp-content/uploads/2020/07/trump_putin_2020_car_shade-300x300.jpg            | funny windshield sun shade Windshield                                              |
| kim trump putin car shade    | https://www.uselessthingstobuy.com/wp-content/uploads/2020/07/kim_trump_putin_2020-300x300.jpg                  | funny car sun shade Car                                                            |
| bottle cap gun launcher      | https://www.uselessthingstobuy.com/wp-content/uploads/2020/03/bottle-cap-gun-launcher-1-300x300.jpg             | cap gun bottle opener Wine                                                         |
|                              | https://www.uselessthingstobuy.com/wp-content/uploads/2020/03/bottle-cap-gun-launcher-300x300.jpg               | hand Bottle opener                                                                 |
| creepy unicorn mask          | https://www.uselessthingstobuy.com/wp-content/uploads/2020/03/creepy_unicorn_mask-300x300.jpg                   | Mask Mask                                                                          |
| creepy unicorn mask          | https://www.uselessthingstobuy.com/wp-content/uploads/2020/03/creepy_unicorn-300x300.jpg                        | snout Mask                                                                         |
| lego builder mug             | https://www.uselessthingstobuy.com/wp-content/uploads/2020/03/lego_builder_mug-300x300.jpg                      | lego mug Build-On Brick Mug-Red                                                    |
| trump fortune teller         | https://www.uselessthingstobuy.com/wp-content/uploads/2020/03/trump_fortune_teller-300x300.jpg                  | president predicto donald trump fortune teller ball Magic 8-Ball                   |

If you weant to remove the limit you can comment it out by adding a # on line 175

```python
#limiting only top 11 images from list( So that the api costs are not that high :D )
    df = df.head(15)

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

