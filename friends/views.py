from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import Friend, FriendshipRequest


User = get_user_model()

@login_required
def add_friend_view(request, to_username):
    if request.method == 'POST':
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        Friend.objects.add_friend(from_user=from_user, to_user=to_user, message='')
    return render(request, 'friends/add_friend.html', {'to_user': to_user})

@login_required
def accept_friend_view(request, friendship_request_id):
    if request.method == 'POST':
        user = request.user
        friendship_request = get_object_or_404(
            FriendshipRequest.objects.filter(
                id=friendship_request_id,
                to_user=user
            )
        )
        friendship_request.accept()
    return render(request, 'friends/accept_request.html', {'to_user': user})

@login_required
def reject_friend_view(request, friendship_request_id):
    if request.method == 'POST':
        user = request.user
        friendship_request = get_object_or_404(
            FriendshipRequest.objects.filter(
                id=friendship_request_id,
                to_user=user
            )
        )
        friendship_request.reject()
    return render(request, 'friends/reject_request.html', {'to_user': user})

@login_required
def remove_friend_view(request, to_username):
    if request.method == 'POST':
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        Friend.objects.remove_friend(from_user=from_user, to_user=to_user)
    return render(request, 'friends/remove_friend.html', {'to_user': to_user})

@login_required
def unaccepted_friendship_requests_view(request):
    user = request.user
    requests = Friend.objects.unaccepted_requests(user=user)
    return render(request, 'friends/unaccepted_requests.html', {'user': user, 'requests': requests})

@login_required
def friends_list_view(request):
    user = request.user
    friends = Friend.objects.friends(user=user)
    return render(request, 'friends/friends_list.html', {'user': user, 'friends': friends})