from typing import Optional, Union

from pydantic import BaseModel, Field
from ..model.enums import UserStatus, UserGender
from ..lib import time as time_lib


class BaseData(BaseModel):
    """
    通用基础数据模型
    """
    # mongodb主键
    _id: str = None
    # 插入时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )


class AuthUser(BaseData):
    """
    用户鉴权模型
    """
    # 用户编号
    id: str
    # 租户编码
    tenantCode: Optional[str] = None
    # 用户名
    userName: Optional[str] = None
    # 用户姓名
    realName: Optional[str] = None
    # 性别
    gender: Optional[int] = UserGender.MALE
    # 电话
    mobile: Optional[str] = None
    # 邮箱
    email: Optional[str] = None
    # 是否超级管理员
    superAdmin: Optional[str] = None
    # 是否超级租户
    superTenant: Optional[int] = 1
    # 启用停用
    isEnabled: Optional[bool] = True
    # 批次状态
    status: Optional[str] = UserStatus.NORMAL

    def to_log(self):
        return f'{self.realName}({self.id})'

    def is_super_admin(self):
        return '1' == self.superAdmin


class AuthApp(BaseData):
    """
    App鉴权模型
    """
    # 用户编号
    appId: str
    # 用户名
    appName: Optional[str] = None
    # 账号
    accessKey: Optional[str] = None
    # 密码
    secretKey: Optional[str] = None
    # 长效Token
    staticToken: Optional[str] = None
    # 是否启用长效Token
    enableStaticToken: Optional[int] = None
    # 启用停用
    isEnabled: Optional[bool] = None
    # 批次状态
    status: Optional[str] = None
    # 租户编码
    tenantCode: Optional[str] = None
