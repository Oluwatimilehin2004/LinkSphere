from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.core.mail import send_mail # type: ignore
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # type: ignore
from django.utils.encoding import force_bytes # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.core.mail import EmailMultiAlternatives # type: ignore
from django.contrib.auth.tokens import default_token_generator # type: ignore
from django.http import HttpResponse, HttpResponseRedirect # type: ignore
from django.contrib.auth.forms import SetPasswordForm # type: ignore
from accounts.models import Follow, Profile
from pages.models import Posts
from .forms import BannerUpdateForm, UserForm, ProfileForm
from .models import Profile
from django.db.models import Q


# Create your views here.
def register(request):
    if request.method== 'POST':
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        confirm_password= request.POST.get('confirm-password')

        if password== confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Already Exists')
                    return redirect('register')
                else:
                    user= User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'Account created successfully')
                    return redirect("signin")
        else:
            messages.error(request, 'Passwords do not match')
            return redirect("register")
    return render(request, "signup.html")


def signin(request):
    if request.method== 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user= authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, 'Login Sucessful')
            return redirect('feeds')
        else: 
            messages.info(request, 'Inavlid Credentials')
            return redirect('signin')
    return render(request, 'login.html')

@login_required(login_url= 'signin')
def signout(request):
    messages.info(request, 'Successfully Signed Out')
    return redirect('signin')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('password-reset-confirm')  # Fetch email from POST data
        
        try:
            user = User.objects.get(email=email)  # Check if user exists
        except User.DoesNotExist:
            return HttpResponse(f'{email} - No user with that email exists.')

        # Generate token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate reset link
        reset_link = f"{request.scheme}://{request.get_host()}/accounts/password-reset-confirm/{uid}/{token}/"

        # Prepare email content
        subject = 'Password Reset Request'
        text_content = f"Hi {user.first_name},\n\nClick the link below to reset your password:\n{reset_link}"
        html_content = render_to_string('password_reset_email.html', {'user': user, 'reset_link': reset_link})

        # Send email using EmailMultiAlternatives
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # Plain text version
            from_email='oluwatimilehinayo2004@gmail.com',  # Replace with your email
            to=[user.email],  # Recipient
        )
        email.attach_alternative(html_content, "text/html")  # Add the HTML version
        email.send()

        return redirect('password_reset_done')  # Redirect after sending the email

    return render(request, 'forgot-password.html')


def password_reset_confirm(request, uidb64, token):
    try:
        # Decode UID and fetch user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return HttpResponse("Invalid reset link.")
    
    # Check token validity
    if not default_token_generator.check_token(user, token):
        return HttpResponse("Invalid or expired token.")

    # Handle the password reset form submission
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Your password has been reset successfully.")
        else:
            return render(request, 'password-reset-confirm.html', {'form': form, 'valid_link': True})

    # If the request is GET, render the password reset confirmation form
    form = SetPasswordForm(user)
    return render(request, 'password-reset-confirm.html', {'form': form, 'valid_link': True})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

@login_required(login_url='signin')
def profile(request, id):
    user = User.objects.get(id=id)  # Profile user
    posts= Posts.objects.filter(author= user)

    # Get followers and following
    followers = User.objects.filter(following__followed=user)
    following = User.objects.filter(followers__follower=user)

    context = {
        'user': user,
        'followers': followers,
        'following': following,
        'posts': posts,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow_unfollow(request, id):
    if request.method == "POST":
        user_to_follow = User.objects.get(id=id)  
        current_user = request.user  

        action = request.POST.get('action')

        if action == 'follow':
            Follow.objects.get_or_create(follower=current_user, followed=user_to_follow)
        elif action == 'unfollow':
            Follow.objects.filter(follower=current_user, followed=user_to_follow).delete()

    return redirect('profile', id=user_to_follow.id) 


@login_required(login_url='signin')
def edit_profile(request, id):
    # Fetch the profile or return a 404 error if it doesn't exist
    profile = get_object_or_404(Profile, id=id)

    if request.method == 'POST':
        # Bind the forms with the submitted data
        user_form = UserForm(request.POST, instance=profile.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)   

        if user_form.is_valid() and profile_form.is_valid():
            # Save the forms
            print(profile_form)
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', id=profile.id )  # Redirect to the profile page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Populate the forms with the current profile and user data
        user_form = UserForm(instance=profile.user)
        profile_form = ProfileForm(instance=profile)

    # Render the edit profile template with the forms
    return render(request, 'edit-profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required(login_url= 'signin')
def edit_banner(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = BannerUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', id=profile.id)  # Redirect to the profile page after updating
    else:
        form = BannerUpdateForm(instance=profile)
    
    return render(request, 'edit_banner.html', {'form': form, 'profile': profile})

@login_required(login_url= 'signin')
def delete_acc(request, id):
    user= User.objects.get(id=id)
    user.delete()
    messages.success(request, 'Acount Succesfully Deleted!')
    return render(request, 'delete_acc.html', {'user': user})

@login_required(login_url='signin')
def search(request):
    query = request.GET.get('q', '').strip()
    user_result = Profile.objects.filter(user__username__icontains=query)
    post_result = Posts.objects.filter(content__icontains=query)
    followers = Follow.objects.filter(followed=request.user)
    
    context = {
        'query': query,
        'user_result': user_result,
        'post_result': post_result,
        'followers': followers,
    }
    return render(request, 'search.html', context)
