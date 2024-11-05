# MIT License
#
# Copyright (c) 2024 Bohdan Borovskyi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import struct
from functools import wraps
from typing import Callable, Any, Dict, Optional, Union
from collections import OrderedDict
from collections.abc import Sized


class Errors:
    class UnpackError(Exception): ...

    class LenNotFoundInMessageError(Exception): ...

    class OutOfBoundError(Exception): ...

    class EmptyMessageError(Exception): ...

    class EmptyFormatError(Exception): ...

    class NoFieldsParsedError(Exception): ...

    class FailedPreconditionError(Exception): ...

    class MessageArgError(Exception): ...

    class FieldTypeError(Exception): ...

    class PackError(Exception): ...

    class FieldNameError(Exception): ...


class Field:
    __counter = 0

    def __init__(self, fmt: Union[str, Callable[..., Any]]):
        if not fmt:
            raise Errors.EmptyFormatError("No fmt specified")
        self.__fmt = fmt
        self.is_var_len = callable(fmt)
        self.name = None
        self.counter = Field.__counter
        Field.__counter += 1

    def __set_name__(self, owner, name):
        self.name = name

    def get_fmt(self, instance: "ByteStructureBase"):
        """
        Return fixed or variable length format of Field.
        """
        if self.is_var_len:
            try:
                return self.__fmt(instance)
            except (KeyError, AttributeError):
                raise Errors.LenNotFoundInMessageError(
                    f'Len field for "{self.name}" not found or set after.'
                )
        return self.__fmt

    def get_expected_size(self, instance: "ByteStructureBase"):
        """
        Calculate fixed and variable length Field size as per specified format.
        """
        return struct.calcsize(self.get_fmt(instance))

    def __get__(self, instance: "ByteStructureBase", owner):
        if instance is None:
            return self
        try:
            return instance.parsed_fields_map[self.name]
        except KeyError:
            raise AttributeError(f'"{self.name}" seems to have already been deleted')

    def __delete__(self, instance: "ByteStructureBase"):
        instance.parsed_fields_map.pop(self.name)
        if hasattr(instance, self.name):
            delattr(instance, self.name)


class Flags:
    PARSED = 1 << 0  # Set once raw message is parsed


def precondition(*, _flags: int):
    """
    Check if method is allowed to run at that point of time.
    """

    def outer(func):
        @wraps(func)
        def inner(self: "ByteStructureBase", *args, **kwargs):
            if not (self.flags & _flags):
                raise Errors.FailedPreconditionError(
                    f"Required flag 0x{_flags:02x} but 0x{self.flags:02x} set"
                )
            return func(self, *args, **kwargs)

        return inner

    return outer


class ByteStructureBase:
    def __new__(cls, *args, **kwargs):
        if cls is ByteStructureBase:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        return super().__new__(cls)

    def __init__(
        self,
        msg: Optional[Union[bytes, bytearray]] = None,
        *,
        fields_map: Optional[Dict[str, Any]] = None,
    ):
        self.flags = 0

        if (not msg) == (not fields_map):
            raise Errors.MessageArgError(
                "Either msg or parsed_fields_map should be provided. Not both."
            )

        self.__msg: Union[bytes, bytearray] = b""
        self.__msg_len: int = 0
        self.parsed_fields_map: Dict[str, Any] = {}

        if msg:
            self.__msg = msg
            self.__msg_len = len(msg)
            self.__parse_fields_from_bytes()
        elif fields_map:
            self.parsed_fields_map = fields_map
            self.__parse_bytes_from_fields()

    def __parse_bytes_from_fields(self):
        data = b""
        fields_map = self.get_fields_and_their_names()
        if set(fields_map) != set(self.parsed_fields_map):
            raise Errors.FieldNameError(
                f"Provided field names on init must be equal "
                f"to field names from Field class attributes: got {set(self.parsed_fields_map)}, exp {set(fields_map)}"
            )

        for name, field in fields_map.items():
            fmt = field.get_fmt(self)
            size = field.get_expected_size(self)
            value = self.parsed_fields_map[name]
            if isinstance(value, Sized):
                if len(value) < size:
                    raise Errors.OutOfBoundError(
                        "Going out of bonds or incorrect endianness for len in case of var len field"
                    )
            try:
                data += struct.pack(fmt, value)
            except struct.error:
                raise Errors.PackError(
                    f'Error packing "{name}:{fmt}" with size {size}: "{value}"'
                )
        self.flags |= Flags.PARSED

        msg_len = len(data)
        exp_len = self.get_expected_size()
        if msg_len < exp_len:
            raise Errors.PackError(
                f"Raw msg len {msg_len} is less than expected {exp_len}"
            )
        self.__msg = data
        self.__msg_len = msg_len

    def __parse_fields_from_bytes(self):
        """
        Unpack raw message into structure based on Field format.
        """
        offset = 0
        fields_map = self.get_fields_and_their_names()
        for name, field in fields_map.items():  # type: str, Field
            fmt = field.get_fmt(self)
            size = field.get_expected_size(self)
            if size + offset > self.__msg_len:
                raise Errors.OutOfBoundError(
                    "Going out of bonds or incorrect endianness for len in case of var len field"
                )
            try:
                value = struct.unpack_from(fmt, self.__msg, offset)[0]
            except struct.error:
                raise Errors.UnpackError(
                    f'Error unpacking "{name}:{fmt}" with size {size} from offset {offset}'
                )
            self.parsed_fields_map[name] = value
            offset += size
        if not self.parsed_fields_map:
            raise Errors.NoFieldsParsedError(
                "No fields parsed. Ensure all fields are of Field type with correct struct format"
            )
        self.flags |= Flags.PARSED

    def get_fields_and_their_names(self) -> Dict[str, Field]:
        fields_map = OrderedDict()
        for cls in reversed(self.__class__.__mro__):
            cls_fields = [
                (name, field)
                for name, field in vars(cls).items()
                if isinstance(field, Field)
            ]
            # to keep a correct order with inheritance
            cls_fields.sort(key=lambda item: item[1].counter)
            fields_map.update(cls_fields)
        return fields_map

    @precondition(_flags=Flags.PARSED)
    def get_expected_size(self):
        """
        Sum of struct.calcsize(fmt) of all fixed and variable length Fields.
        """
        fields_obj = self.get_fields_and_their_names().values()
        return sum(obj.get_expected_size(self) for obj in fields_obj)

    @precondition(_flags=Flags.PARSED)
    def get_raw(self) -> Union[bytes, bytearray]:
        """
        Return full raw message as it is received on init.
        """
        return self.__msg

    @precondition(_flags=Flags.PARSED)
    def __repr__(self):
        str_builder = [f"{self.__class__.__name__}:"]
        for k, v in self.parsed_fields_map.items():
            str_builder.append(f"-- {k} {v}")
        return "\r\n".join(str_builder)
