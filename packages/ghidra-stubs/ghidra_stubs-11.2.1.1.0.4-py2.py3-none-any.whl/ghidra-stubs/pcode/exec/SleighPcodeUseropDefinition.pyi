from typing import List
from typing import overload
import ghidra.pcode.exec
import ghidra.program.model.pcode
import java.lang
import java.util


class SleighPcodeUseropDefinition(object, ghidra.pcode.exec.PcodeUseropLibrary.PcodeUseropDefinition):
    """
    A p-code userop defined using Sleigh source
    """

    OUT_SYMBOL_NAME: unicode = u'__op_output'




    class Builder(object):








        def body(self, __a0: java.lang.CharSequence) -> ghidra.pcode.exec.SleighPcodeUseropDefinition.Builder: ...

        def build(self) -> ghidra.pcode.exec.SleighPcodeUseropDefinition: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        def params(self, __a0: List[unicode]) -> ghidra.pcode.exec.SleighPcodeUseropDefinition.Builder: ...

        @overload
        def params(self, __a0: java.util.Collection) -> ghidra.pcode.exec.SleighPcodeUseropDefinition.Builder: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class Factory(object):




        def __init__(self, __a0: ghidra.app.plugin.processors.sleigh.SleighLanguage): ...



        def define(self, __a0: unicode) -> ghidra.pcode.exec.SleighPcodeUseropDefinition.Builder: ...

        def equals(self, __a0: object) -> bool: ...

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







    def equals(self, __a0: object) -> bool: ...

    def execute(self, __a0: ghidra.pcode.exec.PcodeExecutor, __a1: ghidra.pcode.exec.PcodeUseropLibrary, __a2: ghidra.program.model.pcode.Varnode, __a3: List[object]) -> None: ...

    def getBody(self) -> unicode:
        """
        Get the Sleigh source that defines this userop
        @return the lines
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getInputCount(self) -> int: ...

    def getInputs(self) -> List[unicode]:
        """
        Get the names of the inputs in order
        @return the input names
        """
        ...

    def getName(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def programFor(self, __a0: ghidra.program.model.pcode.Varnode, __a1: List[object], __a2: ghidra.pcode.exec.PcodeUseropLibrary) -> ghidra.pcode.exec.PcodeProgram: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def body(self) -> unicode: ...

    @property
    def inputCount(self) -> int: ...

    @property
    def inputs(self) -> List[object]: ...

    @property
    def name(self) -> unicode: ...