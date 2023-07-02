from django.shortcuts import render
from django.views.generic import ListView
from .models import AllFiles

def home(request):
	return render(request, 'root/home.html',{'posts': AllFiles.objects.all()} )


class PostListView(ListView):
    model=AllFiles
    template_name='root/home.html'
    context_object_name='allfiles'
    ordering=['-created_at']