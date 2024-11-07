from typing import List
from typing import overload
import ghidra.features.base.memsearch.bytesequence
import ghidra.features.base.memsearch.gui
import ghidra.features.base.memsearch.matcher
import java.lang


class MaskedByteSequenceByteMatcher(ghidra.features.base.memsearch.matcher.ByteMatcher):
    """
    ByteMatcher where the user search input has been parsed into a sequence of bytes and
     masks to be used for searching a byte sequence.
    """





    @overload
    def __init__(self, input: unicode, bytes: List[int], settings: ghidra.features.base.memsearch.gui.SearchSettings):
        """
        Constructor where no masking will be required. The bytes must match exactly.
        @param input the input text used to create this matcher
        @param bytes the sequence of bytes to use for searching
        @param settings the {@link SearchSettings} used to parse the input text
        """
        ...

    @overload
    def __init__(self, input: unicode, bytes: List[int], masks: List[int], settings: ghidra.features.base.memsearch.gui.SearchSettings):
        """
        Constructor that includes a mask byte for each search byte.
        @param input the input text used to create this matcher
        @param bytes the sequence of bytes to use for searching
        @param masks the sequence of mask bytes to use for search. Each mask byte will be applied
         to the bytes being search before comparing them to the target bytes.
        @param settings the {@link SearchSettings} used to parse the input text
        """
        ...



    def equals(self, obj: object) -> bool: ...

    def getBytes(self) -> List[int]: ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getInput(self) -> unicode:
        """
        Returns the original input text that generated this ByteMatacher.
        @return the original input text that generated this BytesMatcher
        """
        ...

    def getMask(self) -> List[int]: ...

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
    def bytes(self) -> List[int]: ...

    @property
    def description(self) -> unicode: ...

    @property
    def mask(self) -> List[int]: ...

    @property
    def toolTip(self) -> unicode: ...