from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Musician, Album
from crud_app import forms
from django.db.models import Avg



def index(request):
    musician_list = Musician.objects.order_by('first_name')
    home_data = {
        'musician_list':musician_list,
        'title' : "Home Page"
    }
    return render(request, 'crud_app/index.html', context=home_data)


def musician_form(request):
    form = forms.MusicianForm()
    
    if request.method == 'POST':
        form = forms.MusicianForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Musician Addedd Successfully')
            return index(request)
    
    musician_form_data = {
        'musician_form' : form,
        'title' : "Add Musician"
    }
    return render(request, 'crud_app/musician_form.html', context=musician_form_data)




def album_list(request, artist_id):
    artist_info = Musician.objects.get(pk=artist_id)
    album_list = Album.objects.filter(artist=artist_id)
    artist_rating = Album.objects.filter(artist=artist_id).aggregate(Avg('num_stars'))
    
    album_list_data = {}
    
    
    
    album_list_data.update ({
        'artist_info' : artist_info,
        'album_list' : album_list,
        'artist_rating' :  artist_rating,
        'title' : "List of Album"
    })
    return render(request, 'crud_app/album_list.html', context=album_list_data)




def album_form(request):
    form = forms.AlbumForm()
    
    if request.method == 'POST':
        form = forms.AlbumForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        
    album_form_data = {
        'album_form' : form,
        'title' : "Add Album"
    }
    return render(request, 'crud_app/album_form.html', context=album_form_data)



def edit_artist(request, artist_id):
    artist_info = Musician.objects.get(pk=artist_id)
    form = forms.MusicianForm(instance=artist_info)
    
    if request.method == 'POST':
        form = forms.MusicianForm(request.POST, instance=artist_info)
        
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Artist Updated Successfully!')
            return index(request)
    
    artist_edit_data = {
        'edit_form' : form,
        'title': "Edit Artist"
    }
    return render(request, 'crud_app/edit_artist.html', context=artist_edit_data)




def edit_album(request, album_id):
    album_info = Album.objects.get(pk=album_id)
    form = forms.AlbumForm(instance=album_info)

    if request.method == 'POST':
        form = forms.AlbumForm(request.POST, instance=album_info)
        
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Data Updated Successfully')
            return album_list(request, artist_id=album_info.artist.id,)
             
    album_edit_data = {
        'edit_album' : form,
        'title': "Edit Album",
        'album_info' : album_info,
        'album_id' : album_id
    }
    
    return render(request, 'crud_app/edit_album.html', context=album_edit_data)



def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id).delete()
    
    delete_album_data = {
        'delete_msg' : 'Album Successfully Deleted!!',
        'title' : 'Album Delete'
        }
    
    return render(request, 'crud_app/delete.html', context=delete_album_data)


def delete_artist(request, artist_id):
    artist = Musician.objects.get(pk=artist_id).delete()
    
    delete_artist_data = {
        'delete_msg' : 'Musician Successfully Deleted!!',
        'title' : 'Artist Delete'
        }
    return render(request, 'crud_app/delete_artist.html', context=delete_artist_data)
    