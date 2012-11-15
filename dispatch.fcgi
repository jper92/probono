#!/usr/local/bin/python2.7
import sys, os

sys.path.append('/var/chroot/home/content/16/10018916/lib/python-packages')
sys.path.insert(0, '/var/chroot/home/content/16/10018916/red-ciudadana-voluntariado')
sys.path.append('/var/chroot/home/content/16/10018916/red-ciudadana-voluntariado/proyecto_voluntariado')

os.chdir("/var/chroot/home/content/16/10018916/red-ciudadana-voluntariado/proyecto_voluntariado")
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto_voluntariado.settings'


from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
