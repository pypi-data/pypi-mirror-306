from typing import overload
import java.lang


class SearchMarkers(object):
    """
    Manages the MarkerSet for a given MemorySearchProvider window.
    """





    def __init__(self, tool: ghidra.framework.plugintool.PluginTool, title: unicode, program: ghidra.program.model.listing.Program): ...



    def dispose(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

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

