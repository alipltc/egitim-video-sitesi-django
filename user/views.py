from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from home.models import UserProfile
from order.models import ShopCart, Order, OrderVideo
from user.forms import UserUpdateForm, ProfileUpdateForm
from video.models import Comment, Video, Videoglr


def index(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context ={'profile': profile,'shopcart': shopcart, }

    return render(request,'user_profile.html',context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil Güncelleme Başarılı!')
            return redirect('/user')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {'user_form': user_form,
                   'profile_form': profile_form,
                   }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Plase correct the arror below.')
            return HttpResponseRedirect('/user/password')

    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form,
        })
    

@login_required(login_url='/login')
def comments(request):
    user = request.user
    current_user = UserProfile.objects.get(user_id=user.id)
    comments = Comment.objects.filter(user_id=user.id)
    context = {'profile': current_user,
               'comments': comments,
               }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request,id):
    user = request.user
    current_user = UserProfile.objects.get(user_id=user.id)
    Comment.objects.filter(id=id, user_id=user.id).delete()
    messages.success(request, 'Yorumunuz Kaldırıldı.')
    context = {'profile': current_user,
               }
    return HttpResponseRedirect('/user/comments', context)

@login_required(login_url='/login')
def orders(request):
    current_user = request.user
    order= Order.objects.all()
    orderitems = OrderVideo.objects.filter(user_id=current_user.id, status="Open")
    context = {'order': order,
               'orderitems': orderitems,
               }
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login')
def orderdetail(request,id):
    current_user = request.user
    order = Order.objects.all()
    ordervideo = OrderVideo.objects.get(id=id)
    ordervideodetail = Video.objects.filter(id=id)
    videos = Videoglr.objects.filter(video_id=id)
    context = {'ordervideodetail': ordervideodetail,
               'ordervideo': ordervideo,
               'order': order,
               'videos': videos,
               }
    return render(request, 'user_video_detail.html', context)
