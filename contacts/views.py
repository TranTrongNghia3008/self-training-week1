from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from collections import defaultdict
from .models import Contact, Group

def contact_list(request):
    contacts = Contact.objects.prefetch_related("groups").all()
    grouped = defaultdict(list)
    ungrouped = []

    for contact in contacts:
        if contact.groups.exists():
            for group in contact.groups.all():
                grouped[group.name].append(contact)
        else:
            ungrouped.append(contact)

    return render(request, "contacts/list.html", {
        "grouped_contacts": dict(grouped),
        "ungrouped_contacts": ungrouped
    })

def contact_create(request):
    groups = Group.objects.all()
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        group_ids = request.POST.getlist("groups")

        contact = Contact.objects.create(name=name, email=email, phone=phone)
        contact.groups.set(group_ids)

        return redirect("contact_list")
    return render(request, "contacts/form.html", {"groups": groups})

def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    groups = Group.objects.all()
    if request.method == "POST":
        contact.name = request.POST["name"]
        contact.email = request.POST["email"]
        contact.phone = request.POST["phone"]
        contact.save()

        group_ids = request.POST.getlist("groups")
        contact.groups.set(group_ids)

        return redirect("contact_list")
    return render(request, "contacts/form.html", {"contact": contact, "groups": groups})

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


def group_create(request):
    if request.method == "POST":
        name = request.POST["name"]
        if name:
            Group.objects.create(name=name)
            messages.success(request, "Group created successfully.")
            return redirect("contact_create")  # Hoặc "contact_list" tuỳ bạn
        else:
            messages.error(request, "Group name cannot be empty.")
    return render(request, "contacts/group_form.html")
