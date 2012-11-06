# Create your views here.
import datetime
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import *
from django.db.models import Q

from models import Organizacion, Voluntario
from forms import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from linkedin import hola, requestToken

# Estos 2 metodos indican a la view ingreso_organizacion si se trata de ONG o de empresa
def ingreso_ong(request):
	return ingreso_organizacion(request, True)
def ingreso_empresa(request):
	return ingreso_organizacion(request, False)

#  
#  name: ingreso_organizacion
#  @param request, es_ong: bool
#  

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



# Vista ingreso voluntario
def ingreso_voluntario(request):
	if request.method == 'POST':	# Intenta crear un usuario, si algo no es validado se eliminan todos los cambios
		# Si se elige agregar un nuevo interes
		if 'nuevointeres' in request.POST:
			form = FormInteres(request.POST)
			if form.is_valid():
				form.save()
				return render_to_response('new_volunteer.html', {'form': FormularioVoluntario(request.POST),'interes': FormInteres(), 'title':'Nuevo Voluntario'}, context_instance=RequestContext(request))
			else:
				return render_to_response('new_volunteer.html', {'form': FormularioVoluntario(request.POST),'interes': FormInteres(), 'title':'Nuevo Voluntario', 'error':'Error: No se pudo guardar el interes'}, context_instance=RequestContext(request))
		
		# Si se elige llenar datos por medio de LinkedIn
		#elif 'pin_submit' in request.POST:
			

		# Aqui se asume que se guardara un nuevo voluntario.
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
				return render_to_response('new_volunteer.html',{'form':form, 'interes': FormInteres(), }, context_instance=RequestContext(request))
		return render_to_response('new_volunteer.html',{'form':form, 'interes': FormInteres(), 'title':'Nuevo voluntario', 'error': form['username'].value() + ' already exists'}, context_instance=RequestContext(request))
	else:
		form = FormularioVoluntario()
	return render_to_response('new_volunteer.html', {'form': form, 'interes': FormInteres(), 'title':'Nuevo voluntario'}, context_instance=RequestContext(request))

# Ingreso de nuevo proyecto
def nuevo_proyecto(request, id_ong):
	ong = Organizacion.objects.get(user=id_ong)
	if request.method == 'POST':
		form = FormularioProyecto(request.POST)
		#print form
		if form.is_valid():
			proyecto = form.save(commit = True)
			return HttpResponseRedirect('../../../proyecto/'+str(proyecto.id))
	else:
		form = FormularioProyecto(initial={'organizacion':ong.correo})
	return render_to_response('nuevo_proyecto.html', {'form':form}, context_instance=RequestContext(request))

# Perfil del proyecto
def proyecto(request, id_proy):
	proyecto = Proyecto.objects.get(id=id_proy)
	return render_to_response('proyecto.html', {'proyecto':proyecto}, context_instance=RequestContext(request))

# Ingreso de Puesto
def nuevo_puesto(request, id_proy):
	if request.method == 'POST':
		form = FormularioPuesto(request.POST)
		print request.POST
		print form
		if form.is_valid():
			puesto = form.save()
			return HttpResponseRedirect('../../../puesto/'+str(puesto.id))
		else:
			print 'NO funciona.'
	else:
		form = FormularioPuesto(initial={'proyecto':id_proy})
	return render_to_response('nuevo_puesto.html', {'form':form}, context_instance=RequestContext(request))

# Perfil de puesto
def puesto(request, id_puesto):
	puesto = Puesto.objects.get(id=id_puesto)
	return render_to_response('puesto.html', {'puesto':puesto}, context_instance=RequestContext(request))

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
	lista2=[]
	id_req = int(id_req)
	volemp = None
	q = Q()

	if tipo=='voluntario':
		volemp = Voluntario.objects.get(user=id_req)
	elif tipo=='empresa':
		volemp = Organizacion.objects.get(user=id_req)
	
	if tipo=='voluntario' or tipo=='empresa':
		especialidades = volemp.especialidades.all()
		favoritos = volemp.favoritos.all()
		for f in favoritos:
			q.add(Q(favoritos=f),Q.OR)
		for e in especialidades:
			q.add(Q(especialidades=e),Q.OR)
		
		lista = Puesto.objects.filter(q)

	elif tipo=='ong':
		especialidades = Puesto.objects.get(id=id_req).especialidades.all()
		favoritos = Puesto.objects.get(id=id_req).favoritos.all()
		
		for e in especialidades:
			q.add(Q(especialidades=e),Q.OR)
		for f in favoritos:
			q.add(Q(favoritos=f),Q.OR)
		
		lista = Voluntario.objects.filter(q)
		lista2 = Organizacion.objects.filter(Q(es_empresa=True), q)
		print lista
		print lista2
	return render_to_response('match_search.html',{'tipo':tipo,'lista':lista,'lista2':lista2}, context_instance=RequestContext(request))

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
		if 'login' in request.POST:
			user = authenticate(username=request.POST['username'], password = request.POST['password'])
			if user is not None:
				login(request, user)
			else:
				return render_to_response('main.html', {'user': user, 'log':False, 'invalid':True}, context_instance=RequestContext(request))
		else:
			logout(request)
	vol = None
	if request.user.is_authenticated():
		vol = Voluntario.objects.get(user=request.user)
	return render_to_response('main.html',{'current': None if vol==None else datetime.datetime.now().year - vol.nacimiento.year, 'vol': vol, 'user':request.user, 'log': request.user.is_authenticated()}, context_instance=RequestContext(request))
	
def linkedin(request):
	return HttpResponse(requestToken())
