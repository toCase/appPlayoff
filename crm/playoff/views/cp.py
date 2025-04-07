from django.shortcuts import render, redirect
from django.db.models import Q, Count

from .. import forms
from .. import models
from .. import utils
from ..utils import ROW_COUNT

def load(request, pk:str):
    trn_id = request.session.get("TRN_ID")
    
    com_id = int(pk)
    com_name = models.Competition.objects.get(idx=com_id).__str__()
    
    request.session["COM_ID"] = com_id    
    data = models.CompetitionParticipants.objects.filter(Q(competition_id=com_id))
    
    context = {
        'id':'0',
        'idx': pk,
        'trn_id':trn_id,
        'competition':com_name,
        'data':data[0:ROW_COUNT],
    }
    
    request.session["COM_PAGE"] = '1'
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = '1'
    return render(request, template_name='app_cp.html', context=context)


def filter(request):
    com_id = request.session.get("COM_ID")
    data = models.CompetitionParticipants.objects.filter(Q(competition_id=com_id))
    
    context = {
        'id':'0',
        'data':data[0:ROW_COUNT],
    }
    
    request.session["COM_PAGE"] = '1'
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = '1'
    return render(request, template_name='app_cp_container.html', context=context)
    

def add(request):
    trn_id = request.session.get("TRN_ID")
    form = forms.CPForm(initial={'trn':trn_id})
    context = {
        'id':'0',
        'form':form,
        'data':'',
    }
    return render(request, template_name='app_cp_container.html', context=context)

def edit(request, pk:str):
    trn_id = request.session.get("TRN_ID")
    cp_id = int(pk)
    model = models.CompetitionParticipants.objects.get(idx=cp_id)
    form = forms.CPForm(instance=model, initial={'trn':trn_id})
    context = {
        'id':pk,
        'form':form,
        'data':'',
    }
    return render(request, template_name='app_cp_container.html', context=context)

def save(request, pk:str):
    cp_id = int(pk)
    com_id = request.session.get("COM_ID")
    trn_id = request.session.get("TRN_ID")
    user_id = request.user.id
    
    form = forms.CPForm(request.POST, initial={'trn':trn_id})
    if cp_id > 0:
        model = models.CompetitionParticipants.objects.get(idx=cp_id)
        form = forms.CPForm(request.POST, instance=model, initial={'trn':trn_id})
    
    if form.is_valid():
        data = form.save(commit=False)
        data.competition_id = com_id
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
        return render(request, template_name='app_cp_container.html', context=context)
        

def delete(request, pk:str):
    cp_id = int(pk)
    model = models.CompetitionParticipants.objects.get(idx=cp_id)
    model.delete()
    return page(request, '1')

def page(request, page:str):
    com_id = request.session.get("COM_ID")
    data = models.CompetitionParticipants.objects.filter(Q(competition_id=com_id))
    
    context = {
        'id':'0',
        'data':data[utils.page_from(int(page)):utils.page_to(int(page))],
    }
    
    request.session["COM_PAGE"] = page
    if len(data) > ROW_COUNT:
        context['pag'] = utils.page_list(len(data))
        context['apage'] = page
    return render(request, template_name='app_cp_container.html', context=context)


