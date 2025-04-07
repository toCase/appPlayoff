from django.shortcuts import render, redirect
from django.db.models import Q

from .. import forms
from .. import models
from .. import utils
from ..utils import ROW_COUNT

def get_data(user_id: int, query:str = None):    
    if query is not None:
        data = models.Category.objects.filter(Q(user=user_id) & Q(name__icontains=query))
    else:
        data = models.Category.objects.filter(Q(user=user_id))
    return data    

def load(request):
    user_id = request.user.id
    query = request.session.get("CAT_SEARCH")
    data = get_data(user_id, query)
    context = {
        'id':'0',
        'data':data[0:ROW_COUNT],
        'query':query,
    }
    request.session["CAT_PAGE"] = '1'
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = '1'
    return render(request, template_name='app_category.html', context=context)

def filter(request):
    user_id = request.user.id
    query = request.session.get("CAT_SEARCH")
    if request.method == "GET":
        if request.GET.get("search") != "":
            query = request.GET.get("search")            
        else:
            query = ""
        request.session['CAT_SEARCH'] = query
    data = get_data(user_id, query)
    context = {
        'id': '0',
        'data': data[0:ROW_COUNT],
        'query': query,
    }
    request.session["CAT_PAGE"] = '1'
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = '1'
    return render(request, template_name='app_category_container.html', context=context)

def add(request):
    form = forms.CategoryForm()
    context = {
        'form':form,
        'id':'0',
        'data':'',
    }
    return render(request, template_name='app_category_container.html', context=context)

def save(request, pk:str):
    cat_id = int(pk)
    user_id = request.user.id
    
    form = forms.CategoryForm(request.POST)
    
    if cat_id > 0:
        model = models.Category.objects.get(idx=cat_id)
        form = forms.CategoryForm(request.POST, instance=model)
    
    if form.is_valid():
        data = form.save(commit=False)
        data.user_id = user_id
        data.save()
        return page(request, '1')
    else:
        errors = utils.error_messages(form.errors.get_json_data())
        context = {
            'id':pk,
            'form':form,
            'data':'',
            'errors':errors,
        }
        return render(request, template_name="app_category_container.html", context=context)
        
    

def edit(request, pk:str):
    cat_id = int(pk)
    model = models.Category.objects.get(idx=cat_id)
    form = forms.CategoryForm(instance=model)
    context = {
        'form':form,
        'id':pk,
        'data':'',
    }
    return render(request, template_name="app_category_container.html", context=context)

def delete(request, pk:str):
    cat_id = int(pk)
    model = models.Category.objects.get(idx=cat_id)
    model.delete()
    return page(request, '1')

def page(request, page:str):
    user_id = request.user.id
    query = request.session.get("CAT_SEARCH")
    
    data = get_data(user_id, query)
    context = {
        'id':'0',
        'data':data[utils.page_from(int(page)):utils.page_to(int(page))],
        'query':query,
    }
    
    request.session["CAT_PAGE"] = page
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = page    
    return render(request, template_name="app_category_container.html", context=context)