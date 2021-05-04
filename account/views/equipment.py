from account.models import Equipment
from django.http.response import JsonResponse

def get_equipment(request,id):
    selected_runway = id
    obj_models = list(Equipment.objects.filter(runway_id=selected_runway).values())
    return JsonResponse({'data':obj_models})