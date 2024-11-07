from typing import overload
import ghidra.app.util.html
import java.awt
import java.lang


class ValidatableLine(object):
    """
    A loose concept that represents a line of text, potentially with multiple parts, that can
     be validated against other instances and can change the color of the text.
 
     Validation is performed against another ValidatableLine, which will be set by 
     calling #setValidationLine(ValidatableLine).
    """

    INVALID_COLOR: java.awt.Color







    def copy(self) -> ghidra.app.util.html.ValidatableLine: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getText(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def isDiffColored(self) -> bool: ...

    def isValidated(self) -> bool:
        """
        True means that this line has been matched against another line, <b>regardless of whether 
         the two lines are the same or not</b>.
        @return true if this line has been matched against another line
        """
        ...

    def matches(self, otherLine: ghidra.app.util.html.ValidatableLine) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setTextColor(self, color: java.awt.Color) -> None:
        """
        Set color for all text.
        @param color text color
        """
        ...

    def setValidationLine(self, line: ghidra.app.util.html.ValidatableLine) -> None:
        """
        Sets the other line that this line is validated against.  The other line may be a full, 
         partial, or no match at all.
        @param line the line against which this line is validated
        """
        ...

    def toString(self) -> unicode: ...

    def updateColor(self, otherLine: ghidra.app.util.html.ValidatableLine, invalidColor: java.awt.Color) -> None: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def diffColored(self) -> bool: ...

    @property
    def text(self) -> unicode: ...

    @property
    def textColor(self) -> None: ...  # No getter available.

    @textColor.setter
    def textColor(self, value: java.awt.Color) -> None: ...

    @property
    def validated(self) -> bool: ...

    @property
    def validationLine(self) -> None: ...  # No getter available.

    @validationLine.setter
    def validationLine(self, value: ghidra.app.util.html.ValidatableLine) -> None: ...