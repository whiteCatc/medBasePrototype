import bcrypt
from django.shortcuts import render, redirect
from .forms import RegistroForm
from firebase_config import db
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from firebase_admin import storage


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)  # Incluir request.FILES aquí es crucial para manejar archivos
        if form.is_valid():
            data = form.cleaned_data
            try:
                # Procesamiento de contraseña
                password_encoded = data['contraseña'].encode('utf-8')
                password_hash = bcrypt.hashpw(password_encoded, bcrypt.gensalt())

                # Registro de usuario en Firestore
                user_ref = db.collection('usuarios').document(data['curp'])
                user_data = {
                    'nombre': data['nombre'],
                    'apellidos': data['apellidos'],
                    'correo': data['correo'],
                    'contraseña': password_hash.decode('utf-8')
                }

                if 'img' in request.FILES:
                    image = request.FILES['img']
                    image_url = upload_image_to_storage(image)  # Subir imagen y obtener URL
                    user_data['imagen'] = image_url

                #Set cambiado de lugar para ingresar la imagen si es que hay
                user_ref.set(user_data)

                # Creación del expediente médico
                expediente_ref = db.collection('expedientes').document(data['curp'])
                expediente_ref.set({
                    'información_básica': {
                        'nombre': data.get('nombre'),
                    }
                })

                return redirect('login')
            except Exception as e:
                print(e)
                return render(request, 'registro.html', {'form': form, 'error': str(e)})
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def upload_image_to_storage(image_file):
    bucket = storage.bucket('medbase-37455.appspot.com')
    blob = bucket.blob(image_file.name)
    blob.upload_from_file(image_file, content_type=image_file.content_type)
    blob.make_public()
    return blob.public_url


@csrf_protect  # Asegura que la vista esté protegida contra CSRF
def login(request):
    if request.method == 'POST':
        curp = request.POST.get('curp')
        contraseña = request.POST.get('contraseña', '').encode('utf-8')
        
        if not curp or not contraseña:
            return render(request, 'login.html', {'error': 'CURP y contraseña son requeridos.'})
        
        try:
            user_ref = db.collection('usuarios').document(curp).get()
            if user_ref.exists:
                user_data = user_ref.to_dict()
                password_hash = user_data['contraseña'].encode('utf-8')
                
                if bcrypt.checkpw(contraseña, password_hash):
                    request.session['usuario'] = {
                        'nombre': user_data['nombre'],
                        'apellidos': user_data['apellidos'],
                        'correo': user_data['correo'],
                        'curp': curp,
                        'imagen': user_data.get('imagen', '')  # Añade la URL de la imagen a la sesión
                    }
                    return redirect('perfil_usuario')
                else:
                    return render(request, 'login.html', {'error': 'CURP o contraseña incorrectos'})
            else:
                return render(request, 'login.html', {'error': 'CURP o contraseña incorrectos'})
        except Exception as e:
            print(e)
            return render(request, 'login.html', {'error': 'Ha ocurrido un error al intentar iniciar sesión. Inténtalo de nuevo.'})
    return render(request, 'login.html')

def perfil_usuario(request):
    if 'usuario' in request.session:
        usuario = request.session['usuario']
        return render(request, 'perfil_usuario.html', {'usuario': usuario})
    else:
        return redirect('login')  # Redirigir al login si no hay datos de usuario en la sesión
    
def cerrar_sesion(request):
    # Limpiar la sesión
    if 'usuario' in request.session:
        del request.session['usuario']  # Elimina los datos del usuario de la sesión
    return redirect('login')  # Redirigir al usuario a la página de inicio de sesión


def verificar_sesion(request):
    # Verifica si hay datos de usuario en la sesión
    if 'usuario' in request.session:
        return JsonResponse({'sesion_activa': True})
    else:
        return JsonResponse({'sesion_activa': False})
