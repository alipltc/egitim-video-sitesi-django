from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.form import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile, FAQ
from order.models import ShopCart
from video.models import Video, Category, Galeri, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Video.objects.all()[:4]
    category = Category.objects.all()
    hotvideos = Video.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    lastvideos = Video.objects.all().order_by('-id')[:5]
    context = {'setting': setting,
               'sliderdata': sliderdata,
               'category': category,
               'lastvideos': lastvideos,
               'hotvideos': hotvideos,
               'shopcart': shopcart,
               'page': 'home',}
    return render(request, 'index.html',context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    context = {'setting': setting,'shopcart': shopcart, 'page': 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def iletisim(request):

    if request.method == 'POST': # form post edildiyse
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage() # modelle bağlantı kur
            data.name = form.cleaned_data['name'] # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() #veri tabanına kaydetme
            messages.success(request, "Mesaj gönderme başarılı!")
            return HttpResponseRedirect ('/iletisim')

    setting = Setting.objects.get(pk=1)
    form=ContactForm()
    context = {'setting': setting, 'form': form}
    return render(request, 'iletisim.html',context)

def category_videos(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    videos = Video.objects.filter(category_id=id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    context = {'videos': videos,'category': category,'categorydata': categorydata,'shopcart': shopcart }
    return render(request, 'videos.html', context)

def video_detail(request,id,slug):
    category = Category.objects.all()
    video = Video.objects.get(pk=id)
    images = Galeri.objects.filter(video_id=id)
    comments = Comment.objects.filter(video_id=id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    context = {'video': video,
               'category': category,
               'images': images,
               'comments': comments,
               'shopcart': shopcart,
                }
    return render(request, 'video_detail.html', context)

def video_search(request):
    if request.method == 'POST':  # form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            videos = Video.objects.filter(title__icontains=query)

            context = {'videos': videos,
                       'category': category,
                       }
            return render(request, 'videos_search.html', context)

    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    messages.success(request, "Yine Bekleriz...")
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, "Giriş Yapıldı :) ")
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Hatalı Giriş ! | K.adı veya Şifre Yanlış!")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            #Create data in profile table
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image ="images/user/user.png"
            data.save()
            messages.success(request, "Siteye Başarılı Bir Şekilde Kayıt Oldunuz... ")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('siranumara')
    context = {'category': category,
               'faq': faq,
               }
    return render(request, 'faq.html',context)