from django.db import models
import datetime
from django.contrib.auth.models import User

#category of products
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
#product details table    
class Product(models.Model):
    product_name=models.CharField(max_length=200)
    product_price=models.DecimalField(max_digits=8,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    product_description=models.TextField(default="",blank=True,null=True)
    product_image=models.ImageField(upload_to="uploads/",default="uploads/sample.png")

    def __str__(self):
        return self.product_name

#customer details
class Customer(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=250)
    phone_number=models.CharField(max_length=10)
    password=models.CharField(max_length=25)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
#order item details(items that are to be carted by the users who logged in)
class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    ordered=models.BooleanField(default=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"
    def get_total_item_price(self):
        return self.quantity*self.product.product_price
    def get_final_price(self):
        return self.get_total_item_price()

  #order details(ordered by which user and which items)  
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField(auto_now=True)
    ordered=models.BooleanField(default=False)

    def __str__(self):
        
        if self.user:
            return self.user.username
        return "Anonymous Order"  
    def get_total_price(self):
        return sum(item.get_total_item_price() for item in self.items.all())

    
    
    

