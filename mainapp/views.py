import json
import sys
import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from integrations.collector import collect

from .forms import IntegrationInstanceForm
from .models import IntegrationInstance, Measurement, Metric, User


def collect_integration(integration_instance):
    # TODO: Read secrets from store
    import os

    secrets = {"PLAUSIBLE_API_KEY": os.environ["PLAUSIBLE_API_KEY"]}
    config = json.loads(integration_instance.config)
    return collect(integration_instance.integration_id, config=config, secrets=secrets)


@login_required
def index(request):
    data = {
        m: Measurement.objects.all().filter(metric=m)
        for m in Metric.objects.all().filter(user=request.user)
    }
    return HttpResponse(
        "<br />".join(
            [f"{k}: [{','.join([str(v) for v in v])}]" for k, v in data.items()]
        )
    )


@login_required
def integration_instance_collect(request, integration_instance_id):
    integration_instance = get_object_or_404(
        IntegrationInstance, pk=integration_instance_id, metric__user=request.user
    )
    try:
        measurement = collect_integration(integration_instance)
        # TODO: Should this route change the DB?
        # Should it be another VERB?
        # Measurement.objects.update_or_create(
        #     metric=integration_instance.metric,
        #     date=measurement.date,
        #     defaults={"value": measurement.value},
        # )
    except Exception as e:
        import sys
        import traceback

        exc_info = sys.exc_info()
        return JsonResponse(
            {
                "error": "\n".join(traceback.format_exception(*exc_info)),
                "status": "error",
            },
            status=500,
        )
    return JsonResponse(
        {
            "measurement": measurement,
            "status": "ok",
        }
    )


@login_required
def integration_instance(request, integration_instance_id):
    integration_instance = get_object_or_404(
        IntegrationInstance, pk=integration_instance_id, metric__user=request.user
    )

    integration_error = None
    measurement = None
    if request.POST:
        # TODO: use generic views instead
        # from django.views import generic
        # https://docs.djangoproject.com/en/4.1/intro/tutorial04/#use-generic-views-less-code-is-better
        integration_instance.config = request.POST["config"]
        integration_instance.secrets = request.POST["secrets"]
        # Hack. TODO: Fix
        if (integration_instance.config or "null") == "null":
            integration_instance.config = None
        if (integration_instance.secrets or "null") == "null":
            integration_instance.secrets = None
        # Test the integration before saving it
        try:
            measurement = collect_integration(integration_instance)
        except Exception as e:
            exc_info = sys.exc_info()
            integration_error = "\n".join(traceback.format_exception(*exc_info))
        # If the test is conclusive, save
        if measurement:
            integration_instance.save()

    # show edit page
    form = IntegrationInstanceForm(instance=integration_instance)

    from django.template import RequestContext, Template

    template = Template(
        """
{% extends "base.html" %}
{% block content %}
  <form action="" method="post">
    {% csrf_token %}
    {{ form.media }}
    {{ form }}
    <input type="submit" value="Test and save">
    <p>
        {% if integration_error %}
        <div style="color: red">Error while collecting integration. Settings have not been saved.<br/><pre>{{ integration_error }}</pre></div>
        {% else %}
        <div style="color: green">Integration returned {{ measurement }}. Settings have been saved.</div>
        {% endif %}
    </p>
  </form>
{% endblock %}
        """
    )
    context = RequestContext(
        request,
        {
            "form": form,
            "integration_error": integration_error,
            "measurement": measurement,
        },
    )
    return HttpResponse(template.render(context))
