# library/urls.py

from django.urls import path
from .views import (
    DirectoryDetailView,
    DocumentDetailView,
    RootDirectoryView,
    DocumentDeleteView,
    DirectoryDeleteView,
)
    
from .views import (
    create_directory,
    upload_file,
    edit_directory,
    download_document,
)

urlpatterns = [
    path('', RootDirectoryView.as_view(), name='root-directory'),
    path('<uuid:pk>/', DirectoryDetailView.as_view(), name='directory_detail'),
    path('download/<uuid:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('document-delete/<uuid:pk>/', DocumentDeleteView.as_view(), name='document-delete'),
    path('document-download/<uuid:document_id>/', download_document, name='download-document'),
    path('directory-delete/<uuid:pk>/', DirectoryDeleteView.as_view(), name='directory-delete'),
    path('directory-create/<uuid:parent_id>/', create_directory, name='directory-create'),
    path('directory-edit/<uuid:pk>/', edit_directory, name='directory-edit'),
    path('file-create/<uuid:parent_id>/', upload_file, name='file-create'),
]
