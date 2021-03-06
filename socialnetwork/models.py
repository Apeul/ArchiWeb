from django.db import models

# Importation des modeles
from django.contrib.auth.models import User

# Constant Models

HOMME = 'H'
FEMME = 'F'
GENRE_CHOICES = (
	(HOMME, 'Homme'),
    (FEMME, 'Femme'),
)

SARTHE = 72
MAYENNE = 53
LOIRE_ATLANTIQUE = 44
MAINE_ET_LOIRE = 49
VENDEE = 85
DEPT_CHOICES = (
	(SARTHE, 'Sarthe'),
	(MAYENNE, 'Mayenne'),
	(MAINE_ET_LOIRE, 'Maine et Loire'),
	(LOIRE_ATLANTIQUE, 'Loire Atlantique'),
	(VENDEE,'Vendee')
)

# Create your models here.

class Affinite(models.Model):
	ajouteur = models.ForeignKey(User, related_name='ajouteur')
	ajoute = models.ForeignKey(User, related_name='ajoute')
	ajouteurConfirm = models.BooleanField(default=False)
	ajouteConfirm = models.BooleanField(default=False)

class Bar(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	localisation = models.IntegerField(choices=DEPT_CHOICES,default=72)
	picture = models.FileField(upload_to='upload',default='')
	speciality = models.CharField(max_length=100, default='')
	prix = models.IntegerField(default=5)
	description = models.CharField(max_length=10000,default='')
	notes = models.FloatField(default=0)

class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    emetteur = models.ForeignKey(User, related_name='emetteur')
    recepteur = models.ForeignKey(User, related_name='recepteur')
    message = models.CharField(max_length=200)

class Discotheque(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	localisation = models.IntegerField(choices=DEPT_CHOICES,default=72)
	picture = models.FileField(upload_to='upload',default='')
	speciality = models.CharField(max_length=100, default='')
	prix = models.IntegerField(default=5)
	description = models.CharField(max_length=10000,default='')
	notes = models.FloatField(default=0)

class InformationUser(models.Model):
	user = models.ForeignKey(User)
	genre = models.CharField(choices=GENRE_CHOICES, max_length=1,default='Homme')
	localisation = models.IntegerField(choices=DEPT_CHOICES)
	age = models.IntegerField()
	description = models.CharField(max_length=500)
	profession = models.CharField(max_length=100,default='Prof')

class PictureUser(models.Model):
	user = models.ForeignKey(User)
	picture = models.FileField(upload_to='upload')
	add_date = models.DateField(auto_now_add=True)

class presentBar(models.Model):
	id_bar = models.ForeignKey(Bar)
	id_person = models.ForeignKey(User)

class presentDisco(models.Model):
	id_disco = models.ForeignKey(Discotheque)
	id_person = models.ForeignKey(User)

class Restaurant(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	localisation = models.IntegerField(choices=DEPT_CHOICES,default=72)
	picture = models.FileField(upload_to='upload',default='')
	speciality = models.CharField(max_length=100, default='')
	prix = models.IntegerField(default=5)
	description = models.CharField(max_length=10000,default='')
	notes = models.FloatField(default=0)

class presentRestau(models.Model):
	id_restau = models.ForeignKey(Restaurant)
	id_person = models.ForeignKey(User)

class SearchInformationUser(models.Model):
	user = models.ForeignKey(User)
	genreF = models.BooleanField(default=False)
	genreM = models.BooleanField(default=False)
	localisation = models.IntegerField(choices=DEPT_CHOICES)
	ageMin = models.IntegerField()
	ageMax = models.IntegerField()

class starBar(models.Model):
	id_bar = models.ForeignKey(Bar)
	id_user = models.ForeignKey(User)
	notes = models.IntegerField(default=0)

class starDiscotheque(models.Model):
	id_disco = models.ForeignKey(Discotheque)
	id_user = models.ForeignKey(User)
	notes = models.IntegerField(default=0)

class starRestaurant(models.Model):
	id_restau = models.ForeignKey(Restaurant)
	id_user = models.ForeignKey(User)
	notes = models.IntegerField(default=0)
