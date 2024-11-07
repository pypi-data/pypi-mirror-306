from typing import List
from typing import overload
import docking.widgets.fieldpanel.support
import ghidra.app.util
import ghidra.app.util.viewer.field
import java.lang


class MemoryMatchHighlighter(object, ghidra.app.util.ListingHighlightProvider):
    """
    Listing highlight provider to highlight memory search results.
    """

    NO_HIGHLIGHTS: List[docking.widgets.fieldpanel.support.Highlight]



    def __init__(self, navigatable: ghidra.app.nav.Navigatable, model: ghidra.features.base.memsearch.gui.MemoryMatchTableModel, options: ghidra.features.base.memsearch.gui.MemorySearchOptions): ...



    def createHighlights(self, text: unicode, field: ghidra.app.util.viewer.field.ListingField, cursorTextOffset: int) -> List[docking.widgets.fieldpanel.support.Highlight]: ...

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

