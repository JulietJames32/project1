from django.test import TestCase
from django.urls import reverse,resolve
from store.models import Product,Category,Order,OrderItem
from django.contrib.auth.models import User


class TestUrls(TestCase):
    def test_home(self):
        response=self.client.get('/')
        print(response)
        self.assertEqual(response.status_code,200)
    def test_about_page(self):
        response=self.client.get('/about/')
        self.assertEqual(response.status_code,200)    
    def test_login_page(self):
        response=self.client.get('/login/')
        self.assertEqual(response.status_code,200)   

    def test_logout_page(self):
        self.client.login(username="julietjames",password="12345")
        response=self.client.get('/logout/')

        '''here expecting status code is 302 which is for redirection to another page.
           To perform logout we should have to be already logged in and if user is not
           logged in ,it will redirect to login page'''
        
        self.assertEqual(response.status_code,302) 

    def test_register_page(self):
        response=self.client.get('/register/')
        self.assertEqual(response.status_code,200)  

   
    def test_addproduct_page(self):    
        response=self.client.get('/add/')
        self.assertEqual(response.status_code,200)   
    
    def test_editproduct_page(self):    
        response=self.client.get('/edit/')
        self.assertEqual(response.status_code,200)   
       
    def test_deleteproduct_page(self):    
        response=self.client.get('/delete/')
        self.assertEqual(response.status_code,200)  

    def test_product_page(self):   
        category=Category.objects.create(name="Branded")
        product=Product.objects.create(product_name='shoes',product_price='1000',product_description="ghjas",category=category) 
        
        '''product page has the foregin key of category so we should create a 
           test for  product with a valid category with correct product id.
           The reverse () function dynamically generate the URL based on the 
           view's name in URL pattern and parameter passed to it'''
        
        response=self.client.get(reverse('product',args=[product.pk]))
        self.assertEqual(response.status_code,200)          
    def test_category_page(self):
        category=Category.objects.create(name='Books')
        response=self.client.get(reverse('category',args=["Books"]))
        self.assertEqual(response.status_code,200)    

    def test_cart_page(self):

        '''Here user need to be logged in,then only user can view his cart
           details,so if not logged in ,page will redirect to login page 
           and then to cart details,it is must to be logged in.We created a
           test user and test password and logged in then it will be redirected
           to original page'''
        
        user=User.objects.create_user(username='username',password='password')
        self.client.login(username='username',password='password')
        response=self.client.get(reverse('cart_details'))
        self.assertEqual(response.status_code,200)    
    def test_addtocart_page(self):

        '''1. created a category and product
           2. login is required in its view.so a test user and password created
           3. made a POST request to add the product to cart
           4. it will bw redirected to the cart details page(302 check for redirection)
           5. verifying that the order is added to the cart'''
        
        category=Category.objects.create(name="Branded")
        product=Product.objects.create(product_name='shoes',product_price='1000',product_description="ghjas",category=category)
        user=User.objects.create_user(username='username',password='password')
        self.client.login(username='username',password='password')
        response=self.client.get(reverse('add_to_cart',args=[product.pk]))
        self.assertEqual(response.status_code,302) 
        order_item=OrderItem.objects.filter(product=product,user=user,ordered=False).exists()
        self.assertTrue(order_item)  
    def test_removefromcart_page(self):
        '''1. Here  login required in the view,test user and password is created
           2. product and category created
           3. creating an order and cart item
           4. testing of removal
           5. checking credirction to cart_details page'''
        category=Category.objects.create(name="Branded")
        product=Product.objects.create(product_name='shoes',product_price='1000',product_description="ghjas",category=category)

        user=User.objects.create_user(username='username',password='password')
        self.client.login(username='username',password='password')
        #Dummy order is placing
        order=Order.objects.create(user=user,ordered=False)
        order_item=OrderItem.objects.create(product=product,user=user,ordered=False)
        order.items.add(order_item)
        #checking for redirection to cart details page
        response=self.client.get(reverse('remove_from_cart',args=[product.pk]))
        self.assertEqual(response.status_code,302) 
        #verifying that order item is removed
        order_item_exists=OrderItem.objects.filter(product=product,user=user,ordered=False).exists()
        self.assertFalse(order_item_exists)  
