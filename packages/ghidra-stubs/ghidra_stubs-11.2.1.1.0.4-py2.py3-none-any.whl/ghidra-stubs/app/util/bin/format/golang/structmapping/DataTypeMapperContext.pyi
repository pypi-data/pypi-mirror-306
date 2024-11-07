from typing import overload
import java.lang


class DataTypeMapperContext(object):
    """
    Context passed to StructureMapping logic when binding a structure's fields to a java class's
     fields.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def isFieldPresent(self, presentWhen: unicode) -> bool:
        """
        Tests if a field should be included when creating bindings between a structure and a class.
        @param presentWhen free-form string that is interpreted by each {@link DataTypeMapper}
        @return boolean true if field should be bound, false if field should not be bound
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

