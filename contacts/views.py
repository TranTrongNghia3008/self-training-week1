from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from .models import Contact, Group

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contacts/list.html", {"contacts": contacts})

def contact_create(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        contact = Contact.objects.create(name=name, email=email, phone=phone)
        return redirect("contact_list")
    return render(request, "contacts/form.html")

def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.name = request.POST["name"]
        contact.email = request.POST["email"]
        contact.phone = request.POST["phone"]
        contact.save()
        return redirect("contact_list")
    return render(request, "contacts/form.html", {"contact": contact})

def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        return redirect("contact_list")
    return render(request, "contacts/confirm_delete.html", {"contact": contact})

def contact_batch_delete(request):
    if request.method == "POST":
        ids = request.POST.getlist("contact_ids")
        try:
            with transaction.atomic():
                Contact.objects.filter(id__in=ids).delete()
                messages.success(request, "Deleted selected contacts successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting contacts: {e}")
    return redirect("contact_list")