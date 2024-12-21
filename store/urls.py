from django.urls import path
from. import views
urlpatterns=[
    path("",views.home,name="home"),#defined a url path to home page
    path("about/",views.about,name="about"),#defined a url path to about page
    path("login/",views.login_user,name="login"),#defined a url path to login
    path("logout/",views.logout_user,name="logout"),#defined a url path to logout
    path("register/",views.register_user,name="register"),#defined a url path to register as new user
    path("add/",views.add_product,name="add_product"),#defined a url path to add products
    path("edit/<int:pk>",views.edit_product,name="edit_product"),#defined a url path to edit products
    path("delete/<int:pk>",views.delete_product,name="delete_product"),#defined a url path to delete products
    path("product/<int:pk>",views.product,name="product"),#defining product page
    path('product_list/',views.product_list,name='product_list'),
    path("category/<str:foo>",views.category,name="category"),#defining category page
    path("cart/",views.cart_details,name="cart_details"),#defining cart summary
    path("add_to_cart/<pk>",views.add_to_cart,name="add_to_cart"),# to add a product to the cart directory
    path("remove_from_cart/<int:pk>",views.remove_from_cart,name="remove_from_cart")#to remove a product from the cart
   
]