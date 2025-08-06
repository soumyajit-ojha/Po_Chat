from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse
from account.forms import RegistrationForm, LoginForm, AccountUpdateForm
from django.conf import settings
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendRequest, FriendList
from .models import Account
from .models import get_default_profile_image as default_image_path

# Import utilities
from .utils import fetch_account_details, handle_image_upload, search_accounts
from friend.utils import get_friend_request, get_friend_request_status


def registration_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}")

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("home")
        else:
            context['registration_form'] = form

    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid email or password.")
        context['login_form'] = form
    else:
        context['login_form'] = LoginForm()

    return render(request, 'account/login.html', context)


def account_view(request, *args, **kwargs):
    user = request.user
    receiver_user_id = kwargs.get("user_id")
    account, friend_list = fetch_account_details(request, receiver_user_id)
    friends = friend_list.friends.all()
    
    context = {
        "user_id": account.id,
        "username": account.username,
        "email": account.email,
        "profile_image": account.profile_image.url,
        "hide_email": account.hide_email,
        "friends": friends,
        "is_self": user == account,
        "is_friend": False,
        "BASE_URL": settings.BASE_URL,
        "request_sent" : FriendRequestStatus.NO_REQUEST_SENT.value,
        "friend_requests" : get_friend_request(user),
        "pending_friend_request_id" : None
    }

    if user.is_authenticated and user != account:
        context["is_friend"] = friends.filter(pk=user.id).exists()
        if get_friend_request_status(sender=account, receiver=user) :
            context['request_sent'] = FriendRequestStatus.THEM_SENT_TO_YOU.value
            context['pending_friend_request_id'] = FriendRequest.objects.get(sender=account, receiver=user, is_active=True)
            
        elif get_friend_request_status(sender=user, receiver=account) :
            context['request_sent'] = FriendRequestStatus.YOU_SENT_TO_THEM.value    

    return render(request, 'account/account.html', context=context)


def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = kwargs.get('user_id')
    account = get_object_or_404(Account, pk=user_id)

    if account.pk != request.user.pk:
        return HttpResponse("You can't edit someone else's account.", status=403)

    context = {}
    if request.method == "POST":
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if account.profile_image and account.profile_image.path != default_image_path:
                    account.profile_image.delete()
            form.save()
            return redirect('account', user_id=account.pk)
        else:
            context["form_errors"] = form.errors
    else:
        form = AccountUpdateForm(instance=request.user)

    context["form"] = form
    context["MAX_PHOTO_SIZE"] = settings.MAX_PHOTO_SIZE

    return render(request, 'account/edit_account.html', context=context)


def upload_cropped_image(request):
    if request.method == "POST":
        try:
            data_url = request.POST.get('image')
            if not data_url:
                return JsonResponse({"success": False, "error": "No image data provided."}, status=400)

            handle_image_upload(request.user, data_url)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)

def account_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")

        # Use utility to perform the search
        search_results, error = search_accounts(search_query)
        if error:
            context['error'] = error
        else:
            user = request.user
            accounts = []       # [(account_obj, is_friend), ....]

            if user.is_authenticated:
                auth_user_friend_list = FriendList.objects.get(user=user)
                for account in search_results:
                    # Placeholder for mutual friend check if implemented
                    accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
            else:
                for account in search_results:
                    accounts.append((account, False))

            context['accounts'] = accounts

    return render(request, "account/search_results.html", context)
