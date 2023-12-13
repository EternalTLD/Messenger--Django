from django.http import JsonResponse, HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET

from .models import Friend, FriendshipRequest
from .utils import parse_json_request


User = get_user_model()


@login_required
@require_POST
def accept_request_view(request: HttpRequest) -> JsonResponse:
    friendship_request_id = parse_json_request(request)
    friendship_request = get_object_or_404(
        FriendshipRequest, id=friendship_request_id, to_user=request.user
    )
    friendship_request.accept()

    return JsonResponse({"Status": "Accepted"})


@login_required
@require_POST
def reject_request_view(request: HttpRequest) -> JsonResponse:
    friendship_request_id = parse_json_request(request)
    friendship_request = get_object_or_404(
        FriendshipRequest, id=friendship_request_id, to_user=request.user
    )
    friendship_request.reject()

    return JsonResponse({"Status": "Rejected"})


@login_required
def unaccepted_requests_view(request: HttpRequest) -> HttpResponse:
    requests = Friend.objects.unaccepted_requests(user=request.user)

    return render(
        request,
        "friends/unaccepted_requests.html",
        {"user": request.user, "requests": requests},
    )


@login_required
def rejected_requests_view(request: HttpRequest) -> HttpResponse:
    requests = Friend.objects.rejected_requests(user=request.user)

    return render(
        request,
        "friends/rejected_requests.html",
        {"user": request.user, "requests": requests},
    )


@login_required
@require_POST
def add_friend_view(request: HttpRequest) -> JsonResponse:
    user_id = parse_json_request(request)
    to_user = User.objects.get(id=user_id)
    Friend.objects.add_friend(from_user=request.user, to_user=to_user)

    return JsonResponse({"Status": "Added"})


@login_required
@require_POST
def remove_friend_view(request: HttpRequest) -> JsonResponse:
    friend_id = parse_json_request(request)
    to_user = User.objects.get(id=friend_id)
    Friend.objects.remove_friend(from_user=request.user, to_user=to_user)

    return JsonResponse({"Status": "Removed"})


@login_required
def friend_list_view(request: HttpRequest) -> HttpResponse:
    friends = Friend.objects.friends(user=request.user)

    return render(
        request, "friends/friend_list.html", {"user": request.user, "friends": friends}
    )


@login_required
@require_GET
def search_friend_view(request: HttpRequest) -> HttpResponse:
    friends = []
    query = request.GET.get("query")
    if query:
        friends = Friend.objects.friends(user=request.user).filter(
            from_user__username__icontains=query
        )

    return render(
        request, "friends/friend_list.html", {"user": request.user, "friends": friends}
    )
