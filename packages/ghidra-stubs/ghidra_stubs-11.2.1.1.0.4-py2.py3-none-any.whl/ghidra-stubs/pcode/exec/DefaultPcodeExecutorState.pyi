from typing import overload
import ghidra.pcode.exec
import ghidra.pcode.exec.PcodeArithmetic
import ghidra.pcode.exec.PcodeExecutorStatePiece
import ghidra.program.model.address
import ghidra.program.model.lang
import ghidra.program.model.mem
import ghidra.program.model.pcode
import java.lang
import java.util


class DefaultPcodeExecutorState(object, ghidra.pcode.exec.PcodeExecutorState):
    """
    A p-code executor state formed from a piece whose address and value types are the same

 
     This class will also wire in the arithmetic's
     PcodeArithmetic#modBeforeStore(int, int, Object, int, Object) and
     PcodeArithmetic#modAfterLoad(int, int, Object, int, Object), which is only possible when
     the address and value type are guaranteed to match.
    """





    @overload
    def __init__(self, piece: ghidra.pcode.exec.PcodeExecutorStatePiece): ...

    @overload
    def __init__(self, piece: ghidra.pcode.exec.PcodeExecutorStatePiece, arithmetic: ghidra.pcode.exec.PcodeArithmetic): ...



    def checkRange(self, __a0: ghidra.program.model.address.AddressSpace, __a1: long, __a2: int) -> None: ...

    def clear(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def fork(self) -> ghidra.pcode.exec.DefaultPcodeExecutorState: ...

    def getAddressArithmetic(self) -> ghidra.pcode.exec.PcodeArithmetic: ...

    def getArithmetic(self) -> ghidra.pcode.exec.PcodeArithmetic: ...

    def getClass(self) -> java.lang.Class: ...

    def getConcreteBuffer(self, address: ghidra.program.model.address.Address, purpose: ghidra.pcode.exec.PcodeArithmetic.Purpose) -> ghidra.program.model.mem.MemBuffer: ...

    def getLanguage(self) -> ghidra.program.model.lang.Language: ...

    def getRegisterValues(self) -> java.util.Map: ...

    @overload
    def getVar(self, __a0: ghidra.program.model.lang.Register, __a1: ghidra.pcode.exec.PcodeExecutorStatePiece.Reason) -> object: ...

    @overload
    def getVar(self, __a0: ghidra.program.model.pcode.Varnode, __a1: ghidra.pcode.exec.PcodeExecutorStatePiece.Reason) -> object: ...

    @overload
    def getVar(self, __a0: ghidra.program.model.address.Address, __a1: int, __a2: bool, __a3: ghidra.pcode.exec.PcodeExecutorStatePiece.Reason) -> object: ...

    @overload
    def getVar(self, space: ghidra.program.model.address.AddressSpace, offset: long, size: int, quantize: bool, reason: ghidra.pcode.exec.PcodeExecutorStatePiece.Reason) -> object: ...

    @overload
    def getVar(self, space: ghidra.program.model.address.AddressSpace, offset: object, size: int, quantize: bool, reason: ghidra.pcode.exec.PcodeExecutorStatePiece.Reason) -> object: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def paired(self, __a0: ghidra.pcode.exec.PcodeExecutorStatePiece) -> ghidra.pcode.exec.PcodeExecutorState: ...

    def quantizeOffset(self, __a0: ghidra.program.model.address.AddressSpace, __a1: long) -> long: ...

    @overload
    def setVar(self, __a0: ghidra.program.model.lang.Register, __a1: object) -> None: ...

    @overload
    def setVar(self, __a0: ghidra.program.model.pcode.Varnode, __a1: object) -> None: ...

    @overload
    def setVar(self, __a0: ghidra.program.model.address.Address, __a1: int, __a2: bool, __a3: object) -> None: ...

    @overload
    def setVar(self, space: ghidra.program.model.address.AddressSpace, offset: long, size: int, quantize: bool, val: object) -> None: ...

    @overload
    def setVar(self, space: ghidra.program.model.address.AddressSpace, offset: object, size: int, quantize: bool, val: object) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def addressArithmetic(self) -> ghidra.pcode.exec.PcodeArithmetic: ...

    @property
    def arithmetic(self) -> ghidra.pcode.exec.PcodeArithmetic: ...

    @property
    def language(self) -> ghidra.program.model.lang.Language: ...

    @property
    def registerValues(self) -> java.util.Map: ...