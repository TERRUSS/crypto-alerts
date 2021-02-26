from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import ObjectDoesNotExist

from .serializers import SubscriptionSerializer
from .models import Subscription
from rest_framework import status

@api_view(["GET"])
def ping(request):
	content = {"message": "pong"}
	return JsonResponse(content)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])  
def ping_for_logged(request):
	content = {"message": "Welcome to the SubscriptionStore!"}
	return JsonResponse(content)


##	NOTIFICATIONS ENDPOINTS


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])  
def get_notifications(request):
	user = request.user.id
	notifs = Subscription.objects.filter(added_by=user)
	serializer = SubscriptionSerializer(notifs, many=True)
	return JsonResponse({'notifications': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_notification(request):
	payload = json.loads(request.body)
	user = request.user
	try:
		newNotif = Subscription.objects.create(
			crypto=payload["crypto"],
			ceiling=payload["ceiling"],
			alert_on_fall=payload["alert_on_fall"],
			alert_on_rise=payload["alert_on_rise"],
			added_by=user,
		)
		serializer = SubscriptionSerializer(newNotif)
		return JsonResponse({'notifs': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
	except ObjectDoesNotExist as e:
		return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
	except Exception:
		return JsonResponse({'error': 'Something terrible happened :('}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_notification(request, notif_id):
	user = request.user.id
	payload = json.loads(request.body)
	try:
		notif_item = Subscription.objects.filter(added_by=user, id=notif_id)
		# returns 1 or 0
		notif_item.update(**payload)
		notif = Subscription.objects.get(id=notif_id)
		serializer = SubscriptionSerializer(notif)
		return JsonResponse({'notif': serializer.data}, safe=False, status=status.HTTP_200_OK)
	except ObjectDoesNotExist as e:
		return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
	except Exception:
		return JsonResponse({'error': 'Something terrible happened :('}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_notification(request, notif_id):
	user = request.user.id
	try:
		notif = Subscription.objects.get(added_by=user, id=notif_id)
		notif.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	except ObjectDoesNotExist as e:
		return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
	except Exception:
		return JsonResponse({'error': 'Something terrible happened :('}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
