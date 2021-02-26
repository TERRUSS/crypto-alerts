from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import status


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def deleteAccount(request):
	print("DELETING ACCOUNT", request.user)
	user = request.user
	user.delete()
	
	return JsonResponse({'message': 'Roger, account terminated.'}, safe=False, status=status.HTTP_201_CREATED)
