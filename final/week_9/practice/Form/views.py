from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import *
from django.core.mail import send_mail
from .forms import NameForm, ContactForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data["your_name"])
            return HttpResponse("Form submitted! for " + form.cleaned_data["your_name"])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "name.html", {"form": form}) 

def contact_us(request):

    if request.method == "POST":
        # bind data to form
        form = ContactForm(request.POST)
        # validate data in the form
        if form.is_valid():
            # access cleaned_data
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            print("Subject", subject)
            print("Message", message)
            print("Sender", sender)
            print("CC myself?", cc_myself)

            # Assume that this view send email
            recipients = ["info@example.com"]
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)

            # redirect to "thanks" page when the email has been sent
            return redirect("thanks")
    else:
        form = ContactForm()
    
    return render(request, "contact_us.html", {"form": form})

def thanks(request):
    return HttpResponse("THANKS!!!")

