from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('voluntariado.views',
    url(r'^nuevaorg/$', 'ingreso_organizacion'),
    url(r'^nuevovoluntario/$', 'ingreso_voluntario'),
    url(r'^nuevaempresa/$', 'ingreso_empresa'),
    url(r'^profile/$', 'volunteer_profile'),
)
