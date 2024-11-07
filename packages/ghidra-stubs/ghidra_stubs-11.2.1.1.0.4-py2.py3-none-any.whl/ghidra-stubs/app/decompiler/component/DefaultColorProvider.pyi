from typing import overload
import ghidra.app.decompiler
import ghidra.app.decompiler.component
import java.awt
import java.lang


class DefaultColorProvider(object, ghidra.app.decompiler.component.ColorProvider):
    """
    A color provider that returns a specific color.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getColor(self, token: ghidra.app.decompiler.ClangToken) -> java.awt.Color: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

