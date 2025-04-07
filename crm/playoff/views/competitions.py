from django.shortcuts import render, redirect
from django.db.models import Q, Count

from .. import forms
from .. import models
from .. import utils
from ..utils import ROW_COUNT

def get_data(trn_id:int, query:str = None):
    an_cp = Count('competitionparticipants')
    if query is not None:
        data = models.Competition.objects.annotate(cp=an_cp).filter(Q(tournament=trn_id) & (Q(category__icontains=query) | Q(gender__icontains=query)))
    else:
        data = models.Competition.objects.annotate(cp=an_cp).filter(Q(tournament=trn_id))
    return data    

def load(request, pk:str):
    trn_id = int(pk)
    trn_name = models.Tournament.objects.get(idx=trn_id).name
    
    request.session["TRN_ID"] = trn_id    
    
    query = request.session.get("COM_SEARCH")
    
    data = get_data(trn_id, query)
    
    context = {
        'id':'0',
        'idx': pk,
        'tournament':trn_name,
        'data':data[0:ROW_COUNT],
        'query':query,
    }
    
    request.session["COM_PAGE"] = '1'
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = '1'
    return render(request, template_name='app_competitions.html', context=context)


def filter(request):
    trn_id = request.session.get("TRN_ID")
    query = request.session.get("COM_SEARCH")
    
    if request.method == "GET":
        if request.GET.get('search') != "":
            query = request.GET.get('search')
            request.session['COM_SEARCH'] = query
        else:
            query = ''
    
    data = get_data(trn_id, query)
    
    context = {
        'id':'0',
        'data':data[0:ROW_COUNT],
        'query':query,
    }
    
    request.session["COM_PAGE"] = '1'
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = '1'
    return render(request, template_name='app_competitions_container.html', context=context)

def add(request):
    form = forms.CompetitionsForm(initial={'user':request.user.id})
    context = {
        'id':'0',
        'form':form,
        'data':'',
    }
    return render(request, template_name='app_competitions_container.html', context=context)

def edit(request, pk:str):
    comp_id = int(pk)
    model = models.Competition.objects.get(idx=comp_id)
    form = forms.CompetitionsForm(instance=model, initial={'user':request.user.id})
    context = {
        'id':pk,
        'form':form,
        'data':'',
    }
    return render(request, template_name='app_competitions_container.html', context=context)

def save(request, pk:str):
    comp_id = int(pk)
    trn_id = request.session.get("TRN_ID")
    user_id = request.user.id
    
    form = forms.CompetitionsForm(request.POST, initial={'user':request.user.id})
    if comp_id > 0:
        model = models.Competition.objects.get(idx=comp_id)
        form = forms.CompetitionsForm(request.POST, instance=model, initial={'user':request.user.id})
    
    if form.is_valid():
        data = form.save(commit=False)
        data.tournament_id = trn_id
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
        return render(request, template_name='app_competitions_container.html', context=context)
        

def delete(request, pk:str):
    comp_id = int(pk)
    model = models.Competition.objects.get(idx=comp_id)
    model.delete()
    return page(request, '1')

def page(request, page:str):
    trn_id = request.session.get("TRN_ID")
    query = request.session.get("COM_SEARCH")
    
    data = get_data(trn_id, query)
    
    context = {
        'id':'0',
        'data':data[utils.page_from(int(page)):utils.page_to(int(page))],
        'query':query,
    }
    
    request.session["COM_PAGE"] = page
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = page
    return render(request, template_name='app_competitions_container.html', context=context)


