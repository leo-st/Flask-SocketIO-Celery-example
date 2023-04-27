from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def value_list(cls):
        return list(map(lambda c: c.value, cls))


class PermissionKey(ExtendedEnum):
    USERS_CAN_VIEW_USER_LIST = 'users_can_view_user_list'
    USERS_CAN_CREATE_USER = 'users_can_create_user'
    USERS_CAN_EDIT_OTHER_USERS = 'users_can_edit_other_users'
    ROLES_CAN_VIEW_ROLE_LIST = 'roles_can_view_role_list'
    ROLES_CAN_CREATE_EDIT_ROLE = 'roles_can_create_edit_role'
    PERMISSIONS_CAN_VIEW_PERMISSION_LIST = 'permissions_can_view_permission_list'
    PAGES_CAN_VIEW_ARTICLES_SUPPLIER = 'pages_can_view_articles_supplier'


class ForecastAdaptationLevel(ExtendedEnum):
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'