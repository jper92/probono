from django.db import models

# Modelo de FrontPage
class Interesados (models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    
    def __str__(self):
	    return self.nombre
    
    class Admin:
        pass