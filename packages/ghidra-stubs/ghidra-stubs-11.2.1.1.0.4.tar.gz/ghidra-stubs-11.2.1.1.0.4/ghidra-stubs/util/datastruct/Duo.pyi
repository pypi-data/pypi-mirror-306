from typing import List
from typing import overload
import ghidra.util.datastruct
import ghidra.util.datastruct.Duo
import java.lang
import java.util
import java.util.function


class Duo(object):
    """
    Class for holding two objects of the same type. We are using the idiom of LEFT and RIGHT to 
     refer to each item in this pair of objects.
     The enum "Side" is used to represent either the LEFT (or first) or RIGHT (or second) item.
    """






    class Side(java.lang.Enum):
        LEFT: ghidra.util.datastruct.Duo.Side
        RIGHT: ghidra.util.datastruct.Duo.Side







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

        def otherSide(self) -> ghidra.util.datastruct.Duo.Side: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.util.datastruct.Duo.Side: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.util.datastruct.Duo.Side]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



    @overload
    def __init__(self):
        """
        Constructor with no values.
        """
        ...

    @overload
    def __init__(self, left: object, right: object):
        """
        Constructor with a left and right value.
        @param left the left value
        @param right the right value
        """
        ...



    def each(self, c: java.util.function.Consumer) -> None:
        """
        Invokes the given consumer on both the left and right values.
        @param c the consumer to invoke on both values
        """
        ...

    @overload
    def equals(self, obj: object) -> bool: ...

    @overload
    def equals(self, otherLeft: object, otherRight: object) -> bool:
        """
        Returns true if both values are equals to this objects values.
        @param otherLeft the value to compare to our left side value
        @param otherRight the value to compare to our right side value
        @return true if both values are equals to this objects values
        """
        ...

    def get(self, side: ghidra.util.datastruct.Duo.Side) -> object:
        """
        Gets the value for the given side.
        @param side LEFT or RIGHT
        @return the value for the given side
        """
        ...

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

    def with(self, side: ghidra.util.datastruct.Duo.Side, newValue: object) -> ghidra.util.datastruct.Duo:
        """
        Creates a new Duo, replacing the value for just one side. The other side uses the value 
         from this Duo.
        @param side the side that gets a new value
        @param newValue the new value for the given side
        @return the new Duo
         value as this
        """
        ...

