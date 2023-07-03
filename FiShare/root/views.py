from django.shortcuts import render
from django.views.generic import (ListView,CreateView,DeleteView)
from .models import AllFiles
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse


def home(request):
	return render(request, 'root/home.html',{'file': AllFiles.objects.all()} )


class PostListView(ListView):
    model=AllFiles
    template_name='root/all_files.html'
    context_object_name='files'
    ordering=['-created_at']

class PostCreateView(LoginRequiredMixin, CreateView):
    model = AllFiles
    fields = ['title', 'file']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        file = self.request.FILES.get('file')  # Get the uploaded file
        if file:
            form.instance.file = file  # Assign the uploaded file to the form's instance
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('all_files')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AllFiles
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner
