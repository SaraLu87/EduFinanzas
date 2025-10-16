from django.shortcuts import render, redirect
from .forms import TemaForm

# Lista temporal
temas_lista = []
tema_id_counter = 1

def buscar_tema_por_id(id_tema):
    for tema in temas_lista:
        if tema['id'] == id_tema:
            return tema
    return None


# LISTAR
def tema_listar(request):
    return render(request, 'home/temas/tema_lista.html', { 
        'temas': temas_lista
    })


# CREAR
def tema_crear(request):
    global tema_id_counter
    if request.method == 'POST':
        formulario = TemaForm(request.POST)
        if formulario.is_valid():
            nuevo_tema = {
                'id': tema_id_counter,
                'nombre': formulario.cleaned_data['nombre'],
                'descripcion': formulario.cleaned_data['descripcion']
            }
            temas_lista.append(nuevo_tema)
            tema_id_counter += 1
            return redirect('tema_listar')
    else:
        formulario = TemaForm()

    return render(request, 'home/temas/tema_form.html', { 
        'formulario': formulario,
        'accion': 'Crear'
    })


# EDITAR
def tema_editar(request, id):
    tema = buscar_tema_por_id(id)
    if not tema:
        return redirect('tema_listar')

    if request.method == 'POST':
        formulario = TemaForm(request.POST)
        if formulario.is_valid():
            tema['nombre'] = formulario.cleaned_data['nombre']
            tema['descripcion'] = formulario.cleaned_data['descripcion']
            return redirect('tema_listar')
    else:
        formulario = TemaForm(initial={
            'nombre': tema['nombre'],
            'descripcion': tema['descripcion']
        })

    return render(request, 'home/temas/tema_form.html', {
        'formulario': formulario,
        'accion': 'Editar'
    })


# ELIMINAR
def tema_eliminar(request, id):
    tema = buscar_tema_por_id(id)
    if not tema:
        return redirect('tema_listar')

    if request.method == 'POST':
        temas_lista.remove(tema)
        return redirect('tema_listar')

    return render(request, 'home/temas/tema_confirmar_eliminar.html', {  
        'tema': tema
    })
