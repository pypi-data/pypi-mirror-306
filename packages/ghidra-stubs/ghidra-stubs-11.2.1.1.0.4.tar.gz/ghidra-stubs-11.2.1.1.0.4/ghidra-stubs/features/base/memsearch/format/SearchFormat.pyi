from typing import List
from typing import overload
import ghidra.features.base.memsearch.format
import ghidra.features.base.memsearch.format.SearchFormat
import ghidra.features.base.memsearch.gui
import ghidra.features.base.memsearch.matcher
import java.lang
import java.util


class SearchFormat(object):
    """
    SearchFormats are responsible for parsing user input data into a ByteMatcher that
     can be used for searching memory. It also can convert search matches back into string data and 
     can convert string data from other formats into string data for this format.
    """

    ALL: List[ghidra.features.base.memsearch.format.SearchFormat]
    BINARY: ghidra.features.base.memsearch.format.SearchFormat
    DECIMAL: ghidra.features.base.memsearch.format.SearchFormat
    DOUBLE: ghidra.features.base.memsearch.format.SearchFormat
    FLOAT: ghidra.features.base.memsearch.format.SearchFormat
    HEX: ghidra.features.base.memsearch.format.SearchFormat
    REG_EX: ghidra.features.base.memsearch.format.SearchFormat
    STRING: ghidra.features.base.memsearch.format.SearchFormat




    class SearchFormatType(java.lang.Enum):
        BYTE: ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType
        FLOATING_POINT: ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType
        INTEGER: ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType
        STRING_TYPE: ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType







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
        def valueOf(__a0: unicode) -> ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...







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

    def convertText(self, text: unicode, oldSettings: ghidra.features.base.memsearch.gui.SearchSettings, newSettings: ghidra.features.base.memsearch.gui.SearchSettings) -> unicode:
        """
        Returns a new search input string, doing its best to convert an input string that
         was parsed by a previous {@link SearchFormat}. When it makes sense to do so, it will
         re-interpret the parsed bytes from the old format and reconstruct the input from those
         bytes. This allows the user to do conversions, for example, from numbers to hex or binary and 
         vise-versa. If the byte conversion doesn't make sense based on the old and new formats, it
         will use the original input if that input can be parsed by the new input. Finally, if all
         else fails, the new input will be the empty string.
        @param text the old input that is parsable by the old format
        @param oldSettings the search settings used to parse the old text
        @param newSettings the search settings to used for the new text
        @return the "best" text to change the user search input to
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFormatType(self) -> ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType:
        """
        Returns the {@link SearchFormatType} for this format. This is used to help with the
         {@link #convertText(String, SearchSettings, SearchSettings)} method.
        @return the type for this format
        """
        ...

    def getName(self) -> unicode:
        """
        Returns the name of the search format.
        @return the name of the search format
        """
        ...

    def getToolTip(self) -> unicode:
        """
        Returns a tool tip describing this search format
        @return a tool tip describing this search format
        """
        ...

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

    def parse(self, input: unicode, settings: ghidra.features.base.memsearch.gui.SearchSettings) -> ghidra.features.base.memsearch.matcher.ByteMatcher:
        """
        Parse the given input and settings into a {@link ByteMatcher}
        @param input the user input string
        @param settings the current search/parse settings
        @return a ByteMatcher that can be used for searching bytes (or an error version of a matcher)
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def formatType(self) -> ghidra.features.base.memsearch.format.SearchFormat.SearchFormatType: ...

    @property
    def name(self) -> unicode: ...

    @property
    def toolTip(self) -> unicode: ...