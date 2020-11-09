#pandas and time
import time
import pandas as pd

#Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#BS4 
from bs4 import BeautifulSoup

#idk
import io
import os

# Vision API
from google.cloud import vision

#Test URL
url = "www.tuves.com/" # dont add https://

def get_images(url):
    
    # =============================================================================
    #  Selenium.
    # =============================================================================
    
    """ Selenium arguments.
        --incognito
        --headless
        --no sandbox
    
        Function only has 1 parameter url.
        -url: URL of the page we want to get 
        the missing alt text.
        
        This funcion will initiate chromedriver 
        and will scroll down to the bottom and
        wait 5 seconds so that all images are loaded.
        
        then it will save the html source and pass it
        to the img_alt_src function
    """

    chrome_options = Options()
    #chrome_options.add_argument('--incognito')
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=chrome_options,executable_path='/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
    driver.get('https://' + url)
    
    #scrolling to bottom to load all images on the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #sleep to make sure everything loads
    time.sleep(5)
    
    
    html_source = driver.page_source
    
    img_alt_src(html_source)
    
    driver.close()
    driver.quit()

def img_alt_src(html_source):
    # =============================================================================
    # Beautiful soup
    # =============================================================================
    
    """ 
    This function uses BS4 and takes 1 argument html_source.
    -html_source: is the plain html that is passed from get_images.
    
    After we get the raw html we find all alt text of the images and 
    save them into alt_txt.
    
    We do the same with all the image src of the images on the page. 
    We save it on img_url.
    
    We then pass these two data frames into the cleaning() function.
    """
    
    bs = BeautifulSoup(html_source, 'html.parser')
    
    #Getting all Alt text from HTML 
    alt_txt = [] 
    img_url = []
    for img in bs.find_all('img', alt=True):
        try:
            print(img['alt'])
            print(img['src'])
            a = img['alt']
            s = img['src']
            alt_txt.append(a)
            img_url.append(s)
        except:
            print('pass')
        
    
    cleaning(alt_txt, img_url)
 
def cleaning(alt_txt,img_url):
    # =============================================================================
    # Data cleaning
    # =============================================================================
    
    """ The cleaning function has 2 arguments.
        -alt_txt: df with all the alt text of the page.
        -img_url: all image urls of the page.
        
        In this funtion we perform a cleaning of the DF.
        We take the 2 arguments and create one data frame,
        we then drop all duplicates from both columns.
        After this we create a new list wil only the empty 
        alt text urls.
        
        After we get those we transfrom the list of URLs that
        are missing alt text into a DataFrame.
     """
    
    #Zipping img alt and src in 1 DF
    df = pd.DataFrame(list(zip(alt_txt, img_url)),
                  columns=['alt text','img src'])
    
    
    #dropping any duplicates from both columns
    df = df.drop_duplicates(['alt text','img src'],keep= 'last')
    
    
    ## This might not be applied to every single site. Cleaning anything that has data on
    df = df[~df['img src'].str.contains('data')]
    
    
    #removing anything that is not jpg,png,gif 
    image_type =[".jpg",
                 ".png",
                 "gif",
                 ]
    #here we check if url string includes any of the values of image_type
    clean_urls = []
    clean_alt = []
    for i,b in zip (df['img src'], df['alt text']):
        if any(x in i for x in image_type):
            print(i, "its image")
            clean_urls.append(i) 
            clean_alt.append(b)
        else:
            print(i, 'not image')
    
    #df with clean data       
    df = pd.DataFrame(list(zip(clean_alt,clean_urls)),
                      columns=['alt text','img src'])
    
    
    #checking if src links are absolute or relative
    clean_urls= []
    clean_alt = []
    for i,b in zip (df['img src'], df['alt text']):
        if url not in i:
            print('relative, doesnt contain' ,url)
            clean_urls.append(url + i)
            clean_alt.append(b)
        else:
            print('absolute, it does contain', url)
            clean_urls.append(i)
            clean_alt.append(b)
            
    #clean DF 
    df = pd.DataFrame(list(zip(clean_alt,clean_urls)),
                      columns=['alt text','img src'])
    
    
    #checking https when there is no https://
    clean_urls= []
    clean_alt = []
    for i,b in zip (df['img src'], df['alt text']):
        if "https://" not in i:
            print('not https://')
            clean_urls.append('https://' + i)
            clean_alt.append(b)
        else:
            print('its https')
            clean_urls.append(i)
            clean_alt.append(b)
             
    #clean DF 
    df = pd.DataFrame(list(zip(clean_alt,clean_urls)),
                      columns=['alt text','img src'])
    
    #check if url contains 4 ////  (this is stupid)
    clean_urls= []
    clean_alt = []
    for i,b in zip (df['img src'], df['alt text']):
        if "////" in i:
            print('it has ////')
            x = i.replace('////','//')
            clean_urls.append(x)
            clean_alt.append(b)
        else:
            print('its https')
            clean_urls.append(i)
            clean_alt.append(b)
             
    #clean DF 
    df = pd.DataFrame(list(zip(clean_alt,clean_urls)),
                      columns=['alt text','img src'])
    


    #limiting only top 11 images from list( So that the api costs are not that high :D )
    df = df.head(15)
    
    #here we run our function for alt tet recommendations.
    reco_alt = []
    for a,b in zip(df['img src'], df['alt text']): 
        print(a,b)
        p = detect_web(a)
        reco_alt.append(p)
    
    #Final DF with alt text recos    
    df['recommended alt'] = reco_alt
    
    json_hist = df.to_json(orient="table")
    #return Response(json_hist, mimetype='application/json')

    print(df)
    
    df.to_csv('alt_text.csv', index = False)
    
    
    ### We might need this later, for now we will suggest top 15 images alt text ###
    
    # #creating new list with all empty alt txts
    # empty_alt = []
    # for alt,src in zip(df['alt text'], df['img src']): 
    #     if alt:
    #         print('Alt Text is --> ' ,alt, 'Not empty' )
    #     else:
    #         print('Alt text is empty. img scr is ---> ', src)
    #         a = src
    #         empty_alt.append(a)
    
    
                  
    # #transforming list into DF
    # empty_alt = pd.DataFrame(empty_alt, columns=['img src'])
    # print(empty_alt)

def detect_web(uri):
    # =============================================================================
    # Google Vision API
    # =============================================================================

    """ Function with 1 parameter: 
       - uri: URL of the image. 
       This will output Web Entities and 
       Labels of the image
       """
    """Detects web annotations given an image."""
    
    client = vision.ImageAnnotatorClient.from_service_account_json("/Users/kburchardt/Desktop/Scripts/alt/seo-projects-284600-ff9d5e6a2a34.json")
    
    image = vision.Image()
    image.source.image_uri = uri
    
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    lbls = []
    for label in labels:
        l = label.description
        lbls.append(l)
        print(label.description)
        
        
    response = client.web_detection(image=image)
    annotations = response.web_detection
    best_label = []
    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            #print('\nBest guess label: {}'.format(label.label))
            l = label.label
            best_label.append(l)
            print("Best guess label:" , l)


    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))
        
        web_entities = []
        for entity in annotations.web_entities:
            w = entity.description
            web_entities.append(w)
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))
            
    try:
        
        alt = best_label[0] +' ' +  web_entities[0]
        print('recomended alt text: ', alt)
        return alt
    
    except:
        print('fuckit')
    
    


    if response.error.message:
        alt = 'Error! Try Again'
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message)) 
        
       
    








