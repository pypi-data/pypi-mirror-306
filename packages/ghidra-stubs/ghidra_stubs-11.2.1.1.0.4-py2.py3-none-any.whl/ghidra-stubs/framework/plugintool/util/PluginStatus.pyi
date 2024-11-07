from typing import List
from typing import overload
import ghidra.framework.plugintool.util
import java.lang
import java.util


class PluginStatus(java.lang.Enum):
    DEPRECATED: ghidra.framework.plugintool.util.PluginStatus
    HIDDEN: ghidra.framework.plugintool.util.PluginStatus
    RELEASED: ghidra.framework.plugintool.util.PluginStatus
    STABLE: ghidra.framework.plugintool.util.PluginStatus
    UNSTABLE: ghidra.framework.plugintool.util.PluginStatus







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.framework.plugintool.util.PluginStatus: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.framework.plugintool.util.PluginStatus]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def description(self) -> unicode: ...