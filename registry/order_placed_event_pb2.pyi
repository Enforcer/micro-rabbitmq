"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class OrderPlaced(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    PRODUCT_ID_FIELD_NUMBER: builtins.int
    PRICE_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    id: builtins.int
    product_id: builtins.int
    price: builtins.float
    quantity: builtins.int
    def __init__(
        self,
        *,
        id: builtins.int = ...,
        product_id: builtins.int = ...,
        price: builtins.float = ...,
        quantity: builtins.int = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "id",
            b"id",
            "price",
            b"price",
            "product_id",
            b"product_id",
            "quantity",
            b"quantity",
        ],
    ) -> None: ...

global___OrderPlaced = OrderPlaced