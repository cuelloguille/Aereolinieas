from .models import Mensaje

def mensajes_usuario(request):
    if request.user.is_authenticated:
        mensajes = Mensaje.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    else:
        mensajes = []
    return {'mensajes_usuario': mensajes}
