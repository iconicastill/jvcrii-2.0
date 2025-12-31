from .models import Cliente

def total_clientes(request):
    return {
        'total_clientes': Cliente.objects.count()
    }
