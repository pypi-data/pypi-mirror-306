from typing import List
from typing import overload
import ghidra.features.base.memsearch.format
import ghidra.features.base.memsearch.format.SearchFormat
import ghidra.features.base.memsearch.gui
import ghidra.features.base.memsearch.matcher
import java.lang


class DecimalSearchFormat(ghidra.features.base.memsearch.format.SearchFormat):
    """
    SearchFormat for parsing and display bytes in a decimal format. It supports sizes of
     2,4,8,16 and can be either signed or unsigned.
    """









    def compareValues(self, bytes1: List[int], bytes2: List[int], settings: ghidra.features.base.memsearch.gui.SearchSettings) -> int: ...

    def convertText(self, text: unicode, oldSettings: ghidra.features.base.memsearch.gui.SearchSettings, newSettings: ghidra.features.base.memsearch.gui.SearchSettings) -> unicode: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFormatType(self) -> ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType: ...

    def getName(self) -> unicode:
        """
        Returns the name of the search format.
        @return the name of the search format
        """
        ...

    def getToolTip(self) -> unicode: ...

    def getValueString(self, bytes: List[int], settings: ghidra.features.base.memsearch.gui.SearchSettings) -> unicode: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parse(self, input: unicode, settings: ghidra.features.base.memsearch.gui.SearchSettings) -> ghidra.features.base.memsearch.matcher.ByteMatcher: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

