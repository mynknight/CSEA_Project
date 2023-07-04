from django.shortcuts import render, redirect
from django.views.generic import (ListView,CreateView,DeleteView)
from .models import AllFiles,Folder
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .forms import FolderForm
from django.contrib.auth.decorators import login_required


@login_required
def create_folder(request, parent_folder_id=None):
    parent_folder=None
    if parent_folder_id:
        parent_folder = Folder.objects.get(id=parent_folder_id)
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user  # Set the user for the folder
            folder.parent_folder = parent_folder 
            folder.save()
            return redirect('all_files')
    else:
        form = FolderForm()
    return render(request, 'root/all_files.html', {'folderform': form})


@login_required
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
