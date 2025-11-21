from .models import FriendRequest


# Utility to get friend request status
def get_friend_request_status(sender, receiver):
    """
    Returns the status of a friend request between sender and receiver.
    """
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
        return friend_request
    except FriendRequest.DoesNotExist:
        return False

def get_friend_request(user, *args, **kwargs):
    try:
        all_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
    except FriendRequest.DoesNotExist:
        all_requests = None
    except Exception as e:
        all_requests = None

    return all_requests
