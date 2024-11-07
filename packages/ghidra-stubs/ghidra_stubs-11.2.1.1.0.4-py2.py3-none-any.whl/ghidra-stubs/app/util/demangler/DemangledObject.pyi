from typing import overload
import ghidra.app.util.demangler
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.model.symbol
import ghidra.util.task
import java.lang


class DemangledObject(object, ghidra.app.util.demangler.Demangled):
    """
    A class to represent a demangled object.
    """









    def applyPlateCommentOnly(self, program: ghidra.program.model.listing.Program, address: ghidra.program.model.address.Address) -> bool:
        """
        @param program The program for which to apply the comment
        @param address The address for the comment
        @return {@code true} if a comment was applied
        @throws Exception if the symbol could not be demangled or if the address is invalid
        """
        ...

    def applyTo(self, program: ghidra.program.model.listing.Program, address: ghidra.program.model.address.Address, options: ghidra.app.util.demangler.DemanglerOptions, monitor: ghidra.util.task.TaskMonitor) -> bool:
        """
        Apply this demangled object detail to the specified program.
         <br>
         NOTE: An open Program transaction must be established prior to invoking this method.
        @param program program to which demangled data should be applied.
        @param address address which corresponds to this demangled object
        @param options options which control how demangled data is applied
        @param monitor task monitor
        @return true if successfully applied, else false
        @throws Exception if an error occurs during the apply operation
        """
        ...

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

    @overload
    def getSignature(self) -> unicode: ...

    @overload
    def getSignature(self, format: bool) -> unicode:
        """
        Returns a complete signature for the demangled symbol.
         <br>For example:
                    "unsigned long foo"
                    "unsigned char * ClassA::getFoo(float, short *)"
                    "void * getBar(int **, MyStruct &amp;)"
         <br><b>Note: based on the underlying mangling scheme, the
         return type may or may not be specified in the signature.</b>
        @param format true if signature should be pretty printed
        @return a complete signature for the demangled symbol
        """
        ...

    def getSpecialPrefix(self) -> unicode: ...

    def getStorageClass(self) -> unicode: ...

    def getVisibility(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def isConst(self) -> bool: ...

    def isPointer64(self) -> bool: ...

    def isRestrict(self) -> bool: ...

    def isStatic(self) -> bool: ...

    def isThunk(self) -> bool: ...

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

    def setPointer64(self, isPointer64: bool) -> None: ...

    def setRestrict(self) -> None: ...

    def setSpecialPrefix(self, special: unicode) -> None: ...

    def setStatic(self, isStatic: bool) -> None: ...

    def setStorageClass(self, storageClass: unicode) -> None: ...

    def setThunk(self, isThunk: bool) -> None: ...

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
    def backupPlateComment(self) -> None: ...  # No getter available.

    @backupPlateComment.setter
    def backupPlateComment(self, value: unicode) -> None: ...

    @property
    def basedName(self) -> unicode: ...

    @basedName.setter
    def basedName(self, value: unicode) -> None: ...

    @property
    def const(self) -> bool: ...

    @const.setter
    def const(self, value: bool) -> None: ...

    @property
    def demangledName(self) -> unicode: ...

    @property
    def errorMessage(self) -> unicode: ...

    @property
    def mangledString(self) -> unicode: ...

    @property
    def memberScope(self) -> unicode: ...

    @memberScope.setter
    def memberScope(self, value: unicode) -> None: ...

    @property
    def name(self) -> unicode: ...

    @name.setter
    def name(self, value: unicode) -> None: ...

    @property
    def namespace(self) -> ghidra.app.util.demangler.Demangled: ...

    @namespace.setter
    def namespace(self, value: ghidra.app.util.demangler.Demangled) -> None: ...

    @property
    def namespaceName(self) -> unicode: ...

    @property
    def namespaceString(self) -> unicode: ...

    @property
    def originalDemangled(self) -> unicode: ...

    @originalDemangled.setter
    def originalDemangled(self, value: unicode) -> None: ...

    @property
    def pointer64(self) -> bool: ...

    @pointer64.setter
    def pointer64(self, value: bool) -> None: ...

    @property
    def restrict(self) -> bool: ...

    @property
    def signature(self) -> unicode: ...

    @property
    def specialPrefix(self) -> unicode: ...

    @specialPrefix.setter
    def specialPrefix(self, value: unicode) -> None: ...

    @property
    def static(self) -> bool: ...

    @static.setter
    def static(self, value: bool) -> None: ...

    @property
    def storageClass(self) -> unicode: ...

    @storageClass.setter
    def storageClass(self, value: unicode) -> None: ...

    @property
    def thunk(self) -> bool: ...

    @thunk.setter
    def thunk(self, value: bool) -> None: ...

    @property
    def unaligned(self) -> bool: ...

    @property
    def virtual(self) -> bool: ...

    @virtual.setter
    def virtual(self, value: bool) -> None: ...

    @property
    def visibility(self) -> unicode: ...

    @property
    def visibilty(self) -> None: ...  # No getter available.

    @visibilty.setter
    def visibilty(self, value: unicode) -> None: ...

    @property
    def volatile(self) -> bool: ...

    @volatile.setter
    def volatile(self, value: bool) -> None: ...