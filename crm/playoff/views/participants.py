import csv
from django.shortcuts import render, redirect
from django.db.models import Q, Count

from .. import forms
from .. import models
from .. import utils
from ..utils import ROW_COUNT

def get_data(trn_id:int, query:str = None):
    an_cp = Count('competitionparticipants')
    if query is not None:
        data = models.Participants.objects.annotate(cp=an_cp).filter(Q(tournament=trn_id) & Q(name__icontains=query))
    else:
        data = models.Participants.objects.annotate(cp=an_cp).filter(Q(tournament=trn_id))
    return data    

def load(request, pk:str):
    trn_id = int(pk)
    trn_name = models.Tournament.objects.get(idx=trn_id).name    
    request.session["TRN_ID"] = trn_id    
    query = request.session.get("PCP_SEARCH")    
    data = get_data(trn_id, query)    
    context = {
        'id':'0',
        'idx': pk,
        'tournament':trn_name,
        'data':data[0:ROW_COUNT],
        'query':query,
    }    
    request.session["PCP_PAGE"] = '1'
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = '1'
    return render(request, template_name='app_participants.html', context=context)

def filter(request):
    trn_id = request.session.get("TRN_ID")
    query = request.session.get("PCP_SEARCH")
    
    if request.method == "GET":
        if request.method == "GET":
            query = request.GET.get("search")
            request.session["PCP_SEARCH"] = query
        else:
            query = ""
    data = get_data(trn_id, query)
    context = {
        'data':data[0:ROW_COUNT],
        'query':query
    }
    request.session["PCP_PAGE"] = '1'
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = '1'
    return render(request, template_name='app_participants_container.html', context=context)

def add(request):
    form = forms.ParticipantsForm()
    context = {
        'form':form,
        'id':'0',
        'data':''
    }
    return render(request, template_name='app_participants_container.html', context=context)

def save(request):
    trn_id = request.session.get("TRN_ID")
    user_id = request.user.id
    if request.method == 'POST':
        form = forms.ParticipantsForm(request.POST, request.FILES)
        if form.is_valid():            
            fcsv = request.FILES['csv_file']
            try:
                lines = fcsv.read().decode('utf-8').splitlines()
                for name in lines:
                    model = models.Participants()        
                    model.name = name
                    model.tournament_id = trn_id
                    model.user_id = user_id
                    model.save()                    
                return page(request, '1')
            
            except Exception as e:
                errors = [f"Ошибка при чтении файла: {e}"]
                context = {
                    'form':form,
                    'data':'',
                    'errors':errors
                }
                return render(request, template_name='app_participants_container.html', context=context)
        else:
            return add(request)        

def delete(request, pk:str):
    pcp_id = int(pk)
    model = models.Participants.objects.get(idx=pcp_id)
    model.delete()
    return page(request, '1')
    
def clear(request):
    trn_id = request.session.get("TRN_ID")
    query = request.session.get("PCP_SEARCH")
    
    data = get_data(trn_id, query)
    for item in data:
        item.delete()    
    return page(request, '1')    

def page(request, page:str):
    trn_id = request.session.get("TRN_ID")
    query = request.session.get("PCP_SEARCH")
    
    data = get_data(trn_id, query)
    context = {
        'data':data[utils.page_from(int(page)):utils.page_to(int(page))],
        'query':query,
    }
    
    request.session['PCP_PAGE'] = page
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = page
    return render(request, template_name='app_participants_container.html', context=context)
