from django import forms
from .models import Folder

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = [ 'name' ]
        
class FolderUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False, 'webkitdirectory': True, 'directory': True}))

    class Meta:
        model = Folder
        fields = ['file',]

