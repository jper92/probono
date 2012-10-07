# Create your views here.
from django.http import *
from django.shortcuts import render_to_response
from django.template import *

from models import Organizacion, Voluntario
from forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def ingreso_organizacion(request):
	if request.method == 'POST':
		ong = Organizacion(es_empresa=False, expira = '2001-01-01')
		form = FormularioONG(request.POST, instance = ong)
		if form.is_valid():
			interesado = form.save()
	else:
		form = FormularioONG()
	return render_to_response('ingreso_organizaciones.html', {'form': form}, context_instance=RequestContext(request))

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
			else:
				user.delete()
		return render_to_response('new_volunteer.html',{'form':form, 'error': form['username'].value() + ' already exists'}, context_instance=RequestContext(request))
	else:
		form = FormularioVoluntario()
	return render_to_response('new_volunteer.html', {'form': form}, context_instance=RequestContext(request))

def about(request):
	return render_to_response('about.html',{}, context_instance=RequestContext(request))
	
def contact_us(request):
	return render_to_response('contact.html',{}, context_instance=RequestContext(request))
