from django.http import JsonResponse

def test_path(request):
    return JsonResponse({"pingpong": request})
