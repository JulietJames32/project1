from django.shortcuts import render,redirect,get_object_or_404
from.models import Product,Order,OrderItem
from.models import Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from.forms import UserRegistrationForm
from.forms import Product_Form,ReviewForm
from django.http import Http404
from django.views.generic.edit import FormView
from django.http import HttpResponse



def home(request): #defining home page
    products=Product.objects.all() #calling all the products from modelclass product
    return render(request,"home.html",{'products':products})#rendering dictionary to home page

def about(request): #defining about page
    return render(request,"about.html",{})

def product(request,pk):
    product=Product.objects.get(id=pk) #calling the product from modelclass product
    return render(request,"product.html",{'product':product})
def product_list(request):
    products=Product.objects.all()
    return render(request,"product_list.html",{'products':products})

def category(request,foo): 
     foo=foo.replace('-',' ') #replacing any hyphen with spaces
     try:
          category=Category.objects.get(name=foo)
          products=Product.objects.filter(category=category)
          return render(request,"category.html",{'products':products,'category':category})
     except:     
          messages.success(request,("category doesnt exist!"))
          return redirect ('home')


def login_user(request):                #defining finction to login
      if request.method == "POST":       #if it is post method then password and username are authenticated and redirects to home page
           username=request.POST['username']
           password=request.POST['password']
           user=authenticate(request,username=username,password=password)
           if user is not None:
                login(request,user)
                return redirect("home")
           else:
                error_message = 'Invalid username or password.' #if authentication is not done again it will redirect to login page and shows a error message
                return redirect("login")     
      else: 
            error_message=None
            return render(request,"login.html",{'error_message': error_message})

def logout_user(request): #logout is defined
     logout(request)
     return redirect(home)

def register_user(request): #registering a new user
     if request.method=='POST':
          form=UserRegistrationForm(request.POST) #form from form class is assigned to a new variable
          if form.is_valid(): #if form is valid(all the fielda are entered as per the defined instructions),it will be saved
               form.save()
               return redirect('login') #after the form is saved redirected to login page,there you can login based on new uername and password
          else:
               messages.success(request,("please try again!!")) #if it is not valid and saved ,register function is recalled
               return redirect('register')
     else:
          form=UserRegistrationForm() #if it is not post method ,then it will again render the register template to fill up
          return render(request,'register.html',{'form':form})  
       
def add_product(request): #to add the product,functiopn is defined
     if request.method == 'POST':
          form=Product_Form(request.POST) #if request method is post form created in forms.py is called and we can add product details and then can save if the data entered is valid,it will shown in the home page
          if form.is_valid():
            form.save()
            return redirect('home')

     else:
          form=Product_Form()
          return render(request,'add_product.html',{'form':form})

def edit_product(request,pk): #similarly we can add fuction to edit the product data
      product=get_object_or_404(Product,pk=pk)
      if request.method=='POST':
        form=Product_Form(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('home') 
      else:
        form=Product_Form(instance=product)
        return render(request,'edit_product.html',{'form':form}) 


def delete_product(request,pk):# FUNCTION for deleting products
    product=get_object_or_404(Product,pk=pk)
    
    if request.method=='POST':
        product.delete() #that form product which is saved in product is deleted
        return redirect("home")
    
    return render(request,'delete_product.html',{'product':product})
def get_cart(request):
    cart_id=request.session.get('cart_id')#retrieves the cart id from user session
    if cart_id:#To determine whether the function should retrieve an existing cart or create a new one.
        cart=Order.objects.get(id=cart_id)
    else:
        cart=Order.objects.create()#If the user does not have a cart, a new Order instance is created. This  creates a new empty cart for the user.
        request.session['cart_id']=cart_id
        return cart   
@login_required
def cart_details(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'order': order
        }
    except Order.DoesNotExist:
        context = {
            'message': 'Your cart is empty.'
        }
    return render(request,'cart.html',context)  
@login_required  
def add_to_cart(request,pk):#add a product to the orderitem and assosiate it with order
   #get that particular product of id=pk
   product=Product.objects.get(pk=pk)
   #create orderitem
   order_item,created=OrderItem.objects.get_or_create(
       product=product,
       user=request.user,
       ordered=False,
   )
   order_qs = Order.objects.filter(user=request.user, ordered=False)
   if order_qs.exists():
        order = order_qs[0]
        # If the order item is already in the order, update the quantity
        if order.items.filter(product__id=product.id).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
   else:
        # If the user does not have an active order, create a new order
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
   return redirect("cart_details")  # Redirect to cart details

@login_required
def remove_from_cart(request,pk):
    order = Order.objects.filter(user=request.user, ordered=False).first()  # Get active order (not ordered yet)
    
    if not order:
        raise Http404("You do not have an active order.")
    
    product = get_object_or_404(Product, id=pk)# Get the product to remove
    # Check if the order contains the product
    try:
        cart_item = OrderItem.objects.get(product=product, user=request.user, ordered=False)
    except OrderItem.DoesNotExist:
        raise Http404("This item is not in your cart.")
    
    order.items.remove(cart_item)# Remove the item from the order
    
    #  you could delete the OrderItem if the quantity is reduced to zero or if it's no longer needed
    cart_item.delete()

    return redirect('cart_details')

class ReviewEmailView(FormView):
    template_name='review.html'
    form_class=ReviewForm

    def form_valid(self,form):
        form.send_email()
        msg='Thank you for the review'
        return HttpResponse(msg)

    
    
