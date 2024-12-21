from django import forms
from.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .tasks import send_review_email_task
 
class  UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)
    class Meta:  #User table which is imported is fetched(data of User)
        model=User
        fields= ['username','email','password1','password2']
        labels= {

            'username':'Username',
            'email':'Email Address',
            'password1':'Password',
            'password2':'Confirm password',

        }
class Product_Form(forms.ModelForm):  #form is created to add edit and delete products 
    class Meta: #product table from model class is fetched here
        model=Product
        fields=['product_name','product_price','category','product_description','product_image']


class ReviewForm(forms.Form):
    name=forms.CharField(label='firstname',min_length=4,max_length=50,widget=forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'firstname','id':'form-firstname'}))
    
    email=forms.EmailField(label='Email Address',max_length=200,widget=forms.TextInput(attrs={'class':'form contrl mb-3','placeholder':'email','id':'form-email'}))
    review=forms.CharField(label='review',widget=forms.Textarea(attrs={'class':'form-control','rows':'3'}))

    def send_email(self):
        send_review_email_task.delay(
            name=self.cleaned_data['name'],
            
            email=self.cleaned_data['email'],
            review=self.cleaned_data['review']
        )        