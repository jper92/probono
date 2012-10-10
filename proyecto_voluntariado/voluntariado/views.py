# Create your views here.
import datetime
from django.http import *
from django.shortcuts import render_to_response
from django.template import *

from models import Organizacion, Voluntario
from forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def ingreso_organizacion(request):
	if request.method == 'POST':
		form = FormularioONG(request.POST)
		try:
			user = User.objects.get(username=form['username'].value())
		except:
			user = User.objects.create_user(form['username'].value(), form['correo'].value(), form['password'].value())
			org = Organizacion(user = user, es_empresa = False)
			form = FormularioONG(request.POST, instance = org)
			if form.is_valid():
				form.save()
				return render_to_response('volunteer_profile.html', {'form': form }, context_instance=RequestContext(request))
			else:
				user.delete()
				return render_to_response('new_volunteer.html',{'form':form}, context_instance=RequestContext(request))
		return render_to_response('new_volunteer.html',{'form':form, 'error': form['username'].value() + ' already exists'}, context_instance=RequestContext(request))
	else:
		form = FormularioONG()
	return render_to_response('new_volunteer.html', {'form': form, 'title': 'Nueva ONG'}, context_instance=RequestContext(request))

def ingreso_empresa(request):
	if request.method == 'POST':
		ong = Organizacion(es_empresa=True)
		form = FormularioEmpresa(request.POST, instance = ong)
		if form.is_valid():
			interesado = form.save()
	else:
		form = FormularioEmpresa()
	return render_to_response('ingreso_organizaciones.html', {'form': form}, context_instance=RequestContext(request))



def ingreso_voluntario(request):
	if request.method == 'POST':
		form = FormularioVoluntario(request.POST)
		try:
			user = User.objects.get(username=form['username'].value())
		except:
			user = User.objects.create_user(form['username'].value(), form['correo'].value(), form['password'].value())
			vol = Voluntario(user = user)
			form = FormularioVoluntario(request.POST, instance = vol)
			if form.is_valid():
				interesado = form.save()
				return render_to_response('volunteer_profile.html', {'form': form , 'title':'Nuevo voluntario' }, context_instance=RequestContext(request))
			else:
				user.delete()
				return render_to_response('new_volunteer.html',{'form':form}, context_instance=RequestContext(request))
		return render_to_response('new_volunteer.html',{'form':form, 'title':'Nuevo voluntario', 'error': form['username'].value() + ' already exists'}, context_instance=RequestContext(request))
	else:
		form = FormularioVoluntario()
	return render_to_response('new_volunteer.html', {'form': form, 'title':'Nuevo voluntario'}, context_instance=RequestContext(request))



def volunteer_profile(request):
	vol = Voluntario.objects.get(user='15')
	return render_to_response('volunteer_profile.html', {'vol': vol, 'current': datetime.datetime.now().year - vol.nacimiento.year }, context_instance=RequestContext(request))

def about(request):
	return render_to_response('about.html',{}, context_instance=RequestContext(request))
	
def contact_us(request):
	return render_to_response('contact.html',{}, context_instance=RequestContext(request))

###@login_required
def match_search(request, tipo, id_req):
    lista=[]
    id_req = int(id_req)
    #print tipo,id_req
    if tipo=='voluntario':
        especialidades = Voluntario.objects.get(user=id_req).especialidades.all()
        favoritos = Voluntario.objects.get(user=id_req).favoritos.all()
        lista = Puesto.objects.all()
        #print lista
        for puesto in lista:
            for favorito in favoritosv:
                if not favorito in puesto.favoritos:
                    lista.remove(puesto)
            for especialidad in especialidades:
                if not especialidad in puesto.especialidades:
                    lista.remove(puesto)
        #print lista
    return render_to_response('match_search.html',{'tipo':tipo,'lista':lista}, context_instance=RequestContext(request))



