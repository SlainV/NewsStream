from rest_framework.permissions import BasePermission


class IsJournalist(BasePermission):
    """
    Allow access only to authenticated journalists.
    """

    message = "Only journalists may create articles."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "Journalist"
            and request.user.groups.filter(
                name="Journalist"
            ).exists()
        )


class IsJournalistOrEditor(BasePermission):
    """
    Allow editors to modify any article.

    Allow journalists to modify only articles
    that they authored.
    """

    message = (
        "Only editors or the journalist who created "
        "the article may modify it."
    )

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in [
            "Journalist",
            "Editor",
        ]

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        if request.user.role == "Editor":
            return request.user.groups.filter(
                name="Editor"
            ).exists()

        if request.user.role == "Journalist":
            is_journalist = request.user.groups.filter(
                name="Journalist"
            ).exists()

            return (
                is_journalist
                and obj.author_id == request.user.id
            )

        return False
