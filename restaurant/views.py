from django.shortcuts import redirect, render
import random 
from datetime import datetime, timedelta
# Create your views here.

specials = ["Beef Wellington - $30", "Osetra Caviar - $30", "Nurungji Foie Gras - $30"]
specials_img = ["https://s3-media0.fl.yelpcdn.com/bphoto/QlFqLYp1njQ5NVABa1NwRA/348s.jpg","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6Oyc7fnuaTCQD9ExyzMIMsDK9a4ZvQwmTDw&s", "https://blog.resy.com/wp-content/uploads/2021/03/jpg-800x591.jpeg"]
specials_desc = ["classic English dish of beef tenderloin coated in pâté and duxelles, wrapped in puff pastry, and baked", "Comes from the Ossetra sturgeon and is known for its golden or brownish color, nutty flavor", "Features foie gras, crispy rice, and sweet soy sauce"]

def main(request):
  ''' Show the main restuarant page '''
  template_name = "restaurant/main.html"

  # pass in templates an image of soogil
  context = {
    'image': "https://cdn.vox-cdn.com/thumbor/PQ1UxWSnao32MwEJlRytL7E7XSw=/0x0:5400x3619/1200x800/filters:focal(2268x1378:3132x2242)/cdn.vox-cdn.com/uploads/chorus_image/image/58265777/Soogil_Int_Wide_by_Michael_Tulipan.0.jpeg",
  }
  return render(request, template_name, context)

def order(request):
  ''' Show the order page '''
  template_name = "restaurant/order.html"

  # random num
  random_num = random.randint(0,len(specials)-1)
  # pass into templates a random daily special
  context = {
    'daily_special': specials[random_num],
    'daily_special_img' : specials_img[random_num], 
    'daily_special_desc': specials_desc[random_num],
    'beef_tartare': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSx2DoEkjte6ukggf5XHYoKGJvYsS7zBlCNKA&s",
    'honey_soup': "https://deliciouslittlebites.com/wp-content/uploads/2022/11/Honeynut-Squash-Soup-Recipe-Image-1-3.jpg",
    'duck': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQiTtUeLmeQiq5woDGGJ3MkHYU0DQSqOlN9QQ&s",
  }
  
  return render(request, template_name, context)

def confirmation(request):
  '''
  Handles form submission
  Reads form data from request and sends back to template
  '''

  template_name = "restaurant/confirmation.html"

  # check if POST request
  if request.POST:
      # read form data into python variables
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']

    # add items to cart if checkbox selected
    cart = []
    # add based on price
    total = 0
    if('duck' in request.POST):
      cart += ['Duck - $36']
      total += 36
    if('beef' in request.POST):
      cart += ['Beef - $33']
      total += 33
    if('soup' in request.POST):
      total += 18
      if('mushroom' in request.POST):
        if('nuts' in request.POST):
          cart += ['Soup (no nuts, no mushroom) - $18']
        else:
          cart += ['Soup (no mushroom) - $18']
      elif('nuts' in request.POST):
        cart += ['Soup (no nuts) - $18']
      else:
        cart += ['Soup - $18']
    if('caviar' in request.POST):
      cart += ['Caviar (on the side) - $5']
      total += 5
    if('daily_special' in request.POST):
      cart += ['Daily Special - $30']
      total += 30

    # calculate ETA
    current_time = datetime.now()
    time_to_add = timedelta(minutes=random.randint(30,60))
    ETA = current_time + time_to_add

    # package form data up as context variables for template
    context = {
      'name': name,
      'phone': phone,
      'email': email,
      'cart': cart,
      'total': total,
      'ETA': ETA
    } 

    return render(request, template_name, context)
  # Handle get request
  return redirect("order")

