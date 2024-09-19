# quotes/views.py
# view functions to handle URL requests for the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# global lists for quotes and images urls
all_quotes = ["No matter how hard it is right now, think of how the result will make you feel.", 
              "Go on your own path, even if you live for a day.",
              "Don't give up on a dream you've been working on nearly your entire life.",
              "Remember, there is someone, in South Korea, in the city of Seoul who understands you.",
              "I feel that we are only running forwards without a rest. I hope we can find time to relax and smile.",
              "I want you to be your light baby, you could be your light. So you don't have to be in pain, so you can smile.",
              "Now promise me, several times a day, though you feel alone, don't throw yourself away, hold on for a moment, cross our pinkies, and promise me now.",
              "Never give up on a dream that you've been chasing almost your whole life.",
              "Don't be trapped in someone else's dream.",
              "Go on your own path, even if you live for a day."]
all_urls = ["https://i.pinimg.com/736x/d0/93/56/d0935608d8dc9000b379307e1efb069e.jpg", 
            "https://pyxis.nymag.com/v1/imgs/82f/f08/28fc7928bc8feb5d634d15d4143e096d32-jimin.1x.rsquare.w1400.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/a/a5/Park_Ji-min_on_the_Billboard_Music_Awards_red_carpet%2C_1_May_2019.jpg",
            "https://static.wikia.nocookie.net/my-bts-fanfic/images/f/fb/413E6286-69B8-465E-867D-77CC243746D2.jpeg/revision/latest?cb=20210421163000",
            "https://preview.redd.it/do-you-think-park-jimin-is-handsome-v0-gy9mad8xedy91.jpg?width=640&crop=smart&auto=webp&s=33478bf194dda451ffb22ef36a557b6cda9ec5c6", 
            "https://www.billboard.com/wp-content/uploads/media/Jimin-bts-press-photo-2017-billboard-1548.jpg?w=1024",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqlUxxjWwfddfL_Nafb9R4Py78VV2VedrDiA&s",
            "https://i.pinimg.com/736x/80/94/eb/8094eb156992b736588ee8d62639f085.jpg",
            "https://w0.peakpx.com/wallpaper/374/258/HD-wallpaper-jimin-bts.jpg",
            "https://www.billboard.com/wp-content/uploads/2024/07/Jimin-blooming-02-Courtesy-of-BIGHIT-MUSIC-billboard-1548.jpg?w=942&h=623&crop=1" ]

def quote(request):
    '''
    Function to handle the URL request for /quotes (home page).
    Delegate rendering to the template quotes/quote.html.
    '''
    # use this template to render the response
    template_name = 'quotes/quote.html'

    # create a dictionary of context variables for the template:
    context = {
        "random_quote" : all_quotes[random.randint(0, len(all_quotes)-1)], # grabs random quote
        "random_url": all_urls[random.randint(0, len(all_urls)-1)] # grabs random img url
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    '''
    Function to handle URL request for /quotes/show_all page
    Delegates rendering page to template quotes/show_all.html
    '''
    # use this template to render the response
    template_name = 'quotes/show_all.html'

    # create a dictionary of context variables for the template:
    context = {
        "all_quotes" : all_quotes, # gets all quotes
        "all_urls" : all_urls, #gets all urls
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle URL request for /quotes/about page
    Delegates rendering page to template quotes/about.html
    '''

    # use this template to render the response
    template_name = 'quotes/about.html'

    # create dictionary of context variables for the template:
    context = {

    }

    # delegate rendering work to the template
    return render(request, template_name, context)
