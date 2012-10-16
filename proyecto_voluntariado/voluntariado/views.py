# Create your views here.
import datetime
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import *

from models import Organizacion, Voluntario
from forms import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Estos 2 metodos indican a la view ingreso_organizacion si se trata de ONG o de empresa
def ingreso_ong(request):
	return ingreso_organizacion(request, True)
def ingreso_empresa(request):
	return ingreso_organizacion(request, False)

def ingreso_organizacion(request, es_ong):
	if request.method == 'POST':
		form = FormularioONG(request.POST)
		try:
			user = User.objects.get(username=form['username'].value())
		except:
			user = User.objects.create_user(form['username'].value(), form['correo'].value(), form['password'].value())
			org = Organizacion(user = user, es_empresa = not es_ong, expira = datetime.datetime.now() + datetime.timedelta(days=30))
			form = FormularioONG(request.POST, instance = org)
			if form.is_valid():
				form.save()
				#return render_to_response('volunteer_profile.html', {'form': form, 'title': 'Nueva ONG' }, context_instance=RequestContext(request))
				return redirect('/ong/' + str(org.user_id))
			else:
				user.delete()
				return render_to_response('new_volunteer.html',{'form':form}, context_instance=RequestContext(request))
		return render_to_response('new_volunteer.html',{'form':form, 'error': form['username'].value() + ' already exists', 'title': 'Nueva ONG' if es_ong else 'Nueva empresa'}, context_instance=RequestContext(request))
	else:
		form = FormularioONG()
	return render_to_response('new_volunteer.html', {'form': form, 'title': 'Nueva ONG' if es_ong else 'Nueva empresa'}, context_instance=RequestContext(request))




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
				return redirect('/voluntario/' + str(vol.user_id))
			else:
				user.delete()
				return render_to_response('new_volunteer.html',{'form':form}, context_instance=RequestContext(request))
		return render_to_response('new_volunteer.html',{'form':form, 'title':'Nuevo voluntario', 'error': form['username'].value() + ' already exists'}, context_instance=RequestContext(request))
	else:
		form = FormularioVoluntario()
	return render_to_response('new_volunteer.html', {'form': form, 'title':'Nuevo voluntario'}, context_instance=RequestContext(request))



def volunteer_profile(request, id_voluntario):
	vol = Voluntario.objects.get(user=id_voluntario)
	return render_to_response('volunteer_profile.html', {'vol': vol, 'current': datetime.datetime.now().year - vol.nacimiento.year }, context_instance=RequestContext(request))

def ong_profile(request, id_ong):
	ong = Organizacion.objects.get(user=id_ong)
	return render_to_response('ong_profile.html', {'ong':ong }, context_instance=RequestContext(request))

def about(request):
	return render_to_response('about.html',{}, context_instance=RequestContext(request))
	
def contact_us(request):
	return render_to_response('contact.html',{}, context_instance=RequestContext(request))

###@login_required
def match_search(request, tipo, id_req):
	lista=[]
	id_req = int(id_req)
	volemp = None

	if tipo=='voluntario':
		volemp = Voluntario.objects.get(user=id_req)
	elif tipo=='empresa':
		volemp = Organizacion.objects.get(user=id_req)
	
	if tipo=='voluntario' or tipo=='empresa':
		especialidades = volemp.especialidades.all()
		favoritos = volemp.favoritos.all()
		puestos = Puesto.objects.all()
		
		for puesto in puestos:
			if not puesto in lista:
				for favorito in favoritos:
					if favorito in puesto.favoritos.all():
						lista.append(puesto)
						break
			if not puesto in lista:
				for especialidad in especialidades:
					if especialidad in puesto.especialidades.all():
						lista.append(puesto)
						break

	if tipo=='ong':
		especialidades = Puesto.objects.get(user=id_req).especialidades.all()
		favoritos = Puesto.objects.get(user=id_req).favoritos.all()
		voluntarios = Voluntario.objects.all()
		empresas = Organizacion.objects.all()
		
		for voluntario in voluntarios:
			if not voluntario in lista:
				for favorito in favoritos:
					if favorito in voluntario.favoritos.all():
						lista.append(puesto)
						break
			if not voluntario in lista:
				for especialidad in especialidades:
					if especialidad in voluntario.especialidades.all():
						lista.append(puesto)
						break
		# TODO agregar empresas, cuidando que no se agregue a si misma

	return render_to_response('match_search.html',{'tipo':tipo,'lista':lista}, context_instance=RequestContext(request))

#  
#  name: new_interest
#  @param request, redirect: 0 es para nuevo voluntario, 1 es para nueva org, 2 es para empresa
#  @return http_response
#  

def new_interest(request, redir):
	
	if request.method=='POST':
		#print 'save_btn' in request.POST
		red = '/nuevovoluntario/'
		if redir=='1':
			red = '/nuevaorg/'
		elif redir=='2':
			red = '/nuevaempresa/'
		if 'skip' in request.POST:
			return redirect(red)
		form = FormInteres(request.POST)
		if form.is_valid():
			form.save()
		else:
			return render_to_response('new_interest.html', {'form': form, 'title': u'Nuevo inter\u00e9s'}, context_instance=RequestContext(request))
		if 'save_and_other' in request.POST:
			return render_to_response('new_interest.html', {'form': FormInteres(), 'title': u'Nuevo inter\u00e9s', 'success': 'Gracias, dato guardado' , 'favoritos': Intereses.objects.filter(es_favorito=True).order_by('nombre'), 'especialidades': Intereses.objects.filter(es_favorito=False).order_by('nombre')}, context_instance=RequestContext(request))
		else:
			return redirect(red)
	else:
		form = FormInteres()
		return render_to_response('new_interest.html', { 'form': form , 'title': u'Nuevo inter\u00e9s', 'favoritos': Intereses.objects.filter(es_favorito=True).order_by('nombre'), 'especialidades': Intereses.objects.filter(es_favorito=False).order_by('nombre')}, context_instance=RequestContext(request))

def main_view(request):
	if request.method == 'POST':
		print request.POST
		user = authenticate(username=request.POST['username'], password = request.POST['password'])
		if user is not None:
			login(request, user)
			return render_to_response('main.html', {'user': user, 'log':True}, context_instance=RequestContext(request))
	return render_to_response('main.html',{'user':request.user, 'log': request.user.is_authenticated()}, context_instance=RequestContext(request))
	
