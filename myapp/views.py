from django.shortcuts import render,redirect
from django.db import connection
from django.contrib import messages
import os
from django.conf import settings

# Create your views here.
# client views

def home(request):
    return render(request,"client/home.html")

def login(request):
    if "clientuser" in request.session:
        return redirect("home")
    if request.method == 'POST':
        email=request.POST.get("email")
        pswd=request.POST.get("pswd")
        with connection.cursor() as cursor:
            query="select * from register where email=%s and password=%s"
            cursor.execute(query,[email,pswd])
            data=cursor.fetchone()
            if data:
                messages.success(request,f"Welcome {email}, you logged in successfully!")
                request.session["clientuser"]= data[1]
                return redirect("home")
            
            else:

                return redirect("register")

    return render(request,"client/login.html")

def register(request):
    if request.method == "POST":
        nm=request.POST.get('name')
        cno=request.POST.get('cno')
        email=request.POST.get('email')
        pswd=request.POST.get('pswd')
        with connection.cursor() as cursor:
            query="insert into register(name,contact,email,password) values(%s,%s,%s,%s)"
            cursor.execute(query,[nm,cno,email,pswd])
            return redirect("login")
    return render(request,"client/register.html")

def shop(request):
    with connection.cursor() as cursor:
        query="select * from products"
        cursor.execute(query)
        data=cursor.fetchall()
        datalist =[ 
            {
            "id":rows[0],
            "title":rows[1],
            "description":rows[2],
            "price":rows[3],
            "image":rows[4]
           } for rows in data
        ]
    return render(request,"client/shop.html", {"product":datalist})


def cart(request):
    if "clientuser" not in request.session:
        return redirect("login")
    username=request.session.get("clientuser")
    
    
    with connection.cursor() as cursor:
     query="select * from cart where username=%s"
     cursor.execute(query,[username])
     rows=cursor.fetchall()
     products = []
     for r in rows:
            products.append({
                "id": r[0],
                "pid":r[1],
                "title": r[2],
                "description": r[3],
                "price": r[4],
                "image": r[5]
            })

    total=0
    item=0
    for i in products:
        total=total+int(i["price"])
        item=item+1
    return render(request,"client/cart.html",{"product":products,"totals":total,"items":item})   


def remove(request,id):
    with connection.cursor() as cursor:
        query="delete from cart where id=%s"
        cursor.execute(query,[id])
        messages.success(request,"product removed")


        return redirect("cart")
def contact(request):
    if request.method == 'POST':
        nm=request.POST.get("name")
        email=request.POST.get("email")
        sub=request.POST.get("subject")
        msg=request.POST.get("message")

        with connection.cursor() as cursor:
            query="insert into contact(name,email,subject,message) values(%s,%s,%s,%s)"
            cursor.execute(query,[nm,email,sub,msg])

            return redirect("home")

    return render(request,"client/contact.html")

def about(request):
    return render(request,"client/about.html")

def checkout(request):
    username=request.session.get("clientuser")
    if request.method == "POST":
        name=request.POST.get("name")
        mob=request.POST.get("mobile")
        city=request.POST.get("city")
        state=request.POST.get("state")
        dis=request.POST.get("district")

        pin=request.POST.get("pin")

        with connection.cursor() as cursor:
            query="insert into address(name,mobile,city,state,district,pin) values(%s,%s,%s,%s,%s,%s)"

            selectcart="select * from cart where username=%s"
            cursor.execute(selectcart,[username])
            cart_data=cursor.fetchall()
            cart_list=[
                {
                    "id":row[0],
                     "pid":row[1],
                      "title":row[2],
                       "discription":row[3],
                        "price":row[4],
                         "image":row[5]
                }for row in cart_data
            ]
            insert_order="insert into orders(pid,title,discription,price,image,username) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(insert_order,[cart_list[0]["pid"],cart_list[0]["title"],cart_list[0]["discription"],cart_list[0]["price"],cart_list[0]["image"],username])
            cursor.execute(query,[name,mob,city,state,dis,pin])

            query="delete from cart where username=%s"
            cursor.execute(query,[username])
            messages.success(request,"order placed")
            return redirect("home")

    else:
        with connection.cursor() as cursor:
            sql = "select * from address where name=%s"
            cursor.execute(sql, [username])
            datas = cursor.fetchone()

            if datas:
                data_list = {
                    "id": datas[0],
                    "name": datas[1],
                    "mobile": datas[2],
                    "district": datas[3],
                    "city": datas[4],
                    "state": datas[5],
                    "pin": datas[6]
                }
                return render(request, "client/checkout.html", {"data": data_list,"nm":username})
            else:
                # No address found, return template with empty or default data
                messages.info(request, "No saved address found. Please enter your details.")
                return render(request, "client/checkout.html", {"data": {},"nm":username})

        return render(request,"client/checkout.html", {"data":data_list,"nm":username})



def oneproduct(request,id):
     username=request.session.get("clientuser")
     with connection.cursor() as cursor:
        query="select * from products where id=%s"
        cursor.execute(query,[id])
        data=cursor.fetchone()
        record={
                "id":data[0],
                "title":data[1],
                "description":data[2],
                "price":data[3],
                "image":data[4]
            }
        
        if request.method== 'POST':
            with connection.cursor() as cursor:
                query="insert into cart(pid,title,price,description,image,username) values(%s,%s,%s,%s,%s,%s)"
                cursor.execute(query,[record["id"],record["title"],record["price"],record["description"],record["image"],username])
                messages.success(request,"product added in cart")

                return redirect("cart")
            
            
        
     return render(request,"client/oneproduct.html", {"product":record})
  


def clogout(request):
    if "clientuser" in request.session:
        request.session.flush()
        messages.success(request,"logout successfully")
        return redirect("login")





# Admin views

def alogin(request):
    if "adminuser" in request.session:
        return redirect("products")
    
    if request.method == 'POST':
        email=request.POST.get("email")
        pswd=request.POST.get("pswd")
        with connection.cursor() as cursor:
            query="select * from admin where email=%s and password=%s"
            cursor.execute(query,[email,pswd])
            data=cursor.fetchone()
            if data:
                messages.success(request,f"Welcome {email}, you logged in successfully!")
                request.session["adminuser"]= data[1]
                return redirect("products")
                
            
            else:
                return redirect("alogin")


    return render(request,"admin/alogin.html")


def products(request):
    if "adminuser" not in request.session:
        return redirect("alogin")
    
    if request.method == "POST":
        title=request.POST.get("title")
        des=request.POST.get("description")
        price=request.POST.get("price")
        img=request.FILES.get("image")
        if img:
            image_path=os.path.join(settings.MEDIA_ROOT,"products",img.name)
            os.makedirs(os.path.dirname(image_path),exist_ok=True)
            with open(image_path,"wb") as f:
                for chunk in img.chunks():
                    f.write(chunk)

            image_r_p="/myapp/static/images/products/"+img.name

        with connection.cursor() as cursor:
            query="insert into products(title,description,price,image) values(%s,%s,%s,%s)"
            cursor.execute(query,[title,des,price,image_r_p])
            messages.success(request,"product successfully added")


    return render(request,"admin/products.html")

def logout(request):
    if "adminuser" in request.session:
        
        request.session.flush()
        messages.success(request,"logout successfully")
        return redirect("alogin")
    

def viewproduct(request):
    with connection.cursor() as cursor:
        query="select * from products"
        cursor.execute(query)
        data=cursor.fetchall()
        datalist =[ 
            {
            "id":rows[0],
            "title":rows[1],
            "description":rows[2],
            "price":rows[3],
            "image":rows[4]
           } for rows in data
        ]
    return render(request,"admin/viewproduct.html",{"products":datalist})


def vieworders(request):
    with connection.cursor() as cursor:
        query="select id,title,discription,price,image,username from orders"
        cursor.execute(query)
        data=cursor.fetchall()
        data_list=[
            {
            "id":rows[0],
            "title":rows[1],
            "description":rows[2],
            "price":rows[3],
            "image":rows[4],
            "username":rows[5]
        }for rows in data
        ]
    return render(request,"admin/vieworders.html",{"products":data_list})

def viewaddress(request,name):
    with connection.cursor() as cursor:
        query="select * from address where name=%s"
        cursor.execute(query,[name])
        data=cursor.fetchone()
    return render(request,"admin/viewaddress.html",{"address":data})
        
        


def viewusers(request):
    with connection.cursor() as cursor:
        query="select * from register"
        cursor.execute(query)
        data=cursor.fetchall()
        data_list=[
            {
                "id":rows[0],
                "name":rows[1],
                "contact":rows[2],
                "email":rows[3],
                "password":rows[4]
           }for rows in data
        ]
    return render(request,"admin/viewusers.html", {"users":data_list})

def report(request):
    with connection.cursor() as cursor:
        query="select * from contact"
        cursor.execute(query)
        data=cursor.fetchall()
        data_list=[
            {
                "id":rows[0],
                "name":rows[1],
                "email":rows[2],
                "subject":rows[3],
                "message":rows[4]
            }for rows in data
        ]
    return render(request,"admin/report.html", {"reports":data_list})
def delete(request,id):
   with connection.cursor() as cursor:
       query="delete from products where id=%s"
       cursor.execute(query,[id])
       messages.success(request,"record deleted succesfully")
       return redirect("viewproduct")
   
def update(request,id):
    if request.method=="POST":
        title=request.POST.get("title")
        des=request.POST.get("description")
        price=request.POST.get("price")
        img=request.FILES.get("image")
        if img:
            image_path=os.path.join(settings.MEDIA_ROOT,"products",img.name)
            os.makedirs(os.path.dirname(image_path),exist_ok=True)
            with open(image_path,"wb") as f:
                for chunk in img.chunks():
                    f.write(chunk)

            image_r_p="/myapp/static/images/products/"+img.name

            with connection.cursor() as cursor:
                query="update products set title=%s,description=%s,price=%s,image=%s where id=%s"
                cursor.execute(query,[title,des,price,image_r_p,id])
                messages.success(request,"record ")

            return redirect("viewproduct")
        
        else:
              with connection.cursor() as cursor:
                query="update products set title=%s,description=%s,price=%s where id=%s"
                cursor.execute(query,[title,des,price,id])

              return redirect("viewproduct")

    with connection.cursor() as cursor:
        query="select * from products where id=%s"
        cursor.execute(query,[id])
        data=cursor.fetchone()
        record={
                "id":data[0],
                "title":data[1],
                "description":data[2],
                "price":data[3],
                "image":data[4]
            }
        
        return render(request,"admin/updateproduct.html", {"record":record})

