from django.db import models


# Create your models here.
class Accounts(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="アカウント番号")
    last_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="姓")
    first_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="名")
    birthday = models.DateTimeField()
    mailaddress = models.EmailField()
    
    

class Address(models.Model):
    zip_code = models.CharField(
        verbose_name='郵便番号',max_length=8,blank=True,
    )
    address_pref = models.CharField(
        verbose_name='都道府県',max_length=40,blank=True,
    )
    address_city = models.CharField(
        verbose_name='市区町村番地',max_length=40,blank=True,
    )
    address_buill = models.CharField(
        verbose_name='建物名',max_length=40,blank=True,
    )