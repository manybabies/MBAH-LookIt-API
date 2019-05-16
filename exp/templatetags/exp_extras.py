from django import template
import json

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()

    state = kwargs.get("state")
    if state:
        updated["state"] = state

    if kwargs.get("page"):
        updated["page"] = kwargs.get("page")

    if kwargs.get("match"):
        updated["match"] = kwargs.get("match")

    if kwargs.get("sort"):
        updated["sort"] = kwargs.get("sort")

    return updated.urlencode()


@register.filter
def get_key(dictionary, key):
    return dictionary.get(key, None)


@register.simple_tag
def values_list(queryset, key):
    return json.dumps(list(getattr(obj, key) for obj in queryset))
