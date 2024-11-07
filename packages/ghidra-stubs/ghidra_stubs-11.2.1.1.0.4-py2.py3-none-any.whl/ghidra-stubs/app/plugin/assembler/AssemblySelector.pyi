from typing import overload
import ghidra.app.plugin.assembler.AssemblySelector
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang
import java.util


class AssemblySelector(object):
    """
    Provides a mechanism for pruning and selecting binary assembled instructions from the results of
     parsing textual assembly instructions. There are two opportunities: After parsing, but before
     prototype generation, and after machine code generation. In the first opportunity, filtering is
     optional --- the user may discard any or all parse trees. The second is required, since only one
     instruction may be placed at the desired address --- the user must select one instruction among
     the many results, and if a mask is present, decide on a value for the omitted bits.
 
 
     Extensions of this class are also suitable for collecting diagnostic information about attempted
     assemblies. For example, an implementation may employ the syntax errors in order to produce code
     completion suggestions in a GUI.
    """






    class Selection(java.lang.Record):




        def __init__(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock, __a1: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock): ...



        def ctx(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def ins(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def filterParse(self, parse: java.util.Collection) -> java.util.Collection:
        """
        Filter a collection of parse trees.
 
         <p>
         Generally, the assembly resolver considers every possible parsing of an assembly instruction.
         If, for some reason, the user wishes to ignore certain trees (perhaps for efficiency, or
         perhaps because a certain form of instruction is desired), entire parse trees may be pruned
         here.
 
         <p>
         It is possible that no trees pass the filter. In this case, this method ought to throw an
         {@link AssemblySyntaxException}. Another option is to pass the erroneous result on for
         semantic analysis, in which case, the error is simply copied into an erroneous semantic
         result. Depending on preferences, this may simplify the overall filtering and error-handling
         logic.
 
         <p>
         By default, no filtering is applied. If all the trees produce syntax errors, an exception is
         thrown.
        @param parse the collection of parse results (errors and trees).
        @return the filtered collection, optionally in-place.
        @throws AssemblySyntaxException if the selector wishes to forward one or more syntax errors
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def select(self, rr: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults, ctx: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> ghidra.app.plugin.assembler.AssemblySelector.Selection:
        """
        Select an instruction from the possible results.
 
         <p>
         This must select precisely one resolved constructor from the results given back by the
         assembly resolver. This further implies the mask of the returned result must consist of all
         1s. If no selection is suitable, this must throw an exception.
 
         <p>
         By default, this method selects the shortest instruction that is compatible with the given
         context and takes 0 for bits that fall outside the mask. If all possible resolutions produce
         errors, an exception is thrown.
        @param rr the collection of resolved constructors
        @param ctx the applicable context.
        @return a single resolved constructor with a full instruction mask.
        @throws AssemblySemanticException if all the given results are semantic errors
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

