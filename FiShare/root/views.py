from django.shortcuts import render, redirect
from django.views.generic import (ListView,CreateView,DeleteView,TemplateView)
from .models import AllFiles,Folder
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .forms import FolderForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
import os

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
            if parent_folder:
                return redirect('subfolder',parent_folder_id=parent_folder.id)
            else:
                return redirect('all_files')

    else:
        form = FolderForm()
    return render(request, 'root/create_folder.html', {'folderform': form})


@login_required
def home(request):
	return render(request, 'root/home.html',{'file': AllFiles.objects.all()} )

class MyPostListView(ListView):
    model=AllFiles
    template_name='root/all_files.html'
    context_object_name='files'
    ordering=['-created_at']  


class MyFileFolderView(TemplateView):
    template_name = 'root/all_files.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        folder_id=None
        folder_id = self.kwargs.get('parent_folder_id')

        if folder_id:
            files = AllFiles.objects.filter(owner=self.request.user,folder=folder_id)
        else:
            files = AllFiles.objects.filter(owner=self.request.user, folder=folder_id)

        if folder_id:
            folders = Folder.objects.filter(user=self.request.user, parent_folder=folder_id)
        else:
            folders = Folder.objects.filter(user=self.request.user, parent_folder=None)


        context['files'] = files
        context['folders'] = folders
        return context


class PostListView(ListView):
    model=AllFiles
    template_name='root/user_repo.html'
    context_object_name='files'
    ordering=['-created_at']

    def get_queryset(self):
        # Get the user_id from the URL parameter
        user_id = self.kwargs['user_id']

        # Filter the files based on the user_id
        queryset = super().get_queryset().filter(owner_id=user_id)

        return queryset
    

from django.views.generic import CreateView
from .models import AllFiles, Folder

from django.urls import reverse

class PostCreateView(LoginRequiredMixin, CreateView):
    model = AllFiles
    fields = ['title', 'file']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        file = self.request.FILES.get('file')
        if file:
            form.instance.file = file

        folder_id = self.kwargs.get('parent_folder_id')
        if folder_id:
            folder = Folder.objects.get(id=folder_id)
            form.instance.folder = folder

        response = super().form_valid(form)
        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner
        
    def get_success_url(self):
        parent_folder_id = self.kwargs.get('parent_folder_id')
        if parent_folder_id:
            return reverse('subfolder', kwargs={'parent_folder_id': parent_folder_id})
        return reverse('all_files')
   


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AllFiles
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner

def download_file(request, file_path):
    # Assuming file_path is the path to the file you want to download
    file_name=os.path.basename(file_path)
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)  # Set the desired filename
    return response

