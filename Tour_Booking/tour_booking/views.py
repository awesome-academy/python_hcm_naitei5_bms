from django.shortcuts import render, redirect
from django.utils.translation import gettext
from django.views import generic
from .models import Tour
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    context = {"title": gettext("Home Page")}
    return render(request, "index.html", context=context)


class TourListView(generic.ListView):
    model = Tour

class TourDetailView(generic.DetailView):
    model = Tour



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            return render(request, 'login.html', {'error_message': 'Đăng nhập không thành công. Vui lòng thử lại.'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')
