# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from app.models import *
from app.forms import *
from datetime import datetime

@login_required(login_url="/login/")
def index(request):
    context = {'segment' : 'index'}
    return render(request, "index.html", context)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        context['segment'] = load_template

        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:

        template = loader.get_template( 'pages/error-404.html' )
        return HttpResponse(template.render(context, request))

@login_required(login_url="/login/")
def products(request):
    type = "grid"
    products = product.objects.all()
    return render(request, 'pages/products.html'
                  , {'products': products
                      , 'type': type})

def addProduct(request):
    if request.method == "POST":
        form = productForm(request.POST)
       # if form.is_valid():
        #    try:
        type = "grid"
        msg = "1"
        latest = product.objects.latest('id')
        form.fields["id"].initial = latest.id+ 1
        id = request.POST['id']
        name = request.POST['name']
        create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_uid = 1
        write_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_uid = 1
        category = request.POST['category']
        description = request.POST['description']
        price = request.POST['price']
        pro = product(id=id, write_date=write_date, write_uid=write_uid,create_date=create_date,
         create_uid = create_uid, name=name, description=description, price=price, category=category)

        pro.save()
        products = product.objects.all()
                #messages.success(request, f'Success, Product Saved Successfully')
        return render(request, 'pages/products.html'
                              , {'type': type, 'msg': msg, 'products': products})
         #   except:
          #      pass
        #else:
            #messages.warning(request, f'Sorry, Record Save Error - Invalid Fields')
            #return redirect(addProduct)
    else:
        form = productForm()
        latest = product.objects.latest('id')
        form.fields["id"].initial = latest.id+ 1
        form.fields["create_uid"].initial = 1
        form.fields["write_uid"].initial = 1
        form.fields["create_date"].initial = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        form.fields["write_date"].initial = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        form.fields['id'].widget.attrs['readonly'] = True
        form.fields['create_date'].widget.attrs['readonly'] = True
        form.fields['write_date'].widget.attrs['readonly'] = True
        form.fields['create_uid'].widget.attrs['readonly'] = True
        form.fields['write_uid'].widget.attrs['readonly'] = True
        type = "add"
        return render(request, 'pages/products.html', {'type': type, 'form': form})

