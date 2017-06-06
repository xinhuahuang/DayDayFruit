from django.db import models


# Create your models here.
class Users(models.Model):
    uname = models.CharField(max_length=20)
    pword = models.CharField(max_length=40)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=100, default='')
    contact = models.CharField(max_length=20, default='')
    postcode = models.CharField(max_length=6, default='')

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.uname


class VisitInfo(models.Model):
    vpic = models.CharField(max_length=50)
    vtitle = models.CharField(max_length=20)
    vprice = models.DecimalField(max_digits=5, decimal_places=2)
    vunit = models.CharField(max_length=20,default='500g')
    vclick = models.IntegerField(default=1)
    vtype = models.IntegerField(default=1)
    vindex = models.IntegerField(default=1)
    vusers = models.ForeignKey(Users)

    class Meta:
        db_table = 'VisitInfo'

    def __str__(self):
        return self.vtitle