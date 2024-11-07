from typing import overload
import ghidra.features.base.memsearch.searcher
import java.lang
import java.util.function


class CodeUnitFilter(object, java.util.function.Predicate):
    """
    Search filter that can test a search result and determine if that result starts at or inside
     a code unit that matches one of the selected types.
    """





    def __init__(self, program: ghidra.program.model.listing.Program, includeInstructions: bool, includeDefinedData: bool, includeUndefinedData: bool):
        """
        Constructor
        @param program the program to get code units from for testing its type
        @param includeInstructions if true, accept matches that are in an instruction
        @param includeDefinedData if true, accept matches that are in defined data
        @param includeUndefinedData if true, accept matches that are in undefined data
        """
        ...



    def and(self, __a0: java.util.function.Predicate) -> java.util.function.Predicate: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isEqual(__a0: object) -> java.util.function.Predicate: ...

    def negate(self) -> java.util.function.Predicate: ...

    @staticmethod
    def not(__a0: java.util.function.Predicate) -> java.util.function.Predicate: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def or(self, __a0: java.util.function.Predicate) -> java.util.function.Predicate: ...

    @overload
    def test(self, match: ghidra.features.base.memsearch.searcher.MemoryMatch) -> bool: ...

    @overload
    def test(self, __a0: object) -> bool: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

