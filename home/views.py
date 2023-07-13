from django.shortcuts import render, redirect
from .forms import PDFForm
from gtts import gTTS
from datetime import datetime
import os
from deep_translator import GoogleTranslator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from translate import Translator
from home.models import SignUp
import cloudinary
import cloudinary.uploader

text=''

def HomePage(request):
    return render(request,'HomePage.html')

# Create your views here.
def SignUp1(request):
    if(request.method=='POST'):
        user=request.POST['user']
        pass1=request.POST['pass']
        email=request.POST['email']
        mob=request.POST['mob']
        s1=SignUp(us1=user,pass1=pass1,email=email,mobile=mob)
        s1.save()
        return redirect('/login')
    return render(request,'SignUp.html') 


def TextToLang(request):
    data={
            'data':''
    }
    if request.method=='POST':
        txt1=request.POST['txt1']
        txt1=txt1.strip()
        lg=request.POST['lg']
        
        textt = GoogleTranslator(source='auto', target=lg).translate(txt1)
        print (textt)
        data={
            'data':textt
        }
        return render(request,'TextToLang.html',data) 
    return render(request,'TextToLang.html',data) 

def login(request):
    if request.method=='POST':
        user=request.POST['user']
        pass1=request.POST['pass']
        s1=SignUp.objects.filter(us1=user,pass1=pass1).exists()
        if(s1==True):
            return redirect('/home')
        else:
            return render(request,'Login1.html')
    return render(request,'Login1.html')

def home(request):
    global text
    audio_url = {}

    if request.POST and request.FILES:
        lg=request.POST['lg'];
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
          link,text=  handle_pdf(request.FILES['pdf_file'],lg)
          text = GoogleTranslator(source='auto', target=lg).translate(text)
          print("MY MP3 FILE => ", link)
          audio_url = link
    else:
        form = PDFForm()

    context = {
        'form': form,
        'audio_url': audio_url.get('url'),
        'public': audio_url.get('public_id'),
        'text':text
    }
    return render(request, 'index.html', context)



def handle_pdf(pdf_file,lg):

    lg=lg
    print('############################')
    print(pdf_file)
    print('##########################')

    resource_manager = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(resource_manager, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)
    password = ""
    maxpages = 0
    caching = True

    pagenos = set()

    for page in PDFPage.get_pages(pdf_file, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    text=text
    print(text)

    device.close()
    retstr.close()
    return  convert_to_mp3(text,lg)



def convert_to_mp3(text,lg):
    the_mp3 = gTTS(text=text, lang=lg)
    now = datetime.now()
    today = now.strftime("%d_%m_%Y_%H:%M:%S")
    filename = "files/"+'abc1'+".mp3"
    the_mp3.save(filename)


    cloudinary.config(
                cloud_name = 'deurbvxwp',  
                api_key = '368636563326952',  
                api_secret = 'sXNEaXFV1iQAk-Jr8WFUgdzBLII'  
                )
    cloud =  cloudinary.uploader.upload(filename, resource_type='raw')     
    print(cloud) 


     
    if cloud:
        audio_link = {
                        'public_id': cloud.get('public_id'),
                        'url': cloud.get('secure_url')
                    }
        os.remove(filename)

    return audio_link,text


def download(request):
    link = request.GET['link']
    print("THIS IS THE LINK +++>", link)
        
    return redirect('home')