from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from order.models import customer
from restro.models import Feature, Special
from booktable.models import Table_booked
from contact.models import Contact
from django.core.mail import message, send_mail,EmailMultiAlternatives
from order.models.product import Product
from order.models.category import Category
from django.views import View
from order.models.customer import Customer
from order.models.orders import Order
from django.contrib.auth.hashers import make_password,check_password
from order.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
from order.helpers import send_forget_password_mail
from order.models.forgotpassword import Profile

 



def index(request):
    features=Feature.objects.all()
    specials=Special.objects.all()
    print('you are:',request.session.get('email'))
    return render(request,"index.html",{'features':features,'specials':specials})

#def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2'] 

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email is already exist!')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username is already exist!')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save() 
              

                return redirect('login')   
        else:
            messages.error(request,'Password not match!')
            return redirect('register')    

    else:
        return render(request,"register.html")
def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password2=request.POST.get('password2') 
        #validation
        error_message=None
        customer=Customer(name=name,email=email,password=password,password2=password2)
        
        if(not name):
            error_message='Username is Required !!'
        elif len(name)<4:
            error_message='Username must be 4 or more character long !! ' 
        elif not password:
            error_message='Password is Required !!'
        elif len(password)<4:
            error_message='Password is too short'    
        elif len(password)<6:
            error_message='Password must be 6 char long'        
        elif not password==password2:
            error_message='Password does not match !!'
        elif password==password2:
            if customer.isExists():
                error_message='Email is already exist !!'
                
        #saving
        if not error_message:
            print(name,email,password,password2)
            customer.password=make_password(customer.password)
            customer.password2=make_password(customer.password2)
          
            customer.register()
            return redirect('login')
        else:    
            return render(request,"register.html",{'error':error_message})
                                         

#def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['customer_id']=user.id
            return redirect('restro/')
        else:
            messages.info(request,'Invalid Credentials!')
            return redirect('login')    
    else:
        return render(request,"login.html")        
def login(request):
    return_url=None
    if request.method=='GET':
        return_url=request.GET.get('return_url')#('return_url') gives the url which it contains eg./myorders and store this in return_url variable
        print(return_url)
        return render(request,"login.html")
    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer.get_customer_by_email(email)
       # customername=Customer.get_customer_by_name(name)
        error_message=None
       
        if customer:
            flag=check_password(password,customer.password)
            if flag:
                request.session['customer']=customer.id
                if return_url:
                    return HttpResponseRedirect(return_url)#if it conditio satisfy then it goes to /myorders urls              
                else:
                    return_url=None #else return_url again refresh to none means it never again return the myorders page it will again null and go to homepage restro  
                    return redirect('restro')    
            else:
                error_message='Invalid Credentials !!'    
        else:
            error_message='Invalid Credentials !!'

      
        print(name,email,password)    
        return render(request,"login.html",{'error':error_message})
def logout(request):
    request.session.clear()
    return redirect('restro/')   

import uuid
def forgotpassword(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')

        if not Customer.objects.filter(name=name).first():
            messages.info(request,'No user found with this username.')
            return redirect('forgotpassword')


        user_obj=Customer.get_customer_by_name(name) 
        token=str(uuid.uuid4())
        product=Profile(user=user_obj,forgot_password_token=token)
        product.save()
        send_forget_password_mail(user_obj,email,token)
        messages.info(request,'An Email is Sent')
        return redirect('forgotpassword')
    else:
        return render(request,"forgotpassword.html")   


def  confirm_pwd(request,token):
    context={}
    profile_obj=Profile.objects.filter(forgot_password_token=token).first()
    context={'user_id':profile_obj.user.id}
    if request.method=='POST':
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        user_id=request.POST.get('user_id')

        if user_id is None:
            messages.info(request,'No UserId found')
            return redirect(f'confirm_pwd{token}')

        if new_password != confirm_password:
            messages.info(request,'Password not match.Try again')
            return redirect(f'confirm_pwd{token}')
        
        user_password=make_password(new_password)
        user_password2=make_password(confirm_password)
        user_obj=Customer(id=user_id,password=user_password,password2=user_password2)
        user_obj.save()
       
        
     
        return redirect('login') 

   

    return render(request,"confirm_pwd.html",context)        
                

#def booktable(request):
    reserve_form=BookTableForm()

    if request.method == 'POST':
        reserve_form=BookTableForm(request.POST)

        if reserve_form.is_valid():
            reserve_form.save()
            messages.info(request,'Your booking request was sent. We will call back or send an Email to confirm your reservation. Thank you!')
            return redirect('table_booked')
    context={'form':reserve_form}  
    
    return render(request,"booktable.html",context)   
def booktable(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        date=request.POST['date']
        time=request.POST['time']
        persons=request.POST['person']
        message=request.POST['message']
        data=Table_booked(name=name,email=email,phone=phone,date=date,time=time, no_of_persons=persons,message=message)
        data.save()
        return redirect('table_booked')
    return render(request,"booktable.html")   

def table_booked(request):
    return render(request,"table_booked.html")  

def order(request):
    return render(request,"order.html") 

class OrderPanel(View):
    #this post method generally used to perform some tasks in ordering process
    def post(self,request):
        product=request.POST.get('product')#to take product from template
        remove=request.POST.get('remove')#to remove in cart
        cart=request.session.get('cart')#this is for taking coookies from the cart
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:    
                        cart[product]=quantity-1
                else:    
                    cart[product]=quantity+1
            else:    
                cart[product]=1
        else:
            cart={}
            cart[product]=1

        request.session['cart']=cart    
        print( 'cart',request.session['cart'])
        print('product:',product)
       #print('quantity:',quantity)
        return redirect('orderpanel')
    #this get method simply work to print data in the templates dyanamically
    #dynamically 
    def get(self,request):
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}#initially cart is empty when any anonymous user will come
        products=None
        categories=Category.get_all_categories()#all categories come here from category models
        categoryID=request.GET.get('category')#here the categories are take from the server 
        if categoryID:
            products=Product.get_all_products_by_categoryid(categoryID)#If there are different categories then it return the categoryID means only category of that id
        else:
            products=Product.get_all_products(); #else return all products of different categories   
        data={}
        data['products']=products
        data['categories']=categories
        print('you are:',request.session.get('email'))#this is for testing purpose in console
        return render(request,"orderpanel.html",data)


           

class Cart(View):
    def get(self,request):
        ids=list(request.session.get('cart').keys())#keys of each product which contain in list is passed and store in ids
        products=Product.get_products_by_id(ids)# ids is passed here on the basis of list's items
                                                #and get_products _by_id is a static method to take list items dynamicall
        print(products)
        return render(request,"cart.html",{'products':products})   

class Checkout(View):
    def post(self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        products=Product.get_products_by_id(list(cart.keys()))
        print(address,phone,customer)

        for product in products:
            order=Order(customer=Customer(id=customer),#Customer object is made and pass the id of customer in it
                        product=product,
                        price=product.price,
                        address=address,
                        phone=phone,
                        quantity=cart.get(str(product.id))#becoz product id is number value 
                        )
            order.save()            
        request.session['cart']={}#call the placeorder method from the orders.py
        return redirect('cart')

class Myorders(View):

    #@auth_middleware <-- this is wrong way of use middleware 
    #so we import method_decorator to use  middleware here
    #@method_decorator(auth_middleware) this is the right method to use this method
    #but now i will use the alternative way to use middlewares go to th urls.py
    def get(self,request):
        customer=request.session.get('customer')#customer id is get
        orders=Order.get_orders_by_customer(customer)
        print(orders)
        return render(request,"myorders.html",{'orders':orders})       
                 




def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        data=Contact(name=name,email=email,subject=subject,message=message)
        data.save()
        
       
        subject='Delicious'
        from_email='testingpurpose8000@gmail.com'
        msg=f'Hi {name}, We have received your message.For few minutes we make a confirmation call.Please accept this.Thanking you to contact with us ☺.For any information call us 992199129 '
        to=[email]
        send_mail(subject,msg,from_email,to,fail_silently=False)
       
       
    return render(request,"contact.html")          

