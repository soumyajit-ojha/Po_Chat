from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import FriendRequest, FriendList
from account.models import Account
from .utils import get_friend_request

class AllFriends(View):
    def get(self, request, *args, **kwargs):
        # Authenticated User
        user = request.user
        user_id = kwargs.get("user_id")
        context = {}

        if not user.is_authenticated:
            return JsonResponse({"response" : "You are not authenticated as a valid user."}, status=403)
        if not user_id:
            return JsonResponse({"response" : "User ID missing, must required."}, status=400)
        
        # this_account_holder = this user/ current_user
        try:
            current_user = Account.objects.get(pk=user_id) 
            context['this_user'] = current_user
        except Account.DoesNotExist:
            return JsonResponse({"response":"Account no longer exist."}, status=404)
        # friends of current user
        try:
            friends_list = FriendList.objects.get(user=current_user)
        except FriendList.DoesNotExist:
            return render(request, '404.html')
            return JsonResponse({"response":"No Friends Found."}, status=404)

        if user != current_user:
            if not user in friends_list.friends.all():
                return render(request, '403.html')
                return JsonResponse({"response" : "You were not friends, you can's see."}, status=403)
            
        auth_user_friend_list = FriendList.objects.get(user=user)
        # print(auth_user_friend_list)
        friends = []
        for friend in friends_list.friends.all():
            friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
        context['friends'] = friends
        
        return render(request, "friend/friend_list.html", context)

class SendFriendRequest(View):
    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'message': 'You must be logged in to send a friend request.'}, status=401)

        user_id = request.POST.get('receiver_user_id')
        if not user_id:
            return JsonResponse({'message': 'Unable to send request. Missing receiver ID.'}, status=400)

        try:
            receiver = Account.objects.get(pk=user_id)
            # Check for existing friend request
            if FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True).exists():
                return JsonResponse({'message': 'You have already sent them a friend request.'}, status=400)

            # Create a new friend request
            FriendRequest.objects.create(sender=user, receiver=receiver, is_active=True)
            return JsonResponse({'message': 'Friend request sent successfully.'}, status=200)

        except Account.DoesNotExist:
            return JsonResponse({'message': 'Account not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

class AllFriendRequest(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {}

        if not user.is_authenticated:
            return redirect("login")
        account_id = kwargs.get('user_id')
        try:
            account = Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            return HttpResponse({"message":"Account doesn't exist"}, status=404)
        if user != account:
            HttpResponse({"message":"You can't see others friends"}, status=403)

        context["friend_requests"] = get_friend_request(user=user)

        return render(request, "friend/friend_requests.html", context)
        
class AcceptFriendRequest(View):
    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({"message" : "You have no access for this action."}, status=403)
        
        friend_request_id = kwargs.get("friend_request_id")
        try:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)


        except FriendRequest.DoesNotExist:
            return JsonResponse({"message" : "Friend request doesn't found."}, status=404)

        except Exception as e:

            return JsonResponse({"message":"Failed to accept."})

        if friend_request.receiver != user:
            JsonResponse({"message" : "You have no access to do this action."}, status=403)
        try:
            friend_request.accept()

            return JsonResponse({"response": "Accepted successfully."})
        except Exception as e:

            return JsonResponse({"response": "Error occurred while accepting the request."}, status=500)

class Unfriend(View):
    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({"response":"You need to be logged in to perform this action."}, status=403)

        removee_id = request.POST.get('removee_id')
        if not removee_id:
            return JsonResponse({"response" : "Removee id not provided."}, status=400)

        try:
            removee = Account.objects.get(pk=removee_id)

        except Account.DoesNotExist:
            return JsonResponse({"response" : "User to unfriend doesn't exixt."}, status=404)
        
        except Exception as e:
            return JsonResponse({'response' : f'Error found{str(e)}'}, status=400)
        
        try:
            Own_friend_list = FriendList.objects.get(user=user)
            Own_friend_list.unfriend(removee=removee)
            return JsonResponse({'response' : f'Successfuly unfriend {removee.username}'}, status=200)
        
        except FriendList.DoesNotExist:
            return JsonResponse({"response":"Friend list doesn't found for current user."})
        
        except Exception as e:
            return JsonResponse({'response':f'Error found: {str(e)}'}, status=400)

class DeclineFriendRequest(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"response" : "You don't have permission to do this."}, status=403)
        
        friend_request_id = kwargs.get('friend_request_id')
        if not friend_request_id:
            return JsonResponse({"response" : "Friend request id missing."}, status=404)
        try :
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver != user:
                return JsonResponse({"You are not authorized to decline requests."}, status=403)
            friend_request.decline()
            return JsonResponse({"response" : "Request declined."}, status=200)

        except Exception as e:
            return JsonResponse({"response" : f"Error raised: {str(e)}"}, status=200)

class CancelFriendRequest(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"response": "You must be logged in to cancel a friend request."}, status=403)

        receiver_user_id = request.POST.get("receiver_user_id")
        if not receiver_user_id:
            return JsonResponse({"response": "Receiver user ID is required to cancel the friend request."}, status=400)

        try:
            receiver = Account.objects.get(pk=receiver_user_id)
        except Account.DoesNotExist:
            return JsonResponse({"response": "Receiver account not found."}, status=404)

        # Retrieve active friend requests
        friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
        if not friend_requests.exists():
            return JsonResponse({"response": "No active friend request found to cancel."}, status=404)
        
        for friend_request in friend_requests:
            friend_request.cancel()

        return JsonResponse({"response": "Friend request(s) canceled successfully."}, status=200)