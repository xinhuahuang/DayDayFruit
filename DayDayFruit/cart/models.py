from django.db import models


# Create your models here.
class CartInfo(models.Model):
    user = models.ForeignKey('Users.Users')
    good = models.ForeignKey('df_goods.GoodsInfo')
    count = models.IntegerField(default=1)
    is_buy = models.IntegerField(default=0)