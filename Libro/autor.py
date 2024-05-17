from django.shortcuts import render
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from Libro.models import Autor
from .formulario import AutorForms


@transaction.atomic
def view(request):
    data = {}
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'agregarAutor':
            with transaction.atomic():
                form = AutorForms(request.POST)
                if form.is_valid():
                    nombre = form.cleaned_data['nombre'].upper()
                    apellido = form.cleaned_data['apellido'].upper()

                    try:
                        if Autor.objects.filter(nombre=nombre, apellido=apellido).exists():
                            return JsonResponse(
                                {'status': 'error', 'message': 'El autor ya existe en la base de datos.'})
                        autor = Autor(nombre=nombre, apellido=apellido,
                                      fecha_nacimiento=form.cleaned_data['fecha_nacimiento'])
                        autor.save(request)
                        messages.success(request, 'Registro guardado con éxito.')
                        return JsonResponse({'status': 'success', 'message': 'Autor agregado con éxito.'})
                    except Exception as ex:
                        transaction.set_rollback(True)
                        return JsonResponse({'status': 'error', 'message': 'Error al guardar el dato.'})
                else:
                    return JsonResponse(
                        {'status': 'error', 'message': 'Error en el formulario.', 'errors': form.errors})

        elif action == 'editarAutor':
            with transaction.atomic():
                form = AutorForms(request.POST)
                if form.is_valid():
                    try:
                        autor = Autor.objects.get(pk=request.POST['id'])
                        nombre = form.cleaned_data['nombre'].upper()
                        apellido = form.cleaned_data['apellido'].upper()
                        if Autor.objects.filter(nombre=nombre, apellido=apellido).exclude(pk=autor.pk).exists():
                            return JsonResponse(
                                {'status': 'error', 'message': 'El autor ya existe en la base de datos.'})
                        autor.nombre = nombre
                        autor.apellido = apellido
                        autor.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                        autor.save()
                        messages.success(request, 'Registro actualizado con éxito.')
                        return JsonResponse({'status': 'success', 'message': 'Autor actualizado con éxito.'})
                    except Exception as ex:
                        transaction.set_rollback(True)
                        return JsonResponse({'status': 'error', 'message': 'Error al editar el dato.'})

        elif action == 'eliminarAutor':
            try:
                autor = Autor.objects.get(pk=request.POST['id'])
                autor.delete()
                messages.success(request, 'Registro eliminado con éxito.')
                return JsonResponse({'status': 'success', 'message': 'Autor eliminado con éxito.'})
            except Exception as ex:
                transaction.set_rollback(True)
                return JsonResponse({'status': 'error', 'message': 'Error al eliminar el dato.'})

    else:
        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'agregarAutor':
                try:
                    form = AutorForms()
                    data['titulo'] = 'Agregar Autor'
                    data['form'] = form
                    data['action'] = 'agregarAutor'
                    data['button_text'] = 'Agregar'
                    return render(request, 'autor/form.html', data)
                except Exception as ex:
                    pass

            elif action == 'editarAutor':
                try:
                    data['autor'] = autor = Autor.objects.get(pk=request.GET['id'])
                    form = AutorForms(initial={'nombre': autor.nombre, 'apellido': autor.apellido,
                                               'fecha_nacimiento': autor.fecha_nacimiento})
                    data['titulo'] = 'Editar Autor'
                    data['form'] = form
                    data['action'] = 'editarAutor'
                    data['button_text'] = 'Guardar'
                    return render(request, 'autor/form.html', data)
                except Exception as ex:
                    pass
        else:
            data['titulo'] = 'Administración de Autores de Libros'
            data['autores'] = Autor.objects.all()
            return render(request, 'autor/view.html', data)
