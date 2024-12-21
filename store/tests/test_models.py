from django.test import TestCase
from django . contrib.auth.models import User
#importing all model tables from models
from store.models import Product
from store.models import Category
from store.models import Customer
from store.models import OrderItem
from store.models import Order
#Testing Product Table
class TestProductModels(TestCase):
    def setUp(self):
        # Create a Category instance so the Product can use it,cartegory is a foreign key used
        #product model has a foreign key from category model we have to maintain that relationship here also
        self.category = Category.objects.create(name="Books")
       
    
    def test_product_models(self):
        product1=Product.objects.create(product_name='Poetry killer',product_price="250",category=self.category)
        self.assertEqual(str(product1.product_name),'Poetry killer')
        self.assertEqual(str(product1.product_price),'250')
        self.assertEqual(str(product1.category),'Books')
        self.assertTrue(isinstance(product1,Product))

#Testing Category Table
class TestCategoryModels(TestCase):
    
    def  test_category_models(self):
       category1=Category.objects.create(name="Branded")
       self.assertEqual(str(category1),'Branded')
       self.assertTrue(isinstance(category1,Category))

#Testing Customer Table
class TestCustomerModels(TestCase):

    def test_customer_models(self):
        profile=Customer.objects.create(first_name="Juliet",last_name="James",email="abdcd@yahoo.com",password="1234",phone_number=963258)
        #Testing each field str representation individually
        self.assertEqual(str(profile.first_name),'Juliet')
        self.assertEqual(str(profile.last_name),'James')
        self.assertEqual(str(profile.email),'abdcd@yahoo.com')
        self.assertEqual(str(profile.password),'1234')
        self.assertEqual(str(profile.phone_number),'963258')
        self.assertTrue(isinstance(profile,Customer))


#Testing CartItem Table
class TestOrderItemModels(TestCase):
    def setUp(self) :
        self.user=User.objects.create(username='julietjames')
        self.category=Category.objects.create(name="Books")
        self.ordered='True'
        self.product=Product.objects.create(product_name='BECOMING',product_price=500,category=self.category)
        self.order_item=OrderItem.objects.create(user=self.user,product=self.product,quantity=2,ordered=self.ordered)

    def test_orderitem_model(self):
        #Testing each field str representation individually
        self.assertEqual(str(self.order_item.user.username),'julietjames')
        self.assertEqual(str(self.order_item.ordered),'True')
        self.assertEqual(str(self.order_item.product),'BECOMING')
        self.assertEqual(str(self.order_item.quantity),'2')
        self.assertEqual(str(self.product.category),'Books')
        self.assertTrue(isinstance(self.order_item,OrderItem))
        
    def test_get_total_item_price(self):
        total_price = self.order_item.get_total_item_price()
        self.assertEqual(total_price, 1000)  # (2 * 500=1000)  
   
#Testing Cart Table
class TestOrderModels(TestCase):  
    def setUp(self):
        self.user=User.objects.create(username='julietjames',password='1234')
        self.category=Category.objects.create(name="Books")
        self.product=Product.objects.create(product_name='BECOMING',product_price=500,category=self.category)
        self.order_item=OrderItem.objects.create(user=self.user,product=self.product,quantity=4)
        self.order=Order.objects.create(user=self.user,ordered=True)

        #used to associate an Orderitem with Order in Djangos ORM,We have a many to many field for OrderItem
        #Adding specific orderitem instance to the list in the Order's  items field
        self.order.items.add(self.order_item) 

    def test_order_model(self):
        self.assertEqual(str(self.order.user.username),'julietjames') 
        self.assertEqual(str(self.order.ordered),'True') 
        self.assertEqual(str(self.order),'julietjames')
        self.assertTrue(isinstance(self.order,Order))
    #price calculation   
    def test_get_total_price(self):
        total_price = self.order.get_total_price()
        self.assertEqual(total_price, 2000)  # 2 * 500=1000   