# library/views.py
import os
import shutil

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views.generic import DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings

from typing import Optional
from .models import Directory, Document


@method_decorator(login_required, name='dispatch')
class RootDirectoryView(DetailView):
    model = Directory
    template_name = 'directory_detail.html'
    context_object_name = 'directory'
    
    def get_object(self):
        # Check if there is already a root directory
        root_directory = Directory.objects.filter(parent__isnull=True).first()
        if not root_directory:
            root_directory = Directory.objects.create(name='Library', parent=None)
        return root_directory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subdirectories'] = self.object.subdirectories.all()
        context['documents'] = self.object.documents.all()
        context['parent_directories'] = self.get_parent_directories(self.object)
        return context
    
    def get_parent_directories(self, directory, parent_names=''):
        # Get the directory name and parents in reversed order
        parent_directories = []
        parent_directories.append('</ol>')
        while directory.parent:
            directory.name = '<li class="breadcrumb-item"><a href="' + f'{reverse_lazy("directory_detail", kwargs={"pk": directory.id})}' + '">' + directory.name + '</a></li>'
            parent_directories.append(directory.name)
            directory = directory.parent
        parent_directories.append('<li class="breadcrumb-item"><a href="' + f'{reverse_lazy("directory_detail", kwargs={"pk": directory.id})}' + '">' + directory.name  + '</a></li>')
        
        parent_directories.append('<ol class="breadcrumb">')
        parent_directories.reverse()
        parent_names = ''.join(parent_directories)
        print(parent_names)
        return parent_names

@method_decorator(login_required, name='dispatch')
class DirectoryDetailView(DetailView):
    model = Directory
    template_name = 'directory_detail.html'
    context_object_name = 'directory'

    def get_parent_directories(self, directory, parent_names=''):
        # Get the directory name and parents in reversed order
        parent_directories = []
        parent_directories.append('</ol>')
        while directory.parent:
            directory.name = '<li class="breadcrumb-item"><a href="' + f'{reverse_lazy("directory_detail", kwargs={"pk": directory.id})}' + '">' + directory.name + '</a></li>'
            parent_directories.append(directory.name)
            directory = directory.parent
        parent_directories.append('<li class="breadcrumb-item"><a href="' + f'{reverse_lazy("directory_detail", kwargs={"pk": directory.id})}' + '">' + directory.name  + '</a></li>')
        
        parent_directories.append('<ol class="breadcrumb">')
        parent_directories.reverse()
        parent_names = ''.join(parent_directories)
        print(parent_names)
        return parent_names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subdirectories'] = self.object.subdirectories.all()
        context['documents'] = self.object.documents.all()
        context['parent_directories'] = self.get_parent_directories(self.object)
        return context

@method_decorator(login_required, name='dispatch')
class DocumentDetailView(DetailView):
    model = Document
    template_name = 'document_detail.html'
    context_object_name = 'document'

@method_decorator(login_required, name='dispatch')
class DocumentDeleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        document = Document.objects.get(pk=pk)
        document_path = os.path.join(settings.MEDIA_ROOT, document.get_upload_path(document.name))
        
        if os.path.exists(document_path):
            print("Exist : to delete...")
            os.remove(document_path)
        document.delete()
        return redirect("directory_detail", pk=document.directory.id)

@method_decorator(login_required, name='dispatch')
class DirectoryDeleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        directory = Directory.objects.get(pk=pk)
        directory_path = os.path.join(settings.MEDIA_ROOT, directory.get_system_path())
        print("Deleting..." + directory_path)
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)

        directory.delete()
        return redirect("directory_detail", pk=directory.parent.id)

@require_POST
@login_required
def edit_directory(request, pk: int) -> HttpResponse:
    
    directory = Directory.objects.get(pk=pk)
    new_directory_name = request.POST.get('name')

    # check if the Directory already exists
    # exist = False
    # for dir in directory.parent.subdirectories.all():
    #     if dir.id != directory.id:
    #         if dir.name == new_directory_name:
    #             exist = True

    # if not exist:
    #     old_directory_path_rel = directory.get_system_path()
    #     old_directory_path = os.path.join(settings.MEDIA_ROOT, directory.get_system_path())
    #     new_directory_path = os.path.join(settings.MEDIA_ROOT, os.path.dirname(old_directory_path), new_directory_name)
        
    #     os.rename(old_directory_path, new_directory_path)
    directory.name = new_directory_name
    directory.save()
    
    #     modify_document_file_name(directory, old_directory_path_rel)
    
    return redirect("directory_detail", pk=directory.parent.id)

def modify_document_file_name(directory, old_directory_path_rel):
    for subdirectory in directory.subdirectories.all():
        modify_document_file_name(subdirectory, old_directory_path_rel + "/" + subdirectory.name)

    documents = directory.documents.all()
    for document in documents:
        document.file.name = document.file.name.replace(old_directory_path_rel, directory.get_system_path())
        document.save()


@require_POST
@login_required
def create_directory(request, parent_id: Optional[int] = None) -> HttpResponse:
    directory_name: str = request.POST.get('directory_name')
    if parent_id is None:
        root_directory = Directory.objects.filter(parent__isnull=True).first()
        if not root_directory:
            root_directory = Directory.objects.create(name='Library', parent=None)
        parent_id = root_directory
    parent = get_object_or_404(Directory, id=parent_id)
    directory = Directory.objects.create(name=directory_name, parent=parent)
    return redirect('directory_detail', parent_id)

@require_POST
@login_required
def upload_file(request, parent_id: Optional[int] = None) -> HttpResponse:
    file = request.FILES.get('file')
    if file:
        file_content = file.read()
        parent = get_object_or_404(Directory, id=parent_id)
        
        # safe_filename = os.path.basename(file.name)
        # parent = get_object_or_404(Directory, id=parent_id)
        # intended_path = os.path.join(parent.get_system_path(), safe_filename)

        # if not intended_path.startswith(parent.get_system_path()):
        #     return HttpResponseForbidden("Invalid file path.")
        
        document = Document.objects.create(name=file.name, directory=parent, file=file_content, uploaded_by=request.user)
    return redirect('directory_detail', parent_id)

def download_document(request: HttpRequest, document_id: int) -> HttpResponse:
    document = get_object_or_404(Document, id=document_id)
    response = HttpResponse(document.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.name}"'
    return response

@method_decorator(login_required, name='dispatch')
class SearchView(DetailView):
    model = Directory
    template_name = 'search_results.html'
    context_object_name = 'search_results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            directories = Directory.objects.filter(name__icontains=query)
            documents = Document.objects.filter(name__icontains=query)
            context['directories'] = directories
            context['documents'] = documents
        return context


