from typing import overload
import ghidra.features.base.memsearch.bytesequence
import ghidra.features.base.memsearch.gui
import java.lang


class ByteMatcher(object):
    """
    ByteMatcher is the base class for an object that be used to scan bytes looking for sequences
     that match some criteria. As a convenience, it also stores the input string and settings that
     were used to generated this ByteMatcher.
    """






    class ByteMatch(java.lang.Record):




        def __init__(self, __a0: int, __a1: int): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def length(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def start(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...







    def equals(self, obj: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode:
        """
        Returns a description of what this byte matcher matches. (Typically a sequence of bytes)
        @return a description of what this byte matcher matches
        """
        ...

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

    def getToolTip(self) -> unicode:
        """
        Returns additional information about this byte matcher. (Typically the mask bytes)
        @return additional information about this byte matcher
        """
        ...

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

    def match(self, bytes: ghidra.features.base.memsearch.bytesequence.ExtendedByteSequence) -> java.lang.Iterable:
        """
        Returns an {@link Iterable} for returning matches within the given byte sequence.
        @param bytes the byte sequence to search
        @return an iterable for return matches in the given sequence
        """
        ...

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
    def input(self) -> unicode: ...

    @property
    def settings(self) -> ghidra.features.base.memsearch.gui.SearchSettings: ...

    @property
    def toolTip(self) -> unicode: ...

    @property
    def validInput(self) -> bool: ...

    @property
    def validSearch(self) -> bool: ...