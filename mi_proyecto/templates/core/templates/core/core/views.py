from django.shortcuts import render # type: ignore
from django.views.decorators.http import require_GET # type: ignore

@require_GET
def index(request):
    return render(request, 'core/index.html')