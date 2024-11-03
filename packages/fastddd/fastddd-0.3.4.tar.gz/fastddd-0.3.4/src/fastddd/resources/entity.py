from pydantic import BaseModel, ValidationError, ConfigDict
from typing import TypeVar

from ..errors.app import ValidationException

T = TypeVar("T")


def entity(id_field: str = "id", validation_exception=None):
    """[DDDのEntityに付与するデコレータ]

    Entityクラスには以下の機能を追加する
    - BaseModelを継承しているかチェック
    - new関数が定義されていない場合は、デフォルトのnew関数を定義する
    - new関数がValidationErrorをスローした場合は、ValidationExceptionをスローする
    - IDフィールドを指定することで、IDで比較可能にする

    Args:
        id_field (str): IDフィールド名
        validation_exception (Exception): ValidationErrorをスローした場合にスローする例外クラス
    """

    def decorator(cls: T) -> T:
        # pydanticのBaseModelを継承しているかチェック
        if not issubclass(cls, BaseModel):
            raise ValueError("Entity class must inherit BaseModel")

        # model_configがない場合は追加
        if not hasattr(cls, "model_config"):
            cls.model_config = ConfigDict(from_attributes=True)

        # new関数が定義されていない場合は、デフォルトのnew関数を定義する
        if not hasattr(cls, "new"):
            # クラス名を取得
            class_name = cls.__name__

            # クラスのプロパティを取得
            properties = cls.__annotations__.keys()

            # new関数を定義
            def new(cls, *args, **kwargs):
                # プロパティの値を取得
                values = dict(zip(properties, args))
                values.update(kwargs)
                try:
                    return cls(**values)
                except ValidationError as e:
                    if validation_exception is None:
                        raise ValidationException(
                            e, f"{class_name} validation error", "NOT DEFINED ERROR CODE")
                    else:
                        raise validation_exception(e)

            cls.new = classmethod(new)
        else:
            new = getattr(cls, "new")

            # 例外処理を追加
            def new_with_exception(cls, *args, **kwargs):
                try:
                    return new(*args, **kwargs)
                except ValidationError as e:
                    if validation_exception is None:
                        raise ValidationException(
                            e, f"{cls.__name__} validation error", "NOT DEFINED ERROR CODE")
                    else:
                        raise validation_exception(e)

            cls.new = classmethod(new_with_exception)

        # Entity同士の比較で利用するIDフィールドを指定
        cls.__id_field = id_field

        # 比較演算子をオーバーライド
        def __eq__(self, value: object) -> bool:
            if not isinstance(value, cls):
                return False
            return getattr(self, self.__id_field) == getattr(value, self.__id_field)

        cls.__eq__ = __eq__

        return cls

    return decorator
