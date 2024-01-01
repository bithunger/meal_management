from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout
from admin_dash.models import User, Meal, Daily_Bazar, Daily_Meal, Partial_Meal
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
import datetime as dateTime
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from admin_dash import views



def user_monthly_total_meal(request, month):
    this_month_meal = Daily_Meal.objects.filter(user=request.user, date__month=month)
    total_meal = 0
    for item in this_month_meal:
        if item.dinner >= 0:
            total_meal += item.lunch + item.dinner
        else:
            total_meal += item.lunch
    return total_meal


def user_monthly_total_bazar(request, month):
    this_month_bazar = Daily_Bazar.objects.filter(user=request.user, date__month=month)
    total_bazar = 0
    for item in this_month_bazar:
        total_bazar += item.bazar
    return total_bazar


def monthly_total_meal(month):
    this_month_meal = Daily_Meal.objects.filter(date__month=month)
    total_meal = 0
    for item in this_month_meal:
        if item.dinner >= 0:
            total_meal += item.lunch + item.dinner
        else:
            total_meal += item.lunch
    return total_meal


def monthly_total_bazar(month):
    this_month_bazar = Daily_Bazar.objects.filter(date__month=month)
    total_bazar = 0
    for item in this_month_bazar:
        total_bazar += item.bazar
    return total_bazar


def meal_rate(meal, bazar):
    meal_rate = bazar / meal
    return meal_rate

def my_cost(meal, meal_rate):
    cost = meal*meal_rate
    return cost
    

@login_required
def dashboard(request):
    this_month = dateTime.date.today().month
    month = dateTime.date(1900, this_month, 1).strftime('%B')
    year = datetime.now().year
    
    distinct_users = Daily_Meal.objects.filter(date__month=this_month).distinct().count()
    
    user_total_meal = user_monthly_total_meal(request, this_month)
    user_total_bazar = user_monthly_total_bazar(request, this_month)
    
    total_meal = monthly_total_meal(this_month)
    total_bazar = monthly_total_bazar(this_month)
    
    m_rate = 0
    if total_meal:
        m_rate = meal_rate(total_meal, total_bazar)
    
    m_cost = my_cost(user_total_meal, m_rate)
    
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
   
        
    return render(request, 'user_dashboard/index.html', context)


@login_required
def manage_meal(request):
    today = dateTime.date.today()
    tomorrow = today + dateTime.timedelta(days=1)
    
    partial = Partial_Meal.objects.filter(user=request.user)
    
    return render(request, 'user_dashboard/add_meal.html', {'today':today, 'tomorrow':tomorrow, 'partial':partial})


@login_required
def add_or_off_meal(request):
    if request.POST:
        today = dateTime.date.today()
        tomorrow = today + dateTime.timedelta(days=1)
        
        extra_meal_dinner = request.POST.get('extra_meal_dinner') if request.POST.get('extra_meal_dinner') else 1
        extra_meal_lunch = request.POST.get('extra_meal_lunch') if request.POST.get('extra_meal_lunch') else 1
        
        off_dinner = 0 if request.POST.get('off_dinner') else 1
        off_lunch = 0 if request.POST.get('off_lunch') else 1
        
        today_comment = request.POST['today_comment']
        tomorrow_comment = request.POST['tomorrow_comment']
        
        off_from = request.POST.get('off_from')

        if extra_meal_dinner == extra_meal_lunch == off_dinner == off_lunch == 1 and (off_from == '0' or off_from is None):
            messages.error(request, 'Please update meal')
            return redirect('manage-meal')
        
        if Daily_Meal.objects.filter(date=tomorrow, user=request.user).exists() and off_from != '1':
            messages.error(request, 'Meal already given in this date')
            return redirect('manage-meal')
        elif off_from is not None and off_from != '0':
            user = User.objects.get(id=request.user.id)
            
            if off_from == '1':
                user.status = True
                user.save()
                messages.success(request, 'Meal on successfully')
            else:
                user.status = False
                user.save()
                
                if off_from == 'tomorrow':
                    Daily_Meal.objects.create(user=request.user, date=today, dinner=extra_meal_dinner)
                    Daily_Meal.objects.create(user=request.user, date=tomorrow, dinner=-1, comment=tomorrow_comment)
                else:
                    Daily_Meal.objects.create(user=request.user, date=today, comment=today_comment)
                    Daily_Meal.objects.create(user=request.user, date=tomorrow, dinner=-1)
                    
                messages.success(request, f'Meal off successfully from { off_from }')
                views.meal_update(request)
            return redirect('total-meal')
        else:
            if User.objects.get(id=request.user.id).status is not True:
                messages.error(request, 'Your meals are off, turn on it first')
                return redirect('manage-meal')
            # for today
            if Daily_Meal.objects.filter(date=today, user=request.user).exists():
                today_meal = Daily_Meal.objects.get(date=today)
                if off_dinner == 0:
                    today_meal.dinner = off_dinner
                    if today_meal.comment:
                        today_meal.comment += ' + '+today_comment
                    else: today_meal.comment = today_comment
                    today_meal.save()
                else:
                    today_meal.dinner = extra_meal_dinner
                    if today_meal.comment:
                        today_meal.comment += ' + '+today_comment
                    else: today_meal.comment = today_comment
                    today_meal.save()
            else:
                if off_dinner == 0:
                    Daily_Meal.objects.create(user=request.user, date=today, dinner=off_dinner, comment=today_comment)
                else:
                    Daily_Meal.objects.create(user=request.user, date=today, dinner=extra_meal_dinner, comment=today_comment)
            
            # for tomorrow
            if off_lunch == 0:
                Daily_Meal.objects.create(user=request.user, date=tomorrow, lunch=off_lunch, dinner=-1, comment=tomorrow_comment)
            else:
                Daily_Meal.objects.create(user=request.user, date=tomorrow, lunch=extra_meal_lunch, dinner=-1, comment=tomorrow_comment)

            views.meal_update(request)
            messages.success(request, 'Meal updated successfully')
            return redirect("total-meal")
        
    return redirect('total-meal')


@login_required
def partial_off_meal(request):
    partial_day_from = request.POST.get('partial_day_from')
    partial_off_dinner = True if request.POST.get('partial_off_dinner') else False
    partial_off_lunch = True if request.POST.get('partial_off_lunch') else False
    
    if partial_off_dinner:
        Partial_Meal.objects.create(user=request.user, day=partial_day_from, meal=0) # 0=dinner
    elif partial_off_lunch:
        Partial_Meal.objects.create(user=request.user, day=partial_day_from, meal=1) # 1=lunch
    
    messages.success(request, 'Partially meal of set')
    return redirect('manage-meal')


@login_required
def total_meal(request):
    this_month = dateTime.date.today().month
    month = dateTime.date(1900, this_month, 1).strftime('%B')
    this_month_meal = Daily_Meal.objects.filter(date__month=this_month, user=request.user)
    # this_month_meal = Daily_Meal.objects.filter(user=request.user)
    
    total_meal = 0
    for meal in this_month_meal:
        if meal.dinner >= 0:
            total_meal += meal.lunch + meal.dinner
        else:
            total_meal += meal.lunch
     
    return render(request, 'user_dashboard/total_meal.html', {'this_month_meal':this_month_meal, 'this_month':month, 'total_meal':total_meal})


@login_required
def add_bazar(request):
    today = dateTime.date.today()
    
    if request.POST:
        bazar = request.POST['bazar']
        bazar_list = request.POST['bazar_list']
        Daily_Bazar.objects.create(user=request.user, date=today, bazar=bazar, comment=bazar_list)
        messages.success(request, 'Bazar added successfully')
        return redirect('total-bazar')
    
    return render(request, 'user_dashboard/add_bazar.html', {'today':today})


@login_required
def total_bazar(request):
    this_month = dateTime.date.today().month
    month = dateTime.date(1900, this_month, 1).strftime('%B')
    this_month_bazar = Daily_Bazar.objects.filter(date__month=this_month, user=request.user)
    # this_month_bazar = Daily_Bazar.objects.filter(user=request.user)
    
    total_bazar = 0
    for item in this_month_bazar:
        total_bazar += item.bazar
    return render(request, 'user_dashboard/total_bazar.html', {'this_month_bazar': this_month_bazar, 'this_month':month, 'total_bazar':total_bazar})


@login_required
def partial_delete(request, pk):
    p = Partial_Meal.objects.get(id=pk)
    p.delete()
    return redirect('manage-meal')


@login_required
def delete_all_meal(request):
    d = Daily_Meal.objects.all()
    d.delete()
    return redirect('total-meal')


@login_required
def delete_all_bazar(request):
    d = Daily_Bazar.objects.all()
    d.delete()
    return redirect('total-bazar')


@login_required
def profile(request):
    if request.POST:
        user = User.objects.get(id=request.user.id)
        
        print(request.FILES['image'])
        if 'image' in request.FILES:
            if user.image:
                user.image.delete()
                user.image = request.FILES['image']
            else:
                print(user.username)
                user.image = request.FILES['image']
        user.save()
    return render(request, 'user_dashboard/profile.html')
