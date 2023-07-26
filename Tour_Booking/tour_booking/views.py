from django.shortcuts import render
from django.utils.translation import gettext
from django.views import generic
from .models import Tour
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {"title": gettext("Home Page")}
    return render(request, "index.html", context=context)


class TourListView(generic.ListView):
    model = Tour

class TourDetailView(generic.DetailView):
    model = Tour
