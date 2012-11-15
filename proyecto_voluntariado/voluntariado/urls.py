from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('voluntariado.views',
	url(r'^main/$', 'main_view'),
	url(r'^nuevaorg/$', 'ingreso_ong'),
	url(r'^nuevaempresa/$', 'ingreso_empresa'),
	
	#url(r'^voluntario/(\d+)/$', 'volunteer_profile'), changed to busqueda_vol
	url(r'^empresa/(\d+)/$', 'ong_profile'), #TODO perfil de empresa
	url(r'^(empresa)/(\d+)/buscar_empleo/$', 'match_search'),
	url(r'^ong/(\d+)/$', 'ong_profile'),
	url(r'^ong/(\d+)/nuevoproyecto/$', 'nuevo_proyecto'),
	url(r'^proyecto/(\d+)/$', 'proyecto'),
	url(r'^proyecto/(\d+)/nuevopuesto/$', 'nuevo_puesto'),
	url(r'^puesto/(\d+)/$', 'puesto'),
	url(r'^(puesto)/(\d+)/buscar_voluntarios/$', 'match_search'),
	url(r'^linkedin/$','linkedin'),
	
	# Voluntario
	url(r'^nuevovoluntario/$', 'ingreso_voluntario'),
	url(r'^home/voluntario/$','home_voluntario'),
	url(r'^home/voluntario/buscar_empleo/$', 'busqueda_vol'),
	url(r'^mispuestos/(\d+)/$', 'puesto_voluntario'),
	
	# ONG
	url(r'^home/ong/$','home_ong'),
	
	# Empresa
	url(r'^home/empresa/$','home_empresa'),
	
	url(r'^logout/$','logout_view'),
	url(r'^editarvoluntario/$','edit_volunteer'),
	url(r'^editarong/$','edit_ong'),
	
	# agregar voluntario desde puesto
	url(r'^puesto/(\d+)/voluntario/(\d+)/$', 'puesto_voluntario2'),
	# agregar empresa desde puesto
	url(r'^puesto/(\d+)/empresa/(\d+)/$', 'puesto_empresa'),

	#caso de uso: voluntario/empresa quiere agregar/ver un empleo
	url(r'^mispuestos/(\d+)/$', 'puesto_voluntario'),
	#caso de uso: ong quiere agregar/ver a voluntario para puesto
	url(r'^misvoluntarios/(\d+)/$', 'voluntario_ong'),
)
