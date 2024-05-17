from django.shortcuts import render
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import Genero
from .formulario import GeneroForms

@transaction.atomic
def view(request):
    data = {}
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'agregarGenero':
            with transaction.atomic():
                form = GeneroForms(request.POST)
                if form.is_valid():
                    nombre_genero = form.cleaned_data['nombre_genero'].upper()
                    
                    try:
                        if  Genero.objects.filter(nombre_genero=nombre_genero).exists():
                            return JsonResponse({'status': 'error', 'message': 'El género ya existe en la base de datos.'})
                        genero = Genero(nombre_genero=nombre_genero)
                        genero.save()
                        messages.success(request, 'Registro guardado con éxito.')
                        return JsonResponse({'status': 'success', 'message': 'Género agregado con éxito.'})
                    except Exception as ex:
                        transaction.set_rollback(True)
                        return JsonResponse({'status': 'error', 'message': 'Error al guardar el dato.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Error en el formulario.', 'errors': form.errors})

        elif action == 'editarGenero':
            with transaction.atomic():
                form = GeneroForms(request.POST)
                if form.is_valid():
                    try:
                        genero = Genero.objects.get(pk=request.POST['id'])
                        nombre_genero = form.cleaned_data['nombre_genero'].upper()
                        if Genero.objects.filter(nombre_genero=nombre_genero).exclude(pk=genero.pk).exists():
                            return JsonResponse({'status': 'error', 'message': 'El género ya existe en la base de datos.'})
                        genero.nombre_genero = nombre_genero
                        genero.save()
                        messages.success(request, 'Registro actualizado con éxito.')
                        return JsonResponse({'status': 'success', 'message': 'Género actualizado con éxito.'})
                    except Exception as ex:
                        transaction.set_rollback(True)
                        return JsonResponse({'status': 'error', 'message': 'Error al editar el dato.'})

        elif action == 'eliminarGenero':
            try:
                genero = Genero.objects.get(pk=request.POST['id'])
                genero.delete()
                messages.success(request, 'Registro eliminado con éxito.')
                return JsonResponse({'status': 'success', 'message': 'Género eliminado con éxito.'})
            except Exception as ex:
                transaction.set_rollback(True)
                return JsonResponse({'status': 'error', 'message': 'Error al eliminar el dato.'})

    else:
        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'agregarGenero':
                try:
                    form = GeneroForms()
                    data['titulo'] = 'Agregar Género'
                    data['form'] = form
                    data['action'] = 'agregarGenero'
                    data['button_text'] = 'Agregar'
                    return render(request, 'genero/form.html', data)
                except Exception as ex:
                    pass
            
            elif action == 'editarGenero':
                try:
                    data['genero'] = genero = Genero.objects.get(pk=request.GET['id'])
                    form = GeneroForms(initial={'nombre_genero': genero.nombre_genero})
                    data['titulo'] = 'Editar Género'
                    data['form'] = form
                    data['action'] = 'editarGenero'
                    data['button_text'] = 'Guardar'
                    return render(request, 'genero/form.html', data)
                except Exception as ex:
                    pass
        else:
            data['titulo'] = 'Administración de Géneros de Libros'
            data['generos'] = Genero.objects.all()
            return render(request, 'genero/view.html', data)
