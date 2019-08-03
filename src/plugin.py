from typing import Optional, Callable
from typing import Type as TypingType

from mypy.nodes import TypeInfo, TypeAlias
from mypy.plugin import Plugin, AttributeContext
from mypy.types import Type as MypyType, FunctionLike

_BASE_MODEL_FULLNAME = "test.example.BaseModel"
_BASE_FIELD_FULLNAME = "test.example.BaseField"
_INSTANCE_TYPE_ATTR_NAME = "instance_type"


class ModelPlugin(Plugin):
    def get_attribute_hook(self, fullname: str) -> Optional[Callable[[AttributeContext], MypyType]]:
        attr_info = self.lookup_fully_qualified(fullname)
        if attr_info is None:
            return None

        field_class_name = repr(attr_info.type)
        containing_class_name = ".".join(fullname.split(".")[:-1])

        is_model_class = self._class_has_base(containing_class_name, _BASE_MODEL_FULLNAME)
        is_model_field = self._class_has_base(field_class_name, _BASE_FIELD_FULLNAME)

        if is_model_class and is_model_field:
            instance_type_info = self.lookup_fully_qualified(f"{field_class_name}.{_INSTANCE_TYPE_ATTR_NAME}")
            if instance_type_info is None:
                return None

            if instance_type_info.type is not None:
                instance_type = instance_type_info.type
                if isinstance(instance_type, FunctionLike) and instance_type.is_type_obj():
                    instance_type = instance_type.items()[0].ret_type
            elif isinstance(instance_type_info.node, TypeAlias):
                instance_type = instance_type_info.node.target

            def resolve(_: AttributeContext) -> MypyType:
                return instance_type

            return resolve

        return None

    def _class_has_base(self, class_fullname: str, base_fullname: str) -> bool:
        class_info = self.lookup_fully_qualified(class_fullname)
        return (
            class_info is not None and isinstance(class_info.node, TypeInfo) and class_info.node.has_base(base_fullname)
        )


def plugin(_mypy_info: str) -> TypingType[Plugin]:
    return ModelPlugin
