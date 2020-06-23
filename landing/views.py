from django.shortcuts import render, redirect


def landing_page(request):
    if request.user.is_authenticated:
        # if user is logged in, bring him to  his dashboard
        return redirect("account:dashboard")
    else:
        # if is new user, show landing page and let him register/login/view as guest
        return render(request, 'landing/landing_page.html', {})


# error handling pages
def page_not_found(request, exception):
    return render(request, 'landing/page_not_found.html', {})


def internal_error(request):
    return render(request, 'landing/page_not_found.html', {})