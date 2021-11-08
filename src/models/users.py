from enum import IntEnum


class UserRole(IntEnum):
    """
    用户角色
    """

    NORMAL = 1  # 普通用户
    ENTERPRISE = 2  # 企业用户
    ADMIN = 3  # 平台管理员


class UserStatus(IntEnum):
    """
    账号状态
    """

    ACTIVATED = 1  # 正常状态
    DISABLED = 2  # 已禁用
    UNDER_REVIEW = 3  # 审核中
    REJECT = 4  # 审核不通过
