from django.shortcuts import render


def error_500_view(request, *args, **argv):
    return render(
        request,
        "500.html",
        {},
        status=500,
    )
