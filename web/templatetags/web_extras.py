import textwrap
from typing import Text

from django import template
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from accounts.forms import StudyListSearchForm
from accounts.queries import get_child_eligibility, get_child_participation_eligibility
from project.settings import GOOGLE_TAG_MANAGER_ID

register = template.Library()


def format(text: Text) -> Text:
    if GOOGLE_TAG_MANAGER_ID:
        return mark_safe(textwrap.dedent(text))
    else:
        return ""


def active_nav(request, url) -> bool:
    """Determine is this button is the active button in the navigation bar.

    Args:
        request (Request): Request object from template
        url (Text): String url for the current view

    Returns:
        boolean: returns true if this path is active
    """
    return request.path == url


def nav_next(request, url, text, button):
    """Create form that will submit the current page as the "next" query arg.

    Args:
        request (Request): Request object submitted from template
        url (Text): Target URL
        text (Text): String to be displayed is button
        button (bool): Is this to be styled as a button or as a link

    Returns:
        SafeText: Returns html form used to capture current view and submit it as the "next" query arg
    """
    active = active_nav(request, url)

    if button:
        css_class = "btn btn-light link-secondary border-secondary text-center"
    elif active:
        css_class = "btn active btn-light link-secondary text-center"
    else:
        css_class = "nav-link navbar-link link-secondary border-0 text-center"

    form = f"""<form action="{url}" method="get">
    <button class="{css_class}" type="submit" value="login">{_(text)}</button>
    <input type="hidden" name="next" value="{request.path}" />
    </form>"""

    if not button:
        form = f"""<li>{form}</li>"""

    return mark_safe(form)


@register.simple_tag
def child_is_valid_for_study_criteria(child, study):
    eligibility = {
        "participation_eligibility": get_child_participation_eligibility(child, study),
        "criteria_expression_eligibility": get_child_eligibility(
            child, study.criteria_expression
        ),
    }
    return eligibility


@register.simple_tag
def google_tag_manager() -> Text:
    return format(
        f"""
    <!-- Google tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_TAG_MANAGER_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GOOGLE_TAG_MANAGER_ID}');
    </script>
    """
    )


@register.simple_tag
def nav_link(
    request,
    url_name,
    text,
    html_classes=None,
    queryString=None,
    list=False,
    reverse_url=True,
):
    """General navigation bar item

    Args:
        request (Request): Reqeust submitted from template
        url_name (Text): Name of url to be looked up by reverse
        text (Text): Text to be displayed in item
        html_classes (Array): optional list of one or more classes for the <a> element
        queryString (Text): optional query string to be appended to the end of URL
        list (Boolean): should the nav links be inside <li> elements? (default is False)
        reverse_url (Boolean): Should 'url_name' be reversed? Defaults to True. Set to False when using a URL generated by the url template tag.

    Returns:
        SafeText: HTML of navigation item
    """
    if html_classes is None:
        html_classes = [
            "nav-link",
            "navbar-link",
            "link-secondary",
            "text-center",
            "px-3",
        ]
    if reverse_url:
        url = reverse(url_name)
    else:
        url = url_name
    aria_current = ""
    if active_nav(request, url):
        html_classes.extend(["active", "btn-secondary"])
        aria_current = ' aria-current="page"'
    if queryString:
        url = url + queryString
    nav_a_tag = (
        f'<a class="{" ".join(html_classes)}"{aria_current} href="{url}">{_(text)}</a>'
    )

    if list:
        return mark_safe(f'<li class="nav-item">{nav_a_tag}</li>')
    else:
        return mark_safe(nav_a_tag)


@register.simple_tag
def dropdown_item(request, url_name, text):
    return nav_link(request, url_name, text, ["dropdown-item"])


@register.simple_tag
def nav_login(request, text="Login", button=False):
    """Navigation login button

    Args:
        request (Request): Request object submitted by template
        text (str, optional): Text to be shown in button. Defaults to "Login".
        button (bool, optional): Is this to be styled as a button or as a link. Defaults to False.

    Returns:
        SafeText: HTML form
    """
    url = reverse("login")
    return nav_next(request, url, text, button)


@register.simple_tag
def nav_signup(request, text="Sign up", button=False):
    """Navigation sign up button

    Args:
        request (Request): Request object submitted by template
        text (str, optional): Text to be shown in button. Defaults to "Login".
        button (bool, optional): Is this to be styled as a button or as a link. Defaults to False.

    Returns:
        SafeText: HTML form
    """
    url = reverse("web:participant-signup")
    return nav_next(request, url, text, button)


@register.simple_tag
def studies_tab_text(tabs):
    for tab in tabs:
        if tab.data["selected"]:
            value = tab.data["value"]
            if value == StudyListSearchForm.Tabs.all_studies.value[0]:
                return _(
                    "Use the tabs above to see activities you can do right now, or scheduled activities you can sign up for.\n\nPlease note you'll need a laptop or desktop computer (not a mobile device) running Chrome or Firefox to participate, unless a specific study says otherwise."
                )
            elif value == StudyListSearchForm.Tabs.synchronous_studies.value[0]:
                return _(
                    'You and your child can participate in these studies right now by choosing a study and then clicking "Participate." Please note you\'ll need a laptop or desktop computer (not a mobile device) running Chrome or Firefox to participate, unless a specific study says otherwise.'
                )
            elif value == StudyListSearchForm.Tabs.asynchronous_studies.value[0]:
                return _(
                    'You and your child can participate in these studies by scheduling a time to meet with a researcher (usually over video conferencing). Choose a study and then click "Participate" to sign up for a study session in the future.'
                )


@register.filter(name="studies_tab_selected")
def studies_tab_selected(value):
    for tab in value:
        if tab.data["selected"]:
            return tab.data["value"]


@register.simple_tag
def set_variable(val=None):
    """Tag for defining a string variable.

    Args:
        val (str): string value that needs to be assigned to a variable.

    Returns:
        String to be held in a variable.
    """
    return val


@register.simple_tag
def study_info_table_heading_classes():
    return "col-sm-12 col-md-4 py-2 align-top"


@register.simple_tag
def study_info_table_content_classes():
    return "col-sm-12 col-md-8 py-2 ps-2 align-top"


@register.simple_tag
def button_primary_classes(extra_classes=None):
    classes = ["btn", "btn-primary"]
    if extra_classes:
        classes.extend([extra_classes])

    return " ".join(classes)


@register.simple_tag
def button_secondary_classes(extra_classes=None):
    classes = ["btn", "btn-light", "link-secondary", "border-secondary"]
    if extra_classes:
        classes.extend([extra_classes])

    return " ".join(classes)


@register.simple_tag
def page_title(title, right_side_elements=None):
    if right_side_elements:
        html = f"""<div class="d-flex flex-row bd-highlight mb-4 align-items-center">
        <h1 class="me-auto">{title}</h1>
        <div>{right_side_elements}</div>
        </div>"""
    else:
        html = f'<h1 class="mt-4 mb-4 text-center">{title}</h1>'
    return mark_safe(html)


@register.tag(name="breadcrumb")
def breadcrumb(parser, token):
    nodelist = parser.parse(("endbreadcrumb",))
    parser.delete_first_token()
    return BreadcrumbNode(nodelist)


class BreadcrumbNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def pairwise(self, iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(iterable)
        return zip(a, a)

    def render(self, context):
        if not self.nodelist:
            return ""

        # remove empty nodes
        for node in self.nodelist:
            if not node.render(context).strip():
                self.nodelist.remove(node)

        # get last node from list
        last_node = self.nodelist.pop()

        result = [
            '<nav aria-label="breadcrumb" class="my-2 breadcrumb">',
            '<ol class="breadcrumb">',
        ]

        for a, b in self.pairwise(self.nodelist):
            result.append('<li class="breadcrumb-item">')
            result.append(f'<a href="{a.render(context)}">{b.render(context)}</a>')
            result.append("</li>")

        result.append(
            f'<li class="breadcrumb-item active" aria-current="page">{last_node.render(context)}</li>'
        )
        result.append("</ol></nav>")
        return "".join(result)


@register.tag(name="form_buttons")
def form_buttons(parser, token):
    nodelist = parser.parse(("endform_buttons",))
    parser.delete_first_token()
    return FormButtonsNode(nodelist)


class FormButtonsNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        rendered_buttons = (n.render(context) for n in self.nodelist)
        return f'<div class="d-flex justify-content-end gap-1">{"".join(rendered_buttons)}</div>'


@register.simple_tag
def staff_profile(name, img, blurb, type="large"):
    """Tag for defining a staff image, name and bio/blurb.

    Args:
        name (str): Name to appear under the photo
        img (str): Full path to the image (to be used as the img src)
        blurb (str): Bio/blurb to appear under the name
        type (str): Sets the profile type as "large" (default) or "small". If large, profiles appear in rows of 4 on large screens and rows of 1 on mobile (with reduced image size). If small, the profiles appear in rows of 6 on large screens and rows of 2 on mobile.

    Returns:
        HTML string for the staff profile div
    """

    if type == "large":
        profile_div_classes = "col-12 col-md-6 col-lg-3"
        img_div_classes = "col-8 col-lg-12"
        blurb_classes = ""
    else:
        profile_div_classes = "col-6 col-md-4 col-lg-2"
        img_div_classes = "col-12"
        blurb_classes = "text-center"

    html = f"""<div class="{profile_div_classes}">
    <div class="row justify-content-center">
    <div class="{img_div_classes}">
    <img class="img-fluid w-100 mx-auto d-block rounded-circle shadow mb-3" 
    alt="{name}" 
    src="{img}"/> 
    </div>
    </div>
    <h3 class="text-center">{name}</h3> 
    <p class="pb-4 {blurb_classes}">{blurb}</p>
    </div>"""
    return mark_safe(html)
