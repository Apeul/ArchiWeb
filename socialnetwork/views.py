# Importation des bibiliothèques
from django.contrib	import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render
# Importation des modèles
from django.contrib.auth.models import User
from .models import PictureUser
from .models import Bar,jaimeBar
from .models import informationUser, searchInformationUser

from django.core.mail import send_mail
import os
import random
from django.conf import settings

# Importation des formulaires
from .forms import informationUserForm, searchInformationUserForm, loginForm, registerForm, uploadPictureForm, updateProfilForm, mdpForm,updateBarLike

def index(request):
	if not request.user.is_authenticated:
		formRegister = registerForm()
		formLogin = loginForm()
		formMdp=mdpForm()
		return render(request,'socialnetwork/index.html', {'formRegister': formRegister, 'formLogin': formLogin,'formMdp': formMdp})
	else:
		return redirect(deconnexion)

def csrf_failure(request, reason=""):
	return  HttpResponseForbidden("Access denied")

def page_not_found(request):
    response = render_to_response('404.html',context_instance=RequestContext(request))
    response.status_code = 404

    return response

def connexion(request):
	if request.method == 'POST':
		formLogin = loginForm(request.POST)
		if formLogin.is_valid():
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			if user is not None:
				login(request, user)
				return redirect(deconnexion)
			else:
				messages.add_message(request, messages.ERROR, "Erreur de mot de passe ou de nom d'utilisateur")
				return redirect(index)
	else:
		formLogin = loginForm()
	formRegister = registerForm()
	return render(request, 'socialnetwork/index.html', {'formRegister': formRegister, 'formLogin': formLogin})

def deconnexion(request):
	if request.method == 'POST':
		logout(request)
		messages.success(request, "Vous avez été correctement deconnecté! A bientôt..")
		return redirect(index)
	else:
		if not request.user.is_authenticated:
			return redirect(connexion)
		else:
			return render(request, 'socialnetwork/menu.html')

def mdp_oublie(request):
	if request.method == 'POST':
		formMdp = mdpForm(request.POST)
		if formMdp.is_valid():
			username_u = request.POST['username']
			email_u = request.POST['email']
			try:
				user = User.objects.get(username=username_u, email=email_u)
			except User.DoesNotExist:
				messages.add_message(request, messages.ERROR, "Erreur de nom d'utilisateur ou de l'adresse email")
				return redirect(index)
			nouveaumotdepasse=''
			for i in range(10):
				nouveaumotdepasse += random.choice("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
			user.set_password(nouveaumotdepasse)
			user.save()
			send_mail(
    			'Vis Ton Meeting: changement du mot de passe',
    			'A la suite de votre demande, votre mot de passe a été changé. Utilisez désormais '+ nouveaumotdepasse +' À bientôt sur VTM !',
    			settings.EMAIL_HOST_USER,
    			[email_u], fail_silently=False
			)
		else:
			messages.add_message(request, messages.ERROR, "Erreur de nom d'utilisateur ou de l'adresse email")
			return redirect(index)
	messages.success(request, "Votre nouveau mot de passe vous a correctement été envoyé. Vérifiez votre adresse mail!")
	return redirect(index)

def menu(request):
	form = registerForm(request.POST)
	return render(request, 'socialnetwork/menu.html',{'form': form})


def affinite(request):
	return render(request, 'socialnetwork/affinite.html')

def rencontre(request):
	utilisateur = User.objects.get(pk=request.user.id)

	formInformationUser = informationUserForm()
	formSearchInformationUser = searchInformationUserForm()

	# Chargement des informations de l'utilisateur et les informations de recherche
	try:
		userInformation = informationUser.objects.get(user=utilisateur)
		userSearchInformation = searchInformationUser.objects.get(user=utilisateur)
	except informationUser.DoesNotExist:
		messages.add_message(request, messages.ERROR, "Il est nécéssaire de compléter les informations concernant votre profil et vos recherches")
		return render(request, 'socialnetwork/rencontre.html', {'formInformationUser': formInformationUser, 'formSearchInformationUser': formSearchInformationUser})

	return render(request, 'socialnetwork/rencontre.html')

def montemple(request):
	return render(request, 'socialnetwork/montemple.html')

def bar(request):
	Bars = Bar.objects.all()
	Bar_like = jaimeBar.objects.all()
	return render(request, 'socialnetwork/bar.html',{'Bars': Bars, 'Bar_like': Bar_like})

def ajoutjaime(request):
	if request.method == 'POST':
		
		jaime = jaimeBar(personne=User.objects.get(pk=request.user.id),name=Bar.objects.get(name="Café Crème"))
		jaime.save()
		return render(request, 'socialnetwork/sortie.html', {'updateBarLike': updateBarLike})


def restaurant(request):
	return render(request, 'socialnetwork/restaurant.html')

def sortie(request):
	return render(request, 'socialnetwork/sortie.html')

def forum(request):
	return render(request, 'socialnetwork/forum.html')

def editerProfil(request):
	if request.method == 'POST':
		if "uploadPicture" in request.POST:
			formUploadPicture = uploadPictureForm(request.POST,request.FILES)
			if formUploadPicture.is_valid():
				
				try : 
					picture = PictureUser.objects.get(user=User.objects.get(pk=request.user.id))
					picture.picture.delete()
					picture.picture=request.FILES['picture']
					picture.save()
				except PictureUser.DoesNotExist:
					picture = PictureUser(user=User.objects.get(pk=request.user.id), picture=request.FILES['picture'])
					picture.save()
		else:
			formUploadPicture = uploadPictureForm()

		if "modifInfo" in request.POST:
			formUpdateProfil = updateProfilForm(request.POST)
			user = User.objects.get(pk=request.user.id)
				
			if request.POST['firstname']:
				user.first_name = request.POST['firstname']
				
			if request.POST['lastname']:
				user.last_name = request.POST['lastname']
				
			if request.POST['password']:
				user.set_password(request.POST['password'])

			user.email = request.POST['email']
			user.pseudo = request.POST['username']
			user.save()
		else:
			formUpdateProfil = updateProfilForm({'firstname': request.user.first_name, 'lastname': request.user.last_name, 'username': request.user.username, 'email': request.user.email})
	
	else:
		formUploadPicture = uploadPictureForm()
		formUpdateProfil = updateProfilForm({'firstname': request.user.first_name, 'lastname': request.user.last_name, 'username': request.user.username, 'email': request.user.email})
	
	try:
		lienPicture = PictureUser.objects.get(user=User.objects.get(pk=request.user.id))
	except PictureUser.DoesNotExist:
		lienPicture = PictureUser(picture="/upload/profilePictureOriginal.jpg")

	return render(request, 'socialnetwork/editerProfil.html', {'formUploadPicture': formUploadPicture, 'formEditProfil': formUpdateProfil, 'lienPicture': lienPicture.picture})

def inscription(request):
	if request.method == 'POST':
		form = registerForm(request.POST)
		if form.is_valid():
			username_u=request.POST['username']
			try:
				user = User.objects.get(username=username_u)
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST.get('username'), password=request.POST['password'],email=request.POST['email'])
				user.save()
				user = authenticate(username=request.POST['username'], password=request.POST['password'])
				login(request, user)
				messages.success(request, "Vous êtes à présent inscrit, profitez et faites des rencontres!")
				return redirect(deconnexion)
			messages.add_message(request, messages.ERROR, "Erreur ce pseudo correspond déjà à un profil existant!")
			return redirect(index)
		else:
			messages.add_message(request, messages.ERROR, "Erreur formulaire!")
			return redirect(index)
	else:
		form = registerForm()
	return render(request, 'socialnetwork/index.html', {'form': form})

#Vérifier si l'utilisateur est connecté
#Exclure l'utilisateur
#Exclure les utilisateurs avec qui il est déjà amis
def listUser(request):
	users  = User.objects.all().exclude(is_staff=True)
	return render(request, 'socialnetwork/listUser.html', {'users': users})

#Vérifier si l'utilisateur est connecté
#Ajouter dans la base si tous les champs sont bon
def addFriend(request):
	if request.method == 'POST':
		form = request.POST
		#if form.is_valid():

	return redirect(listUser)


