# Permission helpers

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
