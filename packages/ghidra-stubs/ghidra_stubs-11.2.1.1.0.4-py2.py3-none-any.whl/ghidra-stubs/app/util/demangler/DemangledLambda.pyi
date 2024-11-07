from typing import List
from typing import overload
import ghidra.app.util.demangler
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.model.symbol
import ghidra.util.task
import java.lang


class DemangledLambda(ghidra.app.util.demangler.DemangledFunction):
    """
    Represents a demangled lambda function
    """





    def __init__(self, mangled: unicode, originalDemangled: unicode, name: unicode): ...



    def addParameter(self, parameter: ghidra.app.util.demangler.DemangledParameter) -> None: ...

    def addParameters(self, __a0: List[object]) -> None: ...

    def applyPlateCommentOnly(self, program: ghidra.program.model.listing.Program, address: ghidra.program.model.address.Address) -> bool:
        """
        @param program The program for which to apply the comment
        @param address The address for the comment
        @return {@code true} if a comment was applied
        @throws Exception if the symbol could not be demangled or if the address is invalid
        """
        ...

    def applyTo(self, program: ghidra.program.model.listing.Program, address: ghidra.program.model.address.Address, options: ghidra.app.util.demangler.DemanglerOptions, monitor: ghidra.util.task.TaskMonitor) -> bool: ...

    @staticmethod
    def createNamespace(program: ghidra.program.model.listing.Program, typeNamespace: ghidra.app.util.demangler.Demangled, parentNamespace: ghidra.program.model.symbol.Namespace, functionPermitted: bool) -> ghidra.program.model.symbol.Namespace:
        """
        Get or create the specified typeNamespace.  The returned namespace may only be a partial
         namespace if errors occurred.  The caller should check the returned namespace and adjust
         any symbol creation accordingly.
        @param program the program
        @param typeNamespace demangled namespace
        @param parentNamespace root namespace to be used (e.g., library, global, etc.)
        @param functionPermitted if true an existing function may be used as a namespace
        @return namespace or partial namespace if error occurs
        """
        ...

    def demangledNameSuccessfully(self) -> bool:
        """
        Returns the success state of converting a mangled String into a demangled String
        @return true succeeded creating demangled String
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getBasedName(self) -> unicode: ...

    def getCallingConvention(self) -> unicode:
        """
        Returns the calling convention or null, if unspecified.
        @return the calling convention or null, if unspecified
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDemangledName(self) -> unicode: ...

    def getErrorMessage(self) -> unicode:
        """
        Returns the error message that can be set when an error is encountered, but which is made
         available to the calling method to get details of the error beyond boolean value that is
         returned by {@link #applyTo(Program, Address, DemanglerOptions,TaskMonitor)}.
        @return a message pertaining to issues encountered in the apply methods.  Can be null
        """
        ...

    def getMangledString(self) -> unicode: ...

    def getMemberScope(self) -> unicode: ...

    def getName(self) -> unicode: ...

    def getNamespace(self) -> ghidra.app.util.demangler.Demangled: ...

    def getNamespaceName(self) -> unicode: ...

    def getNamespaceString(self) -> unicode: ...

    def getOriginalDemangled(self) -> unicode: ...

    def getParameterString(self) -> unicode: ...

    def getParameters(self) -> List[ghidra.app.util.demangler.DemangledParameter]: ...

    def getReturnType(self) -> ghidra.app.util.demangler.DemangledDataType:
        """
        Returns the return type or null, if unspecified.
        @return the return type or null, if unspecified
        """
        ...

    @overload
    def getSignature(self) -> unicode: ...

    @overload
    def getSignature(self, format: bool) -> unicode: ...

    def getSignatureSourceType(self) -> ghidra.program.model.symbol.SourceType:
        """
        Get the signature source type which is used when applying the function signature
         to a program. A value of {@link SourceType#DEFAULT} indicates that 
         function return and parameters should not be applied.
        @return signature source type
        """
        ...

    def getSpecialPrefix(self) -> unicode: ...

    def getStorageClass(self) -> unicode: ...

    def getTemplate(self) -> ghidra.app.util.demangler.DemangledTemplate: ...

    def getVisibility(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def isConst(self) -> bool: ...

    def isPointer64(self) -> bool: ...

    def isRestrict(self) -> bool: ...

    def isStatic(self) -> bool: ...

    def isThunk(self) -> bool: ...

    def isTrailingConst(self) -> bool: ...

    def isTrailingPointer64(self) -> bool: ...

    def isTrailingRestrict(self) -> bool: ...

    def isTrailingUnaligned(self) -> bool: ...

    def isTrailingVolatile(self) -> bool: ...

    def isTypeCast(self) -> bool: ...

    def isUnaligned(self) -> bool: ...

    def isVirtual(self) -> bool: ...

    def isVolatile(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setBackupPlateComment(self, plateComment: unicode) -> None:
        """
        Sets the plate comment to be used if the {@link #getOriginalDemangled()} string is not
         available
        @param plateComment the plate comment text
        """
        ...

    def setBasedName(self, basedName: unicode) -> None: ...

    def setCallingConvention(self, callingConvention: unicode) -> None:
        """
        Sets the function calling convention. For example, "__cdecl".
        @param callingConvention the function calling convention
        """
        ...

    def setConst(self, isConst: bool) -> None: ...

    def setMemberScope(self, memberScope: unicode) -> None: ...

    def setName(self, name: unicode) -> None:
        """
        Sets the name of the demangled object
        @param name the new name
        """
        ...

    def setNamespace(self, namespace: ghidra.app.util.demangler.Demangled) -> None: ...

    def setOriginalDemangled(self, originalDemangled: unicode) -> None:
        """
        Sets the original demangled string.  This is useful for clients that reuse constructed
         demangled objects for special case constructs.
         <p>
         Note: this method is not on the interface
        @param originalDemangled the new original demangled string
        """
        ...

    def setOverloadedOperator(self, isOverloadedOperator: bool) -> None:
        """
        Sets whether this demangled function represents
         an overloaded operator. For example, "operator+()".
        @param isOverloadedOperator true if overloaded operator
        """
        ...

    def setPointer64(self, isPointer64: bool) -> None: ...

    def setRestrict(self) -> None: ...

    def setReturnType(self, returnType: ghidra.app.util.demangler.DemangledDataType) -> None:
        """
        Sets the function return type.
        @param returnType the function return type
        """
        ...

    def setSignatureSourceType(self, signatureSourceType: ghidra.program.model.symbol.SourceType) -> None:
        """
        Set signature {@link SourceType} of {@link SourceType#ANALYSIS} which will be used
         when function signatures are applied to a program.  Specifying {@link SourceType#DEFAULT} 
         will prevent function return and parameters from being applied but will still apply
         calling convention name if specified.
        @param signatureSourceType signature source type
        """
        ...

    def setSpecialPrefix(self, special: unicode) -> None: ...

    def setStatic(self, isStatic: bool) -> None: ...

    def setStorageClass(self, storageClass: unicode) -> None: ...

    def setTemplate(self, template: ghidra.app.util.demangler.DemangledTemplate) -> None: ...

    def setTemplatedConstructorType(self, type: unicode) -> None:
        """
        Special constructor where it has a templated type before the parameter list
        @param type the type
        """
        ...

    def setThrowAttribute(self, throwAttribute: unicode) -> None: ...

    def setThunk(self, isThunk: bool) -> None: ...

    def setTrailingConst(self) -> None: ...

    def setTrailingPointer64(self) -> None: ...

    def setTrailingRestrict(self) -> None: ...

    def setTrailingUnaligned(self) -> None: ...

    def setTrailingVolatile(self) -> None: ...

    def setTypeCast(self) -> None: ...

    def setUnaligned(self) -> None: ...

    def setVirtual(self, isVirtual: bool) -> None: ...

    def setVisibilty(self, visibility: unicode) -> None: ...

    def setVolatile(self, isVolatile: bool) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def namespaceName(self) -> unicode: ...