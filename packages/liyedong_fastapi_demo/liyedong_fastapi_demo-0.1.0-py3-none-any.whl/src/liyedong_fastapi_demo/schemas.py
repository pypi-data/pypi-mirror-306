from datetime import datetime
from typing import ClassVar, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, constr

from .models import BaseModel as DBModel

ModelType = TypeVar('ModelType', bound=DBModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class InDBMixin(BaseModel):
    id: int

    Config: ClassVar[ConfigDict] = ConfigDict(
        arbitrary_types_allowed=True,
        # 其他配置选项
    )


class BaseArticle(BaseModel):
    title: constr(max_length=500)
    body: Optional[str] = None


class ArticleSchema(BaseArticle, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateArticleSchema(BaseArticle):
    pass


class UpdateArticleSchema(BaseArticle):
    title: Optional[constr(max_length=500)] = None
