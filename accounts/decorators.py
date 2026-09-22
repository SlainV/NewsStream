"""
The purpose of decorators in Python is to modify the behavior of a function
or method without changing its source code. They are commonly used for
authorization, authentication, and permission controls.
"""


from django.contrib.auth.decorators import user_passes_test


def group_required(group_name):
    """Decorator to check if the current
    user is a member of a specific group."""
    def in_group(user):
        return user.groups.filter(
            name=group_name
        ).exists()

    return user_passes_test(in_group)
