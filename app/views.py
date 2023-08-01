import json
from django.shortcuts import render,redirect
from django.views import View
from .models import MenAndWomen,Category,User,cart,payment
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

import stripe
from django.conf import settings


# Create your views here.

def home(request):

    data = MenAndWomen.objects.filter(category__in=[1, 2])[:4]
    ElectricData = MenAndWomen.objects.filter(category__in=[3])[:4]

    Categories = Category.objects.all()
    context = {

        'MenAndWomen':data,
        'electroncis':ElectricData,
        'categoryData':Categories
    }
        
    return render(request,'index.html',context)

def details(request,pk):
    Data = MenAndWomen.objects.filter(category=pk)
    context = {
        'category':Data
    }
    return render(request,'more_products.html',context)

def electronics(request,pk):
    Data = MenAndWomen.objects.filter(category=pk)
    context = {
        'category':Data
    }
    return render(request,'electroncs_cat.html',context)

def Signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')

        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            error_message = "Email is already exists"
            context = {
                'message':error_message
            }
            return render(request,'Signup.html',context)  # Replace 'form_view' with the URL name of the view handling this form

        # Hash the password securely
        hashed_password = make_password(password)

        # Save the data to the database
        user = User(email=email, name=name, password=hashed_password)
        user.save()

        # Redirect to a success page or do something else after successful form submission
        return redirect('/success_page')  # Replace 'success_page' with the URL name of your success page
    
    return render(request, 'Signup.html')

def success(request):
    return render(request,'success_page.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email exists in the database
        try:
            user = User.objects.get(email=email)
        except:
            error_message = "User with this email does not exist."
            context = {
                'message': error_message
            }

            return render(request, 'login.html', context)
        
        # Check if the provided password matches the hashed password in the database
        if check_password(password, user.password):
            # Password is correct, log in the user
            request.session['user_email'] = email
            return redirect('/')  # Replace 'success_page' with the URL name of your success page
        else:
            # Password is incorrect, show an error message
            error_message = "Invalid credentials. Please try again."
            context = {
                'message': error_message
    
            }

            return render(request, 'login.html', context)

    return render(request, 'login.html')

def add_to_cart(request,pk):
    Data = MenAndWomen.objects.get(pk=pk)

    email = request.session.get('user_email',None)
    if email:
        exist_email = get_object_or_404(User, email=email)
        
        cart_item = cart(user=exist_email, title=Data.title, price=Data.price,image=Data.image,quantity=1)
        cart_item.save()

       # Retrieve all cart items
        cartitem = cart.objects.all()
        # Assuming you have already retrieved the cart_items queryset
        cart_items = cart.objects.filter(user=exist_email)

        # Initialize the total price
        total_price = 0
        for item in cart_items:
           total_price += int(item.price)


        context = {
            
            'cartitems': cartitem,
            'price':total_price
        }
        
    else:
        print('User not login!')

    return render(request,'cart.html',context)

def deletecat(request,pk):
    MWData = get_object_or_404(cart, pk=pk)
    if MWData:
        MWData.delete()
        CartModel = cart.objects.all()
        email = request.session.get('user_email',None)
        exist_email = get_object_or_404(User, email=email)

        cart_items = cart.objects.filter(user=exist_email)

         # Initialize the total price
        total_price = 0
        for item in cart_items:
           total_price += int(item.price)

        context = {
        'cartitems':CartModel,
        'price':total_price
        }

        return render(request,'cart.html',context)


    return render(request,'cart.html')

def update(request, pk):
    if request.method == 'POST':
        try:
            cart_item = cart.objects.get(pk=pk)
            new_quantity = int(request.POST.get('quantity'))


            # Update the quantity of the cart item
            cart_item.quantity = new_quantity
            cart_item.save()
            cart_items = cart.objects.all()

            

        except cart.DoesNotExist:
            # Handle the case when the cart item with the given pk does not exist
            # You can choose to raise an exception, redirect to an error page, or handle it differently based on your use case.
            pass

    email = request.session.get('user_email',None)
    exist_email = get_object_or_404(User, email=email)
    cart_items = cart.objects.filter(user=exist_email)

    total_price = 0
    for item in cart_items:
        total_price += item.quantity * int(item.price)

    context = {
        'cartitems': cart_items,
        'price':total_price
    }
    return render(request, 'cart.html', context)

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiration_month = request.POST.get('expiration_month')
        expiration_year = request.POST.get('expiration_year')
        cvc = request.POST.get('cvc')

        try:
            # Create a token using the card details
            token = stripe.Token.create(
                card={
                    'number': card_number,
                    'exp_month': expiration_month,
                    'exp_year': expiration_year,
                    'cvc': cvc
                }
            )


            # Use the token for further processing or save it for later use
            # e.g., create a charge:
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents (e.g., $10 is 1000 cents)
                currency='usd',
                description='Payment for service/product',
                source=token.id,
            )

            # Handle successful payment here

            return JsonResponse({'success': True})

        except stripe.error.CardError as e:
            # Handle card errors here
            return JsonResponse({'success': False, 'error': str(e)})

        except stripe.error.APIConnectionError as e:
            # Handle API connection errors here
            return JsonResponse({'success': False, 'error': 'API Connection Error'})

        except stripe.error.StripeError as e:
            # Handle other Stripe-related errors here
            return JsonResponse({'success': False, 'error': 'Stripe Error'})

    return JsonResponse({'success': False, 'error': 'Invalid Request'})
    