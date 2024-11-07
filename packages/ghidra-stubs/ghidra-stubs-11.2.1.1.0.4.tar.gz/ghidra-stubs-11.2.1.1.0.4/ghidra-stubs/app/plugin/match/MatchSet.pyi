from typing import Iterator
from typing import List
from typing import overload
import ghidra.app.plugin.match
import java.lang
import java.util
import java.util.function
import java.util.stream


class MatchSet(java.util.HashSet):
    """
    class that contains a collection of matches.
    """

    otherName: unicode
    thisName: unicode



    def __init__(self, thisProgramName: unicode, otherProgramName: unicode):
        """
        @param thisProgramName Name of this program (i.e. the program from 
         which the matching was initiated.
        @param otherProgramName Name of the program being matched.
        """
        ...

    def __iter__(self): ...

    def add(self, __a0: object) -> bool: ...

    def addAll(self, __a0: java.util.Collection) -> bool: ...

    def clear(self) -> None: ...

    def clone(self) -> object: ...

    def contains(self, __a0: object) -> bool: ...

    def containsAll(self, __a0: java.util.Collection) -> bool: ...

    @staticmethod
    def copyOf(__a0: java.util.Collection) -> java.util.Set: ...

    def equals(self, __a0: object) -> bool: ...

    def forEach(self, __a0: java.util.function.Consumer) -> None: ...

    def getClass(self) -> java.lang.Class: ...

    def getMatches(self) -> List[ghidra.app.plugin.match.Match]:
        """
        @return The sorted array of matches.
        """
        ...

    def getResultsArray(self, m: ghidra.app.plugin.match.Match) -> List[object]:
        """
        @return The match as an Object array.
        """
        ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool: ...

    def iterator(self) -> java.util.Iterator: ...

    @staticmethod
    def newHashSet(__a0: int) -> java.util.HashSet: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    @staticmethod
    def of() -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: List[object]) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object, __a2: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object, __a2: object, __a3: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object, __a2: object, __a3: object, __a4: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object, __a2: object, __a3: object, __a4: object, __a5: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object, __a2: object, __a3: object, __a4: object, __a5: object, __a6: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object, __a2: object, __a3: object, __a4: object, __a5: object, __a6: object, __a7: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object, __a2: object, __a3: object, __a4: object, __a5: object, __a6: object, __a7: object, __a8: object) -> java.util.Set: ...

    @overload
    @staticmethod
    def of(__a0: object, __a1: object, __a2: object, __a3: object, __a4: object, __a5: object, __a6: object, __a7: object, __a8: object, __a9: object) -> java.util.Set: ...

    def parallelStream(self) -> java.util.stream.Stream: ...

    def removeAll(self, __a0: java.util.Collection) -> bool: ...

    def removeIf(self, __a0: java.util.function.Predicate) -> bool: ...

    def retainAll(self, __a0: java.util.Collection) -> bool: ...

    def size(self) -> int: ...

    def spliterator(self) -> java.util.Spliterator: ...

    def stream(self) -> java.util.stream.Stream: ...

    @overload
    def toArray(self) -> List[object]: ...

    @overload
    def toArray(self, __a0: List[object]) -> List[object]: ...

    @overload
    def toArray(self, __a0: java.util.function.IntFunction) -> List[object]: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def matches(self) -> List[ghidra.app.plugin.match.Match]: ...