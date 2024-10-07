from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, что пользователь является модератором.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, что пользователь является владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsOwnerAndNotModer(permissions.BasePermission):
    """
    Проверяет, что пользователь является владельцем объекта и не является модератором.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        is_owner = obj.owner == request.user
        # Проверяем, является ли пользователь модератором
        is_not_moder = not request.user.groups.filter(name="moders").exists()
        return is_owner and is_not_moder