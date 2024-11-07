from typing import overload
import ghidra.features.base.memsearch.bytesequence
import ghidra.features.base.memsearch.gui
import ghidra.features.base.memsearch.matcher
import java.lang


class RegExByteMatcher(ghidra.features.base.memsearch.matcher.ByteMatcher):
    """
    ByteMatcher where the user search input has been parsed as a regular expression.
    """





    def __init__(self, input: unicode, settings: ghidra.features.base.memsearch.gui.SearchSettings): ...



    def equals(self, obj: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getInput(self) -> unicode:
        """
        Returns the original input text that generated this ByteMatacher.
        @return the original input text that generated this BytesMatcher
        """
        ...

    def getSettings(self) -> ghidra.features.base.memsearch.gui.SearchSettings:
        """
        Returns the settings used to generate this ByteMatcher.
        @return the settings used to generate this ByteMatcher
        """
        ...

    def getToolTip(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def isValidInput(self) -> bool:
        """
        Returns true if this byte matcher has valid (but possibly incomplete) input text. For 
         example, when entering decimal values, the input could be just "-" as the user starts
         to enter a negative number. In this case the input is valid, but the {@link #isValidSearch()}
         would return false.
        @return true if this byte matcher has valid text
        """
        ...

    def isValidSearch(self) -> bool:
        """
        Returns true if this byte matcher is valid and can be used to perform a search. If false,
         the the description will return a an error message explaining why this byte matcher is
         invalid.
        @return true if this byte matcher is valid and can be used to perform a search.
        """
        ...

    def match(self, byteSequence: ghidra.features.base.memsearch.bytesequence.ExtendedByteSequence) -> java.lang.Iterable: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def description(self) -> unicode: ...

    @property
    def toolTip(self) -> unicode: ...