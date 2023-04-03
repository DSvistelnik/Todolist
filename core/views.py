from django.http import JsonResponse

def main_page(request):
    return JsonResponse({"status": "ok"}, status=200)

