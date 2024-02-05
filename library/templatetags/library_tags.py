import os
from django.conf import settings

from django import template

FILE_EXTENSION_COLORS = {
    'pdf': 'red',
    'doc': 'blue',
    'docx': 'blue',
    'xls': 'green',
    'xlsx': 'green',
    'ppt': 'orange',
    'pptx': 'orange',
    'txt': 'gray',
    'csv': 'darkgreen',
    'zip': 'purple',
    'rar': 'darkpurple',
    'jpg': 'gold',
    'jpeg': 'gold',
    'png': 'grey',
    'gif': 'pink',
    'mp4': 'darkblue',
    'mp3': 'lime',
    'wav': 'teal',
    'avi': 'chocolate',
    'mov': 'navy',
    'html': 'darkred',
    'css': 'royalblue',
    'js': 'yellowgreen',
    'py': 'cyan',
    'java': 'darkcyan',
    'c': 'darkgray',
    'cpp': 'lightgray',
    'xml': 'olive',
    'json': 'lightgreen',
    # ... Add more as per your requirements
}

BOOTSTRAP_ICONS = {
    'aac','ai','bmp', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'ppt', 'pptx', 'py', 'txt',  'json', 'html', 'png', 
}

register = template.Library()

@register.filter
def filename(value):
    # print(value)
    return value.name.split('/')[-1]

@register.filter(name='file_icon')
def file_icon(file_name):
    # Extract the file extension
    file_extension = os.path.splitext(file_name)[1][1:]  # [1:] to remove the dot
    if file_extension not in BOOTSTRAP_ICONS:
        return f'bi bi-file-earmark'
    return f'bi bi-filetype-{file_extension}'

@register.filter(name='file_color')
def file_color(file_name):
    file_extension = os.path.splitext(file_name)[1][1:]  # Extract the file extension without the dot
    return FILE_EXTENSION_COLORS.get(file_extension, 'black')  # Return 'default_color' if the extension is not found
