# templatetags/custom_tags.py
from django import template
from django.utils.html import format_html

register = template.Library()


from typing import Union


@register.filter
def color_status(value: int) -> str:
    """
    Returns a Bootstrap badge with the specified value.

    Parameters:
    - value: An integer value representing the badge value.

    Returns:
    - str: The HTML code for the Bootstrap badge.
    """
    badge_class = "status opacity-50 bg-secondary"

    if value == 1:
        badge_class = "status opacity-50 bg-success"
    elif value > 0:
        badge_class = "status opacity-50 bg-warning"
    elif value == 0:
        badge_class = "status opacity-50 bg-danger"
    else :
        badge_class = "status opacity-50 bg-secondary"

    return badge_class




@register.filter
def bootstrap_badge(value: int) -> str:
    """
    Returns a Bootstrap badge with the specified value.

    Parameters:
    - value: An integer value representing the badge value.

    Returns:
    - str: The HTML code for the Bootstrap badge.
    """
    badge_class = "bg-secondary"

    if value == 1:
        badge_class = "bg-secondary"
    elif value == 2:
        badge_class = "bg-success"
    elif value == 3:
        badge_class = "bg-warning text-dark"
    elif value == 4:
        badge_class = "bg-danger"

    return f'<span class="badge {badge_class}">{value}</span>'

@register.simple_tag
def progress_bar(progress: Union[int, float]) -> str:
    """Generate a progress bar HTML element based on the progress value.

    Args:
        progress: The progress value, ranging from 0 to 100.

    Returns:
        The HTML string representing the progress bar.
    """
    if progress < 75:
        class_attr = "bg-danger"
    elif progress < 100:
        class_attr = "bg-warning"
    else:
        class_attr = "bg-success"

    html = f"""
        <div class="progress">
            <div class="progress-bar progress-bar-striped {class_attr}"
                role="progressbar"
                style="width: {progress}%"
                aria-valuenow="{progress}"
                aria-valuemin="0"
                aria-valuemax="100">
                {progress}%
            </div>
        </div>
    """
    return format_html(html)
