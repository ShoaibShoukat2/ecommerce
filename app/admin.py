from django.contrib import admin
from .models import MenAndWomen,Category,User,cart,payment
# Register your models here.

class MW(admin.ModelAdmin):
    list_display = ('id','title','price','image','category')

admin.site.register(MenAndWomen,MW)

class CatAdmin(admin.ModelAdmin):
    list_display = ('id','title')

admin.site.register(Category,CatAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','name','password')

admin.site.register(User,UserAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user','title','quantity','price','image')
    


admin.site.register(cart,CartAdmin)

class Paymentadmin(admin.ModelAdmin):
    list_display = ('id','user','total_price')


admin.site.register(payment,Paymentadmin)