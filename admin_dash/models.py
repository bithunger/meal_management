from django.contrib.auth.models import AbstractUser
from django.db import models
# from autoslug import AutoSlugField


class User(AbstractUser):
    mobile = models.CharField('Mobile', max_length=50)
    image = models.ImageField('Profile image', upload_to='user/profiles/')
    nid_or_birth = models.ImageField('NID or Birth', upload_to='user/nid/')
    address = models.TextField('Address', max_length=150)
    total_meal = models.IntegerField('Total meal', default=0)
    total_bazar = models.IntegerField('Total bazar', default=0)
    total_tk = models.IntegerField('Total taka', default=0)
    # slug = AutoSlugField(populate_from='username', unique=True)
    status = models.BooleanField('Status', default=True)
    
    
    
class Daily_Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # month = models.CharField('Month', max_length=50)
    date = models.DateField('Date (YYY-MM-DD)')
    lunch = models.IntegerField('Lunch', default=0)
    dinner = models.IntegerField('Dinner', default=0)
    comment = models.TextField('Comments', max_length=200)
    status = models.BooleanField('Status', default=True)
    
    def __str__(self):
        return self.user.username
    
    

class Daily_Bazar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # month = models.CharField('Month', max_length=50)
    date = models.DateField('Date (YYY-MM-DD)')
    bazar = models.IntegerField('Bazar')
    comment = models.TextField('Comments', max_length=500)
    status = models.BooleanField('Status', default=True)
    
    def __str__(self):
        return self.user.username



class Meal(models.Model):
    month = models.CharField('Month', max_length=50)
    total_meal = models.IntegerField('Total meal')
    meal_rate = models.IntegerField('Meal rate')
    total_bazar = models.IntegerField('Total bazar')
    total_mate = models.IntegerField('Total Mate')
    status = models.BooleanField('Status', default=True)
    
    def __str__(self):
        return self.month
    
    
class Partial_Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField('Day', max_length=20)
    meal = models.IntegerField('Meal')
    status = models.BooleanField('Status', default=True)