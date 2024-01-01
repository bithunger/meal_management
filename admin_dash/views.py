from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout
from admin_dash.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from admin_dash.models import User, Meal, Daily_Bazar, Daily_Meal, Partial_Meal
import datetime as dateTime
from user_dash import views
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from datetime import datetime


# create meal for all in every day
@admin_required
def create_meal(request):
    today = dateTime.date.today()
    tomorrow = today + dateTime.timedelta(days=1)
    day = today.strftime('%A')
    next_day = tomorrow.strftime('%A')
    
    users = User.objects.filter(status=True)
    status = 0
    for user in users:
        # check meal was created for tomorrow or not
        if Daily_Meal.objects.filter(date=tomorrow, user=user).exists() is False:
            partial = Partial_Meal.objects.filter(user=user)
            dm = Daily_Meal.objects.filter(user=user, date=today).first()
            if partial:
                print('with-per')
                found_day = [item.meal for item in partial if item.day==day]
                found_next_day = [item for item in partial if item.day==next_day and item.meal==1]
                
                if found_day:
                    print('with-per-found-day', found_day)
                    if found_day==[0]:
                        print('with-per-found-day-0')
                        if dm:
                            print('with-per-found-day-0-dm')
                            dm.dinner = 0
                            dm.save()
                        else:
                            print('with-per-found-day-0-dm-else')
                            Daily_Meal.objects.create(user=user, date=today, lunch=1, dinner=0)
                    elif found_day==[1]:
                        print('with-per-found-day-1')
                        if dm:
                            print('with-per-found-day-1-dm')
                            dm.dinner = 1
                            dm.save()
                        else:
                            print('with-per-found-day-1-dm-else')
                            Daily_Meal.objects.create(user=user, date=today, lunch=0, dinner=1)
                    else:
                        Daily_Meal.objects.create(user=user, date=today, lunch=0, dinner=0)
                else:
                    if dm:
                        print('with-per-not-found-day-dm')
                        dm.dinner = 1
                        dm.save()
                            # Daily_Meal.objects.create(user=user, date=tomorrow, lunch=1, dinner=-1)
                    else:
                        print('with-per-not-found-day-dm-else')
                        Daily_Meal.objects.create(user=user, date=today, lunch=1, dinner=1)
                        
                if found_next_day:
                    print('with-per-not-found-next-day-1')
                    Daily_Meal.objects.create(user=user, date=tomorrow, lunch=0, dinner=-1)
                else:
                    print('with-per-found-next-day-else')
                    Daily_Meal.objects.create(user=user, date=tomorrow, lunch=1, dinner=-1)             
            else:
                print('without-per')
                if dm:
                    print('without-per-dn')
                    dm.dinner = 1
                    dm.save()
                    Daily_Meal.objects.create(user=user, date=tomorrow, lunch=1, dinner=-1)
                else:
                    print('without-per-else')
                    Daily_Meal.objects.create(user=user, date=today, lunch=1, dinner=1)
                    Daily_Meal.objects.create(user=user, date=tomorrow, lunch=1, dinner=-1)
        else:
            status+=1
    if len(users)==status:
        messages.error(request, 'Meal already given in this date')
    else: messages.success(request, 'Meal created successfully for all')
    
    # add meal model or update
    meal_update(request)
    
    return redirect('total-meal')


# admin dashboard
@admin_required
def admin_dashboard(request):
    this_month = dateTime.date.today().month
    month = dateTime.date(1900, this_month, 1).strftime('%B')
    year = datetime.now().year
    
    distinct_users = Daily_Meal.objects.filter(date__month=this_month).distinct().count()
    
    user_total_meal = views.user_monthly_total_meal(request, this_month)
    user_total_bazar = views.user_monthly_total_bazar(request, this_month)
    
    total_meal = views.monthly_total_meal(this_month)
    total_bazar = views.monthly_total_bazar(this_month)
    
    m_rate = 0
    if total_meal:
        m_rate = views.meal_rate(total_meal, total_bazar)
    
    m_cost = views.my_cost(user_total_meal, m_rate)
    paid = m_cost-user_total_bazar
    
    context = {
        'user_total_meal':user_total_meal, 
        'user_total_bazar':user_total_bazar,
        'total_meal':total_meal, 
        'total_bazar':total_bazar,
        'meal_rate':round(m_rate, 7),
        'my_cost':m_cost,
        'month':month,
        'year':year,
        'paid':paid,
        'distinct_users':distinct_users
    }
    return render(request, 'admin_dashboard/index.html', context)


# add meal model or update
@admin_required
def meal_update(request):
    this_month = dateTime.date.today().month
    month = dateTime.date(1900, this_month, 1).strftime('%B')
    
    total_meal = views.monthly_total_meal(this_month)
    total_bazar = views.monthly_total_bazar(this_month)
    
    meal_rate = 0
    if total_meal:
        meal_rate = round(views.meal_rate(total_meal, total_bazar), 7)

    distinct_users = Daily_Meal.objects.filter(date__month=this_month).distinct().count()
    
    meal = Meal.objects.filter(month=month).first()
    # meal = Meal.objects.filter(date__month=this_month).first()
    if meal:
        meal.total_meal = total_meal
        meal.total_bazar = total_bazar
        meal.meal_rate = meal_rate
        meal.total_mate = distinct_users
        meal.save()
    else:
        meal = Meal.objects.create(month=month, total_meal=total_meal, total_bazar=total_bazar, meal_rate=meal_rate, total_mate=distinct_users)

    return meal