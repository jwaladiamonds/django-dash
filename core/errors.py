from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'error/404.html')


def permission_denied(request, exception):
    return render(request, 'error/500.html')

def bad_request(request, exception):
    return render(request, 'error/500.html')
    
def server_error(request):
    return render(request, 'error/500.html')
