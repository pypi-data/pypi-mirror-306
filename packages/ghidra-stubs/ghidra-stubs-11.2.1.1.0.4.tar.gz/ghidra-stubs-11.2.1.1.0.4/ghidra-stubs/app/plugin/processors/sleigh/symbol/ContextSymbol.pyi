from typing import overload
import ghidra.app.plugin.processors.sleigh
import ghidra.app.plugin.processors.sleigh.expression
import ghidra.app.plugin.processors.sleigh.symbol
import ghidra.program.model.pcode
import java.lang
import java.util


class ContextSymbol(ghidra.app.plugin.processors.sleigh.symbol.ValueSymbol):
    """
    A ValueSymbol that gets its semantic value from contiguous bits
     in a VarnodeSymbol. This serves as an embedding of a ContextOp
     into an actual Varnode and is probably only relevant at compile time
    """





    def __init__(self): ...



    def decode(self, decoder: ghidra.program.model.pcode.Decoder, sleigh: ghidra.app.plugin.processors.sleigh.SleighLanguage) -> None: ...

    def decodeHeader(self, decoder: ghidra.program.model.pcode.Decoder) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def followsFlow(self) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFixedHandle(self, hand: ghidra.app.plugin.processors.sleigh.FixedHandle, walker: ghidra.app.plugin.processors.sleigh.ParserWalker) -> None: ...

    def getHigh(self) -> int:
        """
        Get ending bit of context value within its context register.
        @return the ending bit
        """
        ...

    def getId(self) -> int: ...

    def getInternalHigh(self) -> int:
        """
        Get the ending bit of the context value within the "global" buffer, after
         the values have been packed.
        @return the ending bit
        """
        ...

    def getInternalLow(self) -> int:
        """
        Get the starting bit of the context value within the "global" buffer, after
         the values have been packed.
        @return the starting bit
        """
        ...

    def getLow(self) -> int:
        """
        Get starting bit of context value within its context register.
        @return the starting bit
        """
        ...

    def getName(self) -> unicode: ...

    def getPatternExpression(self) -> ghidra.app.plugin.processors.sleigh.expression.PatternExpression: ...

    def getPatternValue(self) -> ghidra.app.plugin.processors.sleigh.expression.PatternValue: ...

    def getScopeId(self) -> int: ...

    def getVarnode(self) -> ghidra.app.plugin.processors.sleigh.symbol.VarnodeSymbol: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def print(self, walker: ghidra.app.plugin.processors.sleigh.ParserWalker) -> unicode: ...

    def printList(self, __a0: ghidra.app.plugin.processors.sleigh.ParserWalker, __a1: java.util.ArrayList) -> None: ...

    def resolve(self, walker: ghidra.app.plugin.processors.sleigh.ParserWalker, debug: ghidra.app.plugin.processors.sleigh.SleighDebugLogger) -> ghidra.app.plugin.processors.sleigh.Constructor: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def high(self) -> int: ...

    @property
    def internalHigh(self) -> int: ...

    @property
    def internalLow(self) -> int: ...

    @property
    def low(self) -> int: ...

    @property
    def varnode(self) -> ghidra.app.plugin.processors.sleigh.symbol.VarnodeSymbol: ...