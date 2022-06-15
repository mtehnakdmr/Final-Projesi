#kütüphaneleri projeme dahil ettim

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.conf import settings
import random
import string
from home.forms import UploadImageForm
from .models import UploadImage

#Resim formatını kontrol eden fonksiyon
def isValidFormat(image):
    uzantılar = ["png", "jpg", "jpeg", "webp", "bmp"] #uzantı listesi
    x = image.split(".") #resim adının uzantısını ayırıyoruz
    Format = x[len(x) - 1] #resim adının uzantısını alıyoruz
    for i in uzantılar: #uzantı listesindeki uzantıları kontrol ediyoruz
        if i in Format: #uzantı varsa
            return True #format doğru
    return False #format yanlış

#Rastgele renk üreten fonksiyon
def randColor():
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) #6 karakterden oluşan hex kodu oluşturuyoruz
    return color #hex kodunu döndürüyoruz

#Rastgele karakterlerden oluşan id oluşturan fonksiyon
def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) #size değeri kadar rastgele karakter oluşturuyoruz



#Resim yükleme sayfası
def index(request):
    if request.user.is_anonymous: #Kullanıcı giriş yapmamış ise
        return redirect("/login/") #Giriş sayfasına yönlendiriyoruz
    url = id_generator(10) #Rastgele id oluşturuyoruz
    
    isUploaded = 0 #Resim yüklenmiş mi?

    if request.method == "POST": #Post isteği gelmişse
        form = UploadImageForm(request.POST, request.FILES) #Formu oluşturuyoruz
        img = request.FILES['image'].name #Resim adını alıyoruz

        unknownFormat = 0 #Resim formatı bilinmiyor mu?

        if not isValidFormat(img): #Resim formatı bilinmiyorsa
            unknownFormat = 1 #Bilinmiyor değeri 1 yapıyoruz
            return render(request, 'index.html', {'form': form, 'unknownFormat': unknownFormat, 'username': request.user, 'url': url}) #Formu gönderiyoruz

        
        if form.is_valid(): #Form geçerli ise
            form.save() #Formu kaydediyoruz
            isUploaded = 1 #Resim yüklendi değeri 1 yapıyoruz

            return render(request, 'index.html', {'form': form, 'isUploaded': isUploaded, 'username': request.user, 'url': url}) #Formu gönderiyoruz
    else: #Post isteği gelmemişse
        form = UploadImageForm() #boş form oluşturuyoruz
    return render(request, 'index.html', {'form': form, 'isUploaded': isUploaded, 'username': request.user, 'url': url}) #Formu gönderiyoruz

#Resimleri gösterme sayfası
def myimages(request):
    if request.user.is_anonymous: #Kullanıcı giriş yapmamış ise
        return redirect("/login") #Giriş sayfasına yönlendiriyoruz
        
    hostName = settings.HOSTNAME #alan adını alıyoruz
    images = UploadImage.objects.filter(uploader=request.user) #Kullanıcının yüklediği resimleri alıyoruz

    img = list(images) #Resimleri listeye çeviriyoruz
    imgNone = 0 #Resim yok mu
    imgSize = 0 #resim adının karakter sayısı
    if img == []: #Resim yoksa
        imgNone = 1 #Resim yok değeri 1 yapıyoruz
    else: #Resim varsa
        imgSize = len(img) #Resim adının karakter sayısını alıyoruz

    if request.method == "POST":#Post isteği gelmişse
        id = request.POST.get("imageID") #Resim id'sini alıyoruz
        i = UploadImage.objects.filter(id=int(id)) #Resim id'sine göre filtreyi oluşturuyoruz
        i.delete() #Resmi siliyoruz
        return redirect("/gallery/") #Galeri sayfasına yönlendiriyoruz
    return render(request, 'myimages.html', context={'images': images,'hostName': hostName, 'imgSize': imgSize, 'imgNone': imgNone, 'email': request.user.email, 'name': request.user.first_name, 'lastname': request.user.last_name, 'username': request.user}) #Resimleri gösterme sayfasını gönderiyoruz

#Giriş sayfası
def loginUser(request):
    if not request.user.is_anonymous: #Kullanıcı giriş yapmış ise
        return redirect("/")#Ana sayfaya yönlendiriyoruz
        
    if request.method == "POST": #Post isteği gelmişse
        username = request.POST.get('username') #Kullanıcı adını alıyoruz.
        password = request.POST.get('password') #Şifreyi alıyoruz
        user = authenticate(username=username, password=password) #Kullanıcıyı doğruluyoruz

        if user is not None: #Kullanıcı doğrulandıysa
            login(request, user) #Kullanıcıyı oturum açıyoruz.
            return redirect("/") #Ana sayfaya yönlendiriyoruz.

        else:#Kullanıcı doğrulanmadıysa
            durum = 0 #Kullanıcı doğrulanmadı değeri 0 yapıyoruz
            return render(request, 'login.html', context={'durum': durum}) #Giriş sayfasını gönderiyoruz

    return render(request, 'login.html') #Giriş sayfasını gönderiyoruz

#Çıkış yapma sayfası
def logoutUser(request):
    logout(request) #Kullanıcı hesabından cıkıyoruz
    return redirect("/login") #Giriş sayfasına yönlendiriyoruz

#404 sayfası
def handler404(request):
    isAnon = 0 #Kullanıcı anonim mi?
    if request.user.is_anonymous: #Kullanıcı anonim ise
        isAnon = 1 #Anonim değeri 1 yapıyoruz.
    if isAnon == 0: #Kullanıcı anonim değilse
        username = request.user #Kullanıcı adını alıyoruz.
    else:#Kullanıcı anonim ise
        username = "" #Boş değer yapıyoruz.
    return render(request, '404.html',context={'isAnon':isAnon,'username':username}) #404 sayfasını gönderiyoruz.

#resim sayfası
def image(request, *args, **kwargs):
    url = kwargs["imageURL"] #resim adresini alıyoruz
    hostName = settings.HOSTNAME #alan adını alıyoruz
    isAnon = 0 #Kullanıcı anonim mi?
    if request.user.is_anonymous: #Kullanıcı anonim ise
        isAnon = 1 #Anonim değeri 1 yapıyoruz
    if isAnon == 0: #Kullanıcı anonim değilse
        username = request.user #Kullanıcı adını alıyoruz
    else: #Kullanıcı anonim ise
        username = ""#Boş değer yapıyoruz
    images = UploadImage.objects.filter(imageURL=kwargs["imageURL"])#Resmi alıyoruz.
    c = None 
    for i in images: #Resimleri döngüye sokuyoruz
        if i.image is not None: #Resim varsa 
            a = str(i.image) #Resim dosyasını alıyoruz
            b = a.split("/") #Resim dosyasının adını alıyoruz
            c = b[len(b) - 1] #Resim dosyasının adını alıyoruz

    emColor = randColor() #Rastgele renk üretiyoruz.
    if isAnon == 0: #Kullanıcı anonim değilse
        if c is not None: #Resim varsa
            return render(request, 'image.html', context={'img': images,'hostName':hostName,'emColor':emColor, 'imgName': c}) #Resim sayfasını gönderiyoruz.
        else: #Resim yoksa
            return render(request, '404.html', context={'isAnon': isAnon,'username':username}) #404 sayfasını gönderiyoruz
    else: #Kullanıcı anonim ise
        if c is not None: #Resim varsa
            return render(request, 'image.html', context={'img': images,'hostName':hostName,'emColor':emColor, 'imgName': c}) #Resim sayfasını gönderiyoruz.
        else: #Resim yoksa
            return render(request, '404.html', context={'isAnon': isAnon,'username':username}) #404 sayfasını gönderiyoruz.

