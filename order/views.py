from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile
from order.models import ShopCart, OrderForm, Order, OrderVideo
from video.models import Category, Video


def index(request):
    return HttpResponse("Order App")

@login_required(login_url='/login')
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkuser = ShopCart.objects.filter(user_id=current_user.id,video_id=id)
    if checkuser:
        control = 1# Ürün sepette var
    else:
        control = 0# Ürün sepette yok
    if id:
        if control == 0:
            data = ShopCart() # modelle bağlantı kur
            data.user_id = current_user.id
            data.video_id = id
            data.quantity = 1
            data.save() #veri tabanına kaydetme
            messages.success(request, "Video Sepete Eklendi!")
        else:
            messages.warning(request, "Uyarı! Ürün Sepette Zaten Mevcut!")

    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    current_user = request.user
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    total=0

    for rs in shopcart:
        total += rs.video.price

    context = {'shopcart': shopcart,
               'category': category,
               'profile': current_user,
               'total': total,}
    return render(request, 'Shopcart_videos.html',context)

@login_required(login_url='/login')
def deleteshopcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Video Sepetten Silindi!")
    return HttpResponseRedirect("/shopcart")

@login_required(login_url='/login')
def ordervideo(request):
    current_user = request.user
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.video.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data =  Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(12).upper
            data.code = ordercode
            data.save()

            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderVideo()
                detail.order_id = data.id #order id
                detail.video_id = rs.video_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                #-----------------
                video = Video.objects.get(id=rs.video_id)
                video.amount -= rs.quantity
                video.save()
                # -----------------
                detail.price = rs.video.price
                detail.amount = rs.amount
                detail.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items']=0
            messages.success(request, "Satın Alım Başarılı. Teşekkür Ederiz")
            return render(request, 'Order_Completed.html',{'ordercode': ordercode,'category': category})
        else:
            messages.success(request, form.errors)
            return HttpResponseRedirect("/order/ordervideo")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id = current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'profile': profile,
               'form': form,
               'total': total, }
    return render(request, 'Order_Form.html', context)
