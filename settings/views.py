from django.shortcuts import render, get_object_or_404, redirect
from .forms import SiteSettingsForm, RequirementStatusForm
from .models import SiteSettings
from project.models import RequirementStatus


def settings_view(request):
    # Attempt to fetch the existing settings, or None if not present
    settings_instance = SiteSettings.objects.first()

    if settings_instance is None:
        settings_instance = SiteSettings()
        settings_instance.save()

    form = SiteSettingsForm(instance=settings_instance)
    requirement_status_forms = [
        RequirementStatusForm(prefix=f"rsf_{str(i)}", instance=req_status)
        for i, req_status in enumerate(RequirementStatus.objects.all())
    ]

    if request.method == "POST":
        
        # Instantiate the form with POST data and files (for the logo)
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_instance)
        print(f"keys: ", request.POST.keys())

        # requirement_status_forms = []
        requirement_status_forms = []
        for i, rs_instance in enumerate(RequirementStatus.objects.all()):
            prefix = f'rsform-{i}'
            rs_form = RequirementStatusForm(request.POST, prefix=prefix, instance=rs_instance)
            requirement_status_forms.append(rs_form)
        
        print(requirement_status_forms)

        if form.is_valid() and all(
            [rs_form.is_valid() for rs_form in requirement_status_forms]
        ):
            form.save()
            print(requirement_status_forms)
            for rs_form in requirement_status_forms:
                print(rs_form)
                rs_form.save()
            return redirect("settings")

    # Render the template with the form context
    return render(
        request,
        "settings.html",
        {"form": form, "requirement_status_forms": requirement_status_forms},
    )
