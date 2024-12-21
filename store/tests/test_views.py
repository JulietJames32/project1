from django.test import TestCase,Client
from django.urls import reverse,resolve
from store.models import Category,Product,Order,OrderItem,Customer
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from store.forms import UserRegistrationForm
class Testviewshome(TestCase):
    def setUp(self):
        #creating test category,test product,test,user,and a dummy order is placed
        self.category=Category.objects.create(name='branded')
        self.product=Product.objects.create(product_name='shoes',product_price=100,category=self.category)
        self.user=User.objects.create_user(username='username',password='password')
        self.order=Order.objects.create(user=self.user)
        #urls for the testing are initiated here
        self.client=Client()
        self.home=reverse('home')
        self.about=reverse('about')
        self.login=reverse('login')
        self.logout=reverse('logout')
        self.register=reverse('register')
        self.cart=reverse('cart_details')
        self.add_to_cart=reverse('add_to_cart',kwargs={'pk':self.product.pk})
        self.remove_from_cart=reverse('remove_from_cart',kwargs={'pk':self.product.pk})

    #testing each views in views.py    
    def testhomeview(self):
        response=self.client.get(self.home)
        self.assertEquals(response.status_code,200)  
        self.assertTemplateUsed(response,'home.html')

    def testaboutview(self):
        response=self.client.get(self.about)
        self.assertEquals(response.status_code,200)  
        self.assertTemplateUsed(response,'about.html')  

    def testproductview(self):
        response=self.client.get(reverse('product',args=[self.product.pk]))
        self.assertEquals(response.status_code,200)  
        self.assertTemplateUsed(response,'product.html')   

    def testcategoryview(self):
        response=self.client.get(reverse('category',args=[self.category.name.replace(' ', '-')]))
        self.assertEquals(response.status_code,200)  
        self.assertTemplateUsed(response,'category.html')

    def testlogin_userview(self):
        response=self.client.post(self.login,{'username':'username','password':'password'})
        self.assertRedirects(response,self.home)

    def testlogout_userview(self):
        #logging in first
        self.client.login(username='username',password='password')
        response=self.client.get(self.logout)
        self.assertRedirects(response,self.home)

    def testregister_userview(self):
        response=self.client.get(self.register)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html') 
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

    def test_cart_details_view(self):
        self.client.login(username='username', password='password')
        response = self.client.get(self.cart)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html') 

    def testadd_to_cartview(self):
        # Login first
        self.client.login(username='username', password='password')
        response = self.client.get(self.add_to_cart)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,self.cart)
        #checking if the product is added to the cart
        order=Order.objects.get(user=self.user,ordered=False)
        self.assertTrue(order.items.filter(product=self.product).exists())
        
    def testremove_from_cartview(self):
        # Login first
        self.client.login(username='username', password='password')
        response = self.client.get(self.add_to_cart)
        #removing from cart
        response=self.client.get(self.remove_from_cart)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,self.cart)
        #checking the product is removed
        order = Order.objects.get(user=self.user, ordered=False)
        self.assertFalse(order.items.filter(product=self.product).exists())
    