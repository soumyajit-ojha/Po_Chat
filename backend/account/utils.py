from django.core.files.base import ContentFile
import base64

from friend.models import FriendList
from .models import Account


# Utility to fetch account details
def fetch_account_details(request, user_id):
    """
    Fetch account details and friend list for the given user ID.
    """
    try:
        account = Account.objects.get(pk=user_id)
        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList.objects.create(user=account)
    except Account.DoesNotExist:
        account = None

    return account, friend_list


# Utility for handling image uploads
def handle_image_upload(account, base64_image):
    """
    Decodes and uploads a base64-encoded image for the given account.
    Deletes the old profile image if present.
    """
    format, imgstr = base64_image.split(";base64,")  # Split metadata and image data
    ext = format.split("/")[-1]  # Get file extension
    image_data = ContentFile(base64.b64decode(imgstr), name=f"cropped_image.{ext}")

    # Delete the old image
    if account.profile_image:
        account.profile_image.delete()

    # Save the new image
    account.profile_image.save(image_data.name, image_data)


from account.models import Account


def search_accounts(query):
    """
    Searches for accounts by email or username matching the query.
    """
    if not query or len(query) > 100:
        return None, "Invalid search query. Query is either empty or too long."

    search_results = Account.objects.filter(
        username__icontains=query, email__icontains=query
    ).distinct()
    return search_results, None
