from account.models import Equipment
from django.http.response import JsonResponse

def get_equipment(request,*args, **kwargs):
    selected_runway = kwargs.get('runway')
    obj_models = list(Equipment.objects.filter(runway__runway=selected_runway).values())
    return JsonResponse({'data':obj_models})