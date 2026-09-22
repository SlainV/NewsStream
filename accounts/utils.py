# Permission helpers


# def is_editor(user):
#    """Check if the current user has editor permissions.
#    Returns True or False."""
#    return user.groups.filter(
#        name="Editor"
#    ).exists()


# def is_journalist(user):
#    """Check if the current user has journalist permissions.
#    Returns True or False."""
#    return user.groups.filter(
#        name="Journalist"
#    ).exists()


# def is_publisher_manager(user):
#    """Check if the current user has publisher manager permissions.
#    Returns True or False."""
#    return user.groups.filter(
#        name="Publisher Manager"
#    ).exists()


def has_role(user, role):
    """Check if the current user has a specific role.
    Returns True or False."""
    return user.groups.filter(
        name=role
    ).exists()


def is_reader(user):
    return has_role(
        user,
        "Reader"
    )


def is_editor(user):
    return has_role(
        user,
        "Editor"
    )


def is_journalist(user):
    return has_role(
        user,
        "Journalist"
    )


def is_publisher_manager(user):
    return has_role(
        user,
        "Publisher Manager"
    )


def is_administrator(self):
    """Check if the current user has a specific role."""
    return self.groups.filter(name="Administrator").exists()
