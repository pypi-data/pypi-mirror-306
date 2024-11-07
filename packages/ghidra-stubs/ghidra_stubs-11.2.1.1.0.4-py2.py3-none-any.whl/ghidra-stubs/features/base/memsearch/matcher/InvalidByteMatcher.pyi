from typing import overload
import ghidra.features.base.memsearch.bytesequence
import ghidra.features.base.memsearch.gui
import ghidra.features.base.memsearch.matcher
import java.lang


class InvalidByteMatcher(ghidra.features.base.memsearch.matcher.ByteMatcher):
    """
    Objects of this class are the result of SearchFormats not being able to fully parse
     input text. There are two cases. The first is the user type an illegal character for the
     selected search format. In that case this matcher is both an invalid search and an invalid
     input and the description will explain the error. The second case is the input is valid text,
     but not complete so that a fully valid byte matcher could not be created. In this case, the
     search is still invalid, but the input is valid. The description will reflect this situation.
    """





    @overload
    def __init__(self, errorMessage: unicode):
        """
        Construct an invalid matcher from invalid input text.
        @param errorMessage the message describing the invalid input
        """
        ...

    @overload
    def __init__(self, errorMessage: unicode, isValidInput: bool):
        """
        Construct an invalid matcher from invalid input text or partial input text.
        @param errorMessage the message describing why this matcher is invalid
        @param isValidInput return true if the reason this is invalid is simply that the input
         text is not complete. For example, the user types "-" as they are starting to input
         a negative number.
        """
        ...



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

    def isValidInput(self) -> bool: ...

    def isValidSearch(self) -> bool: ...

    def match(self, bytes: ghidra.features.base.memsearch.bytesequence.ExtendedByteSequence) -> java.lang.Iterable: ...

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

    @property
    def validInput(self) -> bool: ...

    @property
    def validSearch(self) -> bool: ...