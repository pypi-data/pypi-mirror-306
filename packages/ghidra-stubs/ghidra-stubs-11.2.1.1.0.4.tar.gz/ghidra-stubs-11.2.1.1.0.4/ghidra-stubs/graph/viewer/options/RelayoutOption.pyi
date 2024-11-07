from typing import List
from typing import overload
import ghidra.graph.viewer.options
import java.lang
import java.util


class RelayoutOption(java.lang.Enum):
    ALWAYS: ghidra.graph.viewer.options.RelayoutOption
    BLOCK_MODEL_CHANGES: ghidra.graph.viewer.options.RelayoutOption
    NEVER: ghidra.graph.viewer.options.RelayoutOption
    VERTEX_GROUPING_CHANGES: ghidra.graph.viewer.options.RelayoutOption







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.graph.viewer.options.RelayoutOption: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.graph.viewer.options.RelayoutOption]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

