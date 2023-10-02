from django.shortcuts import render,HttpResponse,redirect
from storeapp.models import Product,Cart,Orders
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.
'''
def function_name(request):
    function body
    return HttpResponse(data)     
'''
def home(request):
    p=Product.objects.all()  #list of product is in variable p
    #print(p)
    context={}
    context['user']="itvedant"
    context['x']=20
    context['y']=40
    context['l']=[10,20,30,40,60]
    context['d']={'id':1,'name':'machine','price':2500,'qty':2}
    context['data']=[

             {'id':1,'name':'machine','price':2500,'qty':5},
             {'id':2,'name':'Samgsung','price':12500,'qty':2},
             {'id':3,'name':'apple','price':15000,'qty':5},

    ]

    context['products']=p
    return render(request,'home.html',context) #passing context to home.html

def edit(request,rid):
    #print("Id to be edited:,",rid)
    #return HttpResponse("Hello from Edit"+rid)
    if request.method=='GET':
        p=Product.objects.filter(id=rid) #select * from storeapp_product where id=2
        context={}     #creating Empty Dictionary
        context['data']=p   # assigning fetch product to key data in context dictionary
        return render(request,'Edit.html',context) # passing dict. context to Edit.html
    else:
        uname=request.POST['pname']
        uprice=request.POST['price']
        uqty=request.POST['Qty']
        #print("Name:",uname)
        #print("Price:",uprice)
        #print("qty:",uqty)
        p=Product.objects.filter(id=rid)
        p.update(name=uname,price=uprice,qty=uqty)
        return redirect('/home')

def delete(request,rid):
    #return HttpResponse("Id to be Deleted"+rid)
    p=Product.objects.filter(id=rid)
    p.delete()
    return redirect('/home')

def greet(request):
    return render(request,'base.html')

def addproduct(request):
    #print(request.method)
    if request.method=="GET":
        print("In if part") 
        return render(request,'addproduct.html')
    else:
        print("In Else Part")
        product_name=request.POST['pname']
        price=request.POST['price']
        quantity=request.POST['Qty']
        #print("Name:",product_name)
        #print("Price:",price)
        #print("Quantity:",quantity)
        #insert record into object
        p=Product.objects.create(name=product_name,price=price,qty=quantity)
        print("Product Object",p)
        p.save()
        #return HttpResponse("Data is inserted into table")\
        return redirect('/home')

# function for Ecommerce Website

def index(request):
    uid=request.user.id
    print("user id",uid)
    print(request.user.is_authenticated)
    print(request.user.username)
    p=Product.objects.filter(is_active=True)
    context={}
    context['Products']=p
    return render(request,'index.html',context)

def details(request,id):
    p=Product.objects.filter(id=id)
    print(p)
    context={}
    context['products']=p
    return render(request,'details.html',context)

def userlogin(request):
    context={}
    if request.method=='GET':
       return render(request,'login.html')
    else:
        uname=request.POST['lname']
        upass=request.POST['lpass']
        #print(uname)
        #print(upass)
        u=authenticate(username=uname,password=upass)
        if u is not None:
            login(request,u)
            return redirect('/index')
        else:
            context['errmsg']="Invalid Username and Password"
            return render(request,"login.html",context)

def register(request):
    context={}
    if request.method=='GET':
        return render(request,'register.html',context)
    else:
        user=request.POST['uname']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        #Validation
        if user== '' or p== '' or cp== '':
            context['errmsg']="Fields cannot be Empty"
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']="Password Doesn't matched"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=user)
                u.set_password(p)
                u.save()
                context['success']=" Create User Successfully"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User Already Exists"
                return render(request,'register.html',context)

def payment(request):
    context={}
    client = razorpay.Client(auth=("rzp_test_5RiEtwiMNJjvhL", "omBcOxXpm3kPsVvZ3hBpQ15Q"))
    #print(client)
    o=Orders.objects.filter(uid=request.user.id)
    oid=str(o[0].order_id)
    s=0
    for y in o:
        s=s+(y.qty*y.pid.price)
    print("Order id:",oid)
    print("Total:",s)
    s=s*100
    data = { "amount": s, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context['payment']=payment
    context['Data']=o

    print(payment)
    return render(request,'payment.html',context)

def place_order(request):
    context={}
    c=Cart.objects.filter(uid=request.user.id)
    oid=random.randrange(1000,9999)
    i=len(c)
    print("order Id",oid)
    s=0
    for x in c:
            o=Orders.objects.create(order_id=oid,uid=x.uid,pid=x.pid,qty=x.qty)
            o.save()
            s=s+(x.qty*x.pid.price)
            x.delete()
    
    context['cdata']=c
    context['total']=s
    context['items']=i

    return render(request,'order.html',context)
        
def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def addcart(request,rid):
    context={}
    print(request.user.id)
    if request.user.id:
        p=Product.objects.filter(id=rid)
        u=User.objects.filter(id=request.user.id)
        q1=Q(pid=p[0])
        q2=Q(uid=u[0])
        res=Cart.objects.filter(q1 & q2)
        #print('Response',res)
        if res:
            context['dup']="Product Already Added !!!"
            context['products']=p
            return render(request,'details.html',context)
        else:
            
            #print(u)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['products']=p
            context['success']="product Added Successfully in Cart!!!"
            return render(request,'details.html',context)
    else:
        return redirect('/login')
    

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=1)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['Products']=p
    return render(request,'index.html',context)

def pricerange(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=1)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['Products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv == '1':
        para='-price'
        
    else:
        para='price'
    
    p=Product.objects.order_by(para).filter(is_active=1)
    context={}
    context['Products']=p
    return render(request,'index.html',context)

def user_logout(request):
    logout(request)
    return redirect('/index')

def viewcart(request):
    context={}
    if request.user.is_authenticated:
        c=Cart.objects.filter(uid=request.user.id)
        i=len(c)
        s=0
        for x in c:
            s=s+(x.qty*x.pid.price)
            print("Summation or Total:",s)
        context['total']=s
        context['cdata']=c
        context['items']=i
        return render(request,'cart.html',context)
    else:
        return redirect('/login')
    
def removecart(request,rid):
    c=Cart.objects.filter(id=rid)
    c.delete()
    return redirect('/cart')

def cartqty(request,sig,pid):
    q1=Q(uid=request.user.id)
    q2=Q(pid=pid)
    c=Cart.objects.filter(q1 & q2)
    print(c)
    qty=c[0].qty
    if sig == '0':
        if qty>1:
            qty=qty-1
            c.update(qty=qty)
    else:
        qty=qty+1
    c.update(qty=qty)

    return redirect("/cart")

def sendmail(request):
    pid=request.GET['p1']
    oid=request.GET['p2']
    sign=request.GET['p3']
    rec_email=request.user.email

    #print("payment Id:",pid)
    #print("Order Id:",oid)
    #print("Signature",sign)
    msg="Your Order Had Been Placed Successfully. Your Order Tracking Id:"+oid
    send_mail(
    "Ekart Order Status",
    msg,
    "sauravnegi445@gmail.com",
    [rec_email],
    fail_silently=False,
    )

    return HttpResponse("Email Send")





        

