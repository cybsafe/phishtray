from django import template

register = template.Library()


@register.inclusion_tag("admin/exercise/exercise_submit_line.html", takes_context=True)
def exercise_submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context["opts"]
    change = context["change"]
    is_popup = context["is_popup"]
    save_as = context["save_as"]
    has_copy_permission = False

    ctx = {
        "opts": opts,
        "show_delete_link": get_delete_permission(context),
        "show_delete_button": get_delete_permission(context),
        "show_save_as_new": not is_popup and change and save_as,
        "show_save_and_add_another": (
            context["has_add_permission"]
            and not is_popup
            and (not save_as or context["add"])
        ),
        "show_save_and_continue": not is_popup and context["has_change_permission"],
        "is_popup": is_popup,
        "show_save": True,
        "preserved_filters": context.get("preserved_filters"),
    }

    original = context["original"]
    user = context["user"]
    if original is not None and original.__class__.__name__ == "Exercise":
        if (
            user.is_superuser
            or user.organization == original.organisation
            or original.organisation is None
        ):
            has_copy_permission = True

        if user.is_staff and original.organisation is None:
            ctx["show_save_and_add_another"] = False
            ctx["show_save"] = False
            ctx["show_delete_button"] = False

    ctx["has_copy_permission"] = has_copy_permission

    return ctx


def get_delete_permission(context):
    change = context["change"]
    is_popup = context["is_popup"]
    return (
        not is_popup
        and context["has_delete_permission"]
        and change
        and context.get("show_delete", True)
    )
