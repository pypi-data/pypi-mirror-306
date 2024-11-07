from typing import List
from typing import overload
import ghidra.app.plugin.match.MatchSymbol
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.model.symbol
import ghidra.util.task
import java.lang


class MatchSymbol(object):





    class MatchedSymbol(object):








        def equals(self, __a0: object) -> bool: ...

        def getAProgram(self) -> ghidra.program.model.listing.Program: ...

        def getASymbolAddress(self) -> ghidra.program.model.address.Address: ...

        def getBProgram(self) -> ghidra.program.model.listing.Program: ...

        def getBSymbolAddress(self) -> ghidra.program.model.address.Address: ...

        def getClass(self) -> java.lang.Class: ...

        def getMatchCount(self) -> int: ...

        def getMatchType(self) -> ghidra.program.model.symbol.SymbolType: ...

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

        @property
        def AProgram(self) -> ghidra.program.model.listing.Program: ...

        @property
        def ASymbolAddress(self) -> ghidra.program.model.address.Address: ...

        @property
        def BProgram(self) -> ghidra.program.model.listing.Program: ...

        @property
        def BSymbolAddress(self) -> ghidra.program.model.address.Address: ...

        @property
        def matchCount(self) -> int: ...

        @property
        def matchType(self) -> ghidra.program.model.symbol.SymbolType: ...





    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def matchSymbol(aProgram: ghidra.program.model.listing.Program, setA: ghidra.program.model.address.AddressSetView, bProgram: ghidra.program.model.listing.Program, setB: ghidra.program.model.address.AddressSetView, minSymbolNameLength: int, includeOneToOneOnly: bool, includeExternals: bool, monitor: ghidra.util.task.TaskMonitor) -> List[ghidra.app.plugin.match.MatchSymbol.MatchedSymbol]: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

