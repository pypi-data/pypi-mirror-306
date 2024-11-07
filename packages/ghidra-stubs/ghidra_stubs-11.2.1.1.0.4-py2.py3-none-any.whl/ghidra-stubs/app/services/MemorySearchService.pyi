from typing import overload
import ghidra.app.nav
import ghidra.features.base.memsearch.gui
import java.lang


class MemorySearchService(object):
    """
    Service for invoking the MemorySearchProvider
    """









    def createMemorySearchProvider(self, navigatable: ghidra.app.nav.Navigatable, input: unicode, settings: ghidra.features.base.memsearch.gui.SearchSettings, useSelection: bool) -> None:
        """
        Creates a new memory search provider window
        @param navigatable the navigatable used to get bytes to search
        @param input the input string to search for
        @param settings the settings that determine how to interpret the input string
        @param useSelection true if the provider should automatically restrict to a selection if
         a selection exists in the navigatable
        """
        ...

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

