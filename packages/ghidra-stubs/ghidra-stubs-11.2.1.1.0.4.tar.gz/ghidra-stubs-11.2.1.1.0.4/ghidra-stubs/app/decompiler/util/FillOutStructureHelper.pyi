from typing import List
from typing import overload
import ghidra.app.decompiler
import ghidra.app.decompiler.util.FillOutStructureHelper
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.program.model.pcode
import java.lang


class FillOutStructureHelper(object):
    """
    Automatically create a Structure data-type based on references found by the decompiler to a
     root parameter or other variable.

     If the parameter is already a Structure pointer, any new references found can optionally be added
     to the existing Structure data-type.
     #processStructure(HighVariable, Function, boolean, boolean, DecompInterface) is the primary
     entry point to the helper, which computes the new or updated Structure based on an existing
     decompiled function. Decompilation, if not provided externally, can be performed by calling
     #computeHighVariable(Address, Function, DecompInterface).  A decompiler process,
     if not provided externally, can be started by calling #setUpDecompiler(DecompileOptions).
    """






    class OffsetPcodeOpPair(object):




        def __init__(self, __a0: long, __a1: ghidra.program.model.pcode.PcodeOp): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getOffset(self) -> long: ...

        def getPcodeOp(self) -> ghidra.program.model.pcode.PcodeOp: ...

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
        def offset(self) -> long: ...

        @property
        def pcodeOp(self) -> ghidra.program.model.pcode.PcodeOp: ...

    def __init__(self, program: ghidra.program.model.listing.Program, monitor: ghidra.util.task.TaskMonitor):
        """
        Constructor.
        @param program the current program
        @param monitor task monitor
        """
        ...



    def computeHighVariable(self, storageAddress: ghidra.program.model.address.Address, function: ghidra.program.model.listing.Function, decomplib: ghidra.app.decompiler.DecompInterface) -> ghidra.program.model.pcode.HighVariable:
        """
        Decompile a function and return the resulting HighVariable associated with a storage address
        @param storageAddress the storage address of the variable
        @param function is the function
        @param decomplib is the active interface to use for decompiling
        @return the corresponding HighVariable or null
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getComponentMap(self) -> ghidra.program.model.data.NoisyStructureBuilder:
        """
        Retrieve the component map that was generated when structure was created using decompiler 
         info. Results are not valid until 
         {@link #processStructure(HighVariable, Function, boolean, boolean, DecompInterface)} is invoked.
        @return componentMap
        """
        ...

    def getLoadPcodeOps(self) -> List[ghidra.app.decompiler.util.FillOutStructureHelper.OffsetPcodeOpPair]:
        """
        Retrieve the offset/pcodeOp pairs that are used to load data from the variable
         used to fill-out structure.
         Results are not valid until 
         {@link #processStructure(HighVariable, Function, boolean, boolean, DecompInterface)} is invoked.
        @return the pcodeOps doing the loading from the associated variable
        """
        ...

    def getStorePcodeOps(self) -> List[ghidra.app.decompiler.util.FillOutStructureHelper.OffsetPcodeOpPair]:
        """
        Retrieve the offset/pcodeOp pairs that are used to store data into the variable
         used to fill-out structure.
         Results are not valid until 
         {@link #processStructure(HighVariable, Function, boolean, boolean, DecompInterface)} is invoked.
        @return the pcodeOps doing the storing to the associated variable
        """
        ...

    @staticmethod
    def getStructureForExtending(dt: ghidra.program.model.data.DataType) -> ghidra.program.model.data.Structure:
        """
        Check if a variable has a data-type that is suitable for being extended.
         If so return the structure data-type, otherwise return null.
         Modulo typedefs, the data-type of the variable must be exactly a
         "pointer to a structure".  Not a "structure" itself, or a
         "pointer to a pointer to ... a structure".
        @param dt is the data-type of the variable to test
        @return the extendable structure data-type or null
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def processStructure(self, var: ghidra.program.model.pcode.HighVariable, function: ghidra.program.model.listing.Function, createNewStructure: bool, createClassIfNeeded: bool, decomplib: ghidra.app.decompiler.DecompInterface) -> ghidra.program.model.data.Structure:
        """
        Create or update a Structure data-type given a function and a root pointer variable.
         The function must already be decompiled, but if a decompiler interface is provided, this
         method will recursively follow variable references into CALLs, possibly triggering additional
         decompilation.
        @param var is the pointer variable
        @param function is the function to process
        @param createNewStructure if true a new Structure with a unique name will always be generated,
         if false and the variable corresponds to a Structure pointer, the existing Structure will be 
         updated instead.
        @param createClassIfNeeded if true and variable corresponds to a <B>this</B> pointer without 
         an assigned Ghidra Class (i.e., {@code void * this}), the function will be assigned to a 
         new unique Ghidra Class namespace with a new identically named Structure returned.  If false,
         a new unique Structure will be created.
        @param decomplib is the (optional) decompiler interface, which can be used to recursively
         decompile into CALLs.
        @return a filled-in Structure or null if one could not be created
        """
        ...

    def setUpDecompiler(self, options: ghidra.app.decompiler.DecompileOptions) -> ghidra.app.decompiler.DecompInterface:
        """
        Set up a decompiler interface and prepare for decompiling on the currentProgram. 
         The interface can be used to pass to computeHighVariable or to processStructure.
        @param options are the options to pass to the decompiler
        @return the decompiler interface
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def componentMap(self) -> ghidra.program.model.data.NoisyStructureBuilder: ...

    @property
    def loadPcodeOps(self) -> List[object]: ...

    @property
    def storePcodeOps(self) -> List[object]: ...

    @property
    def upDecompiler(self) -> None: ...  # No getter available.

    @upDecompiler.setter
    def upDecompiler(self, value: ghidra.app.decompiler.DecompileOptions) -> None: ...