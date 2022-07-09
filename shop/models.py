from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    publish_date = models.DateField()
    img = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key="TRUE")
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=50, default="")
    number = models.CharField(max_length=50, default="")
    query = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key="True")
    items_json = models.CharField(max_length=50000)
    fname = models.CharField(max_length=50, default="")
    sname = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=1000, default="")
    number = models.CharField(max_length=1000, default="")
    address1 = models.CharField(max_length=1000, default="")
    city = models.CharField(max_length=1000, default="")
    state = models.CharField(max_length=1000, default="")
    zipcode = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.fname


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key='True')
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timeestamp = models.DateField(auto_now_add="TRUE")

    def __str__(self):
        return self.update_desc[0:7]
