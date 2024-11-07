from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyStateGenerator
import java.lang
import java.util.stream


class AssemblyOperandStateGenerator(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyStateGenerator):
    """
    The generator of AssemblyOperandState from AssemblyParseNumericToken

 
     In short, this handles generation of a single operand state for the operand and value recorded by
     the given parse token.
    """





    def __init__(self, resolver: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver, node: ghidra.app.plugin.assembler.sleigh.tree.AssemblyParseNumericToken, opSym: ghidra.app.plugin.processors.sleigh.symbol.OperandSymbol, fromLeft: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns):
        """
        Construct the operand state generator
        @param resolver the resolver
        @param node the node from which to generate the state
        @param fromLeft the accumulated patterns from the left sibling or parent
        @param opSym the operand symbol
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def generate(self, gc: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyStateGenerator.GeneratorContext) -> java.util.stream.Stream: ...

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

