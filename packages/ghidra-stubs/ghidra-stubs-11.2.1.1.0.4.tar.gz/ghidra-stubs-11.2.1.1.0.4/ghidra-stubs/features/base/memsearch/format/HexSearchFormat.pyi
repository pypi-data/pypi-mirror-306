from typing import List
from typing import overload
import ghidra.features.base.memsearch.format
import ghidra.features.base.memsearch.format.SearchFormat
import ghidra.features.base.memsearch.gui
import ghidra.features.base.memsearch.matcher
import java.lang


class HexSearchFormat(ghidra.features.base.memsearch.format.SearchFormat):
    """
    SearchFormat for parsing and display bytes in a hex format. This format only 
     accepts hex digits or wild card characters.
    """









    def compareValues(self, bytes1: List[int], bytes2: List[int], settings: ghidra.features.base.memsearch.gui.SearchSettings) -> int:
        """
        Compares bytes from search results based on how this format interprets the bytes.
         By default, formats just compare the bytes one by one as if they were unsigned values.
         SearchFormats whose bytes represent numerical values will override this method and
         compare the bytes after interpreting them as numerical values.
        @param bytes1 the first array of bytes to compare
        @param bytes2 the second array of bytes to compare
        @param settings the search settings used to generate the bytes.
        @return a negative integer, zero, or a positive integer as the first byte array 
         is less than, equal to, or greater than the second byte array
        """
        ...

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

    def getValueString(self, bytes: List[int], settings: ghidra.features.base.memsearch.gui.SearchSettings) -> unicode:
        """
        Reverse parses the bytes back into input value strings. Note that this is only used by
         numerical and string type formats. Byte oriented formats just return an empty string.
        @param bytes the to convert back into input value strings
        @param settings The search settings used to parse the input into bytes
        @return the string of the reversed parsed byte values
        """
        ...

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

