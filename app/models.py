from django.db import models

# Create your models here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255) 
    # Add other fields for the Category model if needed

    def __str__(self):
        return self.title

class MenAndWomen(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    image = models.ImageField(upload_to='men_and_women_images/')  # Assuming you want to upload images
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Storing hashed password is recommended in a real application
    def __str__(self):
        return self.email

class cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default='')
    quantity = models.IntegerField(default=0)
    price = models.CharField(max_length=255,default='')
    image = models.ImageField(upload_to='cart/',null=True,blank=True)

class payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=255,default='')
    total_price = models.IntegerField(default=0)






