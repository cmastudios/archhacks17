import cv2
from django.conf.urls import url
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from nutritrack import predict, nut_api, prices
from nutritrack.forms import UploadFileForm, RegistrationForm
from nutritrack.models import MealReport, Nutrient, Ingredient, Meal


@login_required
def index(request):
    nut = Nutrient()
    nut.kcal = 0
    nut.fat = 0
    nut.carb = 0
    nut.sugar = 0
    nut.protein = 0
    nut.sodium = 0
    nut.vA = 0
    nut.vC = 0
    nut.iron = 0
    nut.calcium = 0
    mr = MealReport.objects.filter(user=request.user)
    for r in list(mr):
        for i in r.meal.ingredients.all():
            n = i.nutrients
            nut += n
    return render(request, 'nutritrack/index.html', {'user': request.user, 'nut': nut})


@ensure_csrf_cookie
def splash(request):
    return render(request, 'splash.html')

@login_required
def report(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['file']
            with open('/tmp/image' + image.name, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            opencvImage = cv2.imread('/tmp/image' + image.name)
            pred = predict.client.predict_image(opencvImage)
            label = pred['prediction']['label']
            m, new = Meal.objects.get_or_create(name=label)
            if new:
                nut = nut_api.load_nutrition_data(label)
                i = Ingredient(name=label, amount=1, nutrients=nut)
                i.save()
                m.ingredients.add(i)
                m.save()
            mr = MealReport(user=request.user, meal=m)
            mr.save()

            return render(request, 'nutritrack/predict.html', {'options': pred['top5']})
            #return redirect('/nutritrack/meals/')
    else:
        form = UploadFileForm()
    return render(request, 'nutritrack/form.html', {'form': form})


@login_required
def profile(request):
    return redirect('/nutritrack/')


@login_required
def meals(request):
    return render(request, 'nutritrack/meals.html', {'meals': [mr.meal for mr in MealReport.objects.filter(user=request.user)]})


@login_required
def recipe(request, recipe_id):
    r = Meal.objects.get(pk=recipe_id)
    inc = list(r.ingredients.all())
    for i in inc:
        p = prices.get_price(i.name)
        if p is None:
            i.price = '(Price Unavailable)'
        else:
            i.price = f'${(p["unit"] * i.amount):.2f} - ${(p["package"]):.2f} per package (Walmart)'
    return render(request, 'nutritrack/recipe.html', {'recipe': r, 'ingredients': inc})


@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            login(request, user)
            messages.info(request, 'Welcome to NutriTrack!')
            return redirect('/nutritrack/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

