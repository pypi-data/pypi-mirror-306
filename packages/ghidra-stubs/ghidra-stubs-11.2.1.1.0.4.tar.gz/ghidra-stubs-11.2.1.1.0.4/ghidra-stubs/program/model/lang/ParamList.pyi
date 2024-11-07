from typing import List
from typing import overload
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.lang
import ghidra.program.model.lang.ParamList
import ghidra.program.model.listing
import ghidra.program.model.pcode
import ghidra.xml
import java.lang
import java.util


class ParamList(object):
    """
    A group of ParamEntry that form a complete set for passing parameters (in one direction)
    """






    class WithSlotRec(object):




        def __init__(self): ...



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







    def assignMap(self, __a0: ghidra.program.model.lang.PrototypePieces, __a1: ghidra.program.model.data.DataTypeManager, __a2: java.util.ArrayList, __a3: bool) -> None: ...

    def encode(self, encoder: ghidra.program.model.pcode.Encoder, isInput: bool) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getPotentialRegisterStorage(self, prog: ghidra.program.model.listing.Program) -> List[ghidra.program.model.listing.VariableStorage]:
        """
        Get a list of all parameter storage locations consisting of a single register
        @param prog is the controlling program
        @return an array of VariableStorage
        """
        ...

    def getSpacebase(self) -> ghidra.program.model.address.AddressSpace:
        """
        Get the address space associated with any stack based parameters in this list.
        @return the stack address space, if this models parameters passed on the stack, null otherwise
        """
        ...

    def getStackParameterAlignment(self) -> int:
        """
        Return the amount of alignment used for parameters passed on the stack, or -1 if there are no stack params
        @return the alignment
        """
        ...

    def getStackParameterOffset(self) -> long:
        """
        Find the boundary offset that separates parameters on the stack from other local variables
         This is usually the address of the first stack parameter, but if the stack grows positive, this is
         the first address AFTER the parameters on the stack
        @return the boundary offset
        """
        ...

    def hashCode(self) -> int: ...

    def isEquivalent(self, obj: ghidra.program.model.lang.ParamList) -> bool:
        """
        Determine if this ParmList is equivalent to another instance
        @param obj is the other instance
        @return true if they are equivalent
        """
        ...

    def isThisBeforeRetPointer(self) -> bool:
        """
        Return true if the this pointer occurs before an indirect return pointer
 
         The automatic parameters: this parameter and the hidden return value pointer both
         tend to be allocated from the initial general purpose registers reserved for parameter passing.
         This method returns true if the this parameter is allocated first.
        @return false if the hidden return value pointer is allocated first
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def possibleParamWithSlot(self, loc: ghidra.program.model.address.Address, size: int, res: ghidra.program.model.lang.ParamList.WithSlotRec) -> bool:
        """
        Determine if a particular address range is a possible parameter, and if so what slot(s) it occupies
        @param loc is the starting address of the range
        @param size is the size of the range in bytes
        @param res holds the resulting slot and slotsize
        @return true if the range is a possible parameter
        """
        ...

    def restoreXml(self, parser: ghidra.xml.XmlPullParser, cspec: ghidra.program.model.lang.CompilerSpec) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def spacebase(self) -> ghidra.program.model.address.AddressSpace: ...

    @property
    def stackParameterAlignment(self) -> int: ...

    @property
    def stackParameterOffset(self) -> long: ...

    @property
    def thisBeforeRetPointer(self) -> bool: ...