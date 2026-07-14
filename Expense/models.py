# Create your models here.
from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [

    ('Food', 'Food'),

    ('Shopping', 'Shopping'),

    ('Travel', 'Travel'),

    ('Bills', 'Bills'),

    ('Education', 'Education'),

    ('Health', 'Health'),

    ('Entertainment', 'Entertainment'),

    ('Transport', 'Transport'),

    ('Others', 'Others'),

]



class Expense(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=20,choices=CATEGORY_CHOICES,default='others')
    date=models.DateField()
    description=models.TextField(blank=True,null=True)

def __str__(self):
        return self.title
   