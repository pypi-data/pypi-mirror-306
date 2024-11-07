from typing import overload
import ghidra.app.plugin.core.analysis
import ghidra.framework.options
import java.lang


class DWARFImportOptions(object):
    """
    Import options exposed by the DWARFAnalyzer
    """





    def __init__(self):
        """
        Create new instance
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDefaultCC(self) -> unicode: ...

    def getOptionsUpdater(self) -> ghidra.app.plugin.core.analysis.AnalysisOptionsUpdater:
        """
        See {@link Analyzer#getOptionsUpdater()}
        @return {@link AnalysisOptionsUpdater}
        """
        ...

    def hashCode(self) -> int: ...

    def isCopyRenameAnonTypes(self) -> bool:
        """
        Option to control a feature that copies anonymous types into a structure's "namespace"
         CategoryPath and giving that anonymous type a new name based on the structure's field's
         name.
        @return boolean flag.
        """
        ...

    def isCreateFuncSignatures(self) -> bool:
        """
        Option to control creating FunctionSignature datatypes for each function defintion
         found in the DWARF debug data.
        @return boolean flag.
        """
        ...

    def isElideTypedefsWithSameName(self) -> bool:
        """
        Option to control eliding typedef creation if the dest type has the same name.
        @return boolean true if the DWARF importer should skip creating a typedef if its
         dest has the same name.
        """
        ...

    def isIgnoreParamStorage(self) -> bool: ...

    def isImportDataTypes(self) -> bool:
        """
        Option to turn on/off the import of data types.
        @return boolean true if import should import data types.
        """
        ...

    def isImportFuncs(self) -> bool:
        """
        Option to turn on/off the import of funcs.
        @return boolean true if import should import funcs.
        """
        ...

    def isImportLocalVariables(self) -> bool: ...

    def isOrganizeTypesBySourceFile(self) -> bool:
        """
        Option to organize imported datatypes into sub-folders based on their source file name.
        @return boolean flag
        """
        ...

    def isOutputDIEInfo(self) -> bool:
        """
        Option to control tagging data types and functions with their DWARF DIE
         record number.
        @return boolean true if the DWARF importer should tag items with their DIE record
         number.
        """
        ...

    def isOutputInlineFuncComments(self) -> bool:
        """
        Option to control tagging inlined-functions with comments.
        @return boolean flag.
        """
        ...

    def isOutputLexicalBlockComments(self) -> bool:
        """
        Option to control tagging lexical blocks with Ghidra comments.
        @return boolean flag.
        """
        ...

    def isOutputSourceLineInfo(self) -> bool: ...

    def isOutputSourceLocationInfo(self) -> bool:
        """
        Option to control tagging data types and functions with their source code
         location (ie. filename : line number ) if the information is present in the DWARF record.
        @return boolean true if the DWARF importer should tag items with their source code location
         info.
        """
        ...

    def isSpecialCaseSizedBaseTypes(self) -> bool:
        """
        Option to recognize named base types that have an explicit size in the name (eg "int32_t)
         and use statically sized data types instead of compiler-dependent data types.
        @return boolean true if option is turned on
        """
        ...

    def isTryPackStructs(self) -> bool:
        """
        Option to enable packing on structures/unions created during the DWARF import.  If packing
         would change the structure's details, packing is left disabled.
        @return boolean flag
        """
        ...

    def isUseBookmarks(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def optionsChanged(self, options: ghidra.framework.options.Options) -> None:
        """
        See {@link Analyzer#optionsChanged(Options, ghidra.program.model.listing.Program)}
        @param options {@link Options}
        """
        ...

    def registerOptions(self, options: ghidra.framework.options.Options) -> None:
        """
        See {@link Analyzer#registerOptions(Options, ghidra.program.model.listing.Program)}
        @param options {@link Options}
        """
        ...

    def setCopyRenameAnonTypes(self, b: bool) -> None:
        """
        Option to control a feature that copies anonymous types into a structure's "namespace"
         CategoryPath and giving that anonymousfunction.getEntryPoint() type a new name based on the structure's field's
         name.
        @param b boolean flag to set.
        """
        ...

    def setCreateFuncSignatures(self, createFuncSignatures: bool) -> None:
        """
        Option to control creating FunctionSignature datatypes for each function defintion
         found in the DWARF debug data.
        @param createFuncSignatures boolean flag to set.
        """
        ...

    def setDefaultCC(self, defaultCC: unicode) -> None: ...

    def setElideTypedefsWithSameName(self, elide_typedefs_with_same_name: bool) -> None:
        """
        Option to control eliding typedef creation if the dest type has the same name.
        @param elide_typedefs_with_same_name boolean to set
        """
        ...

    def setIgnoreParamStorage(self, ignoreParamStorage: bool) -> None: ...

    def setImportDataTypes(self, importDataTypes: bool) -> None:
        """
        Option to turn on/off the import of data types.
        @param importDataTypes boolean to set
        """
        ...

    def setImportFuncs(self, output_Funcs: bool) -> None: ...

    def setImportLocalVariables(self, importLocalVariables: bool) -> None: ...

    def setOrganizeTypesBySourceFile(self, organizeTypesBySourceFile: bool) -> None:
        """
        Option to organize imported datatypes into sub-folders based on their source file name.
        @param organizeTypesBySourceFile boolean flag to set.
        """
        ...

    def setOutputDIEInfo(self, output_DWARF_die_info: bool) -> None:
        """
        Option to control tagging data types and functions with their DWARF DIE
         record number.
        @param output_DWARF_die_info boolean to set
        """
        ...

    def setOutputInlineFuncComments(self, output_InlineFunc_comments: bool) -> None: ...

    def setOutputLexicalBlockComments(self, output_LexicalBlock_comments: bool) -> None:
        """
        Option to control tagging lexical blocks with Ghidra comments.
        @param output_LexicalBlock_comments boolean flag to set.
        """
        ...

    def setOutputSourceLineInfo(self, outputSourceLineInfo: bool) -> None: ...

    def setOutputSourceLocationInfo(self, output_DWARF_location_info: bool) -> None:
        """
        Option to control tagging data types and functions with their source code
         location (ie. filename : line number ) if the information is present in the DWARF record.
        @param output_DWARF_location_info boolean to set
        """
        ...

    def setSpecialCaseSizedBaseTypes(self, b: bool) -> None:
        """
        Option to recognize named base types that have an explicit size in the name (eg "int32_t)
         and use statically sized data types instead of compiler-dependent data types.
        @param b true to turn option on, false to turn off
        """
        ...

    def setTryPackDataTypes(self, tryPackStructs: bool) -> None:
        """
        Option to enable packing on structures created during the DWARF import.  If packing
         would change the structure's details, packing is left disabled.
        @param tryPackStructs boolean flag to set
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
    def copyRenameAnonTypes(self) -> bool: ...

    @copyRenameAnonTypes.setter
    def copyRenameAnonTypes(self, value: bool) -> None: ...

    @property
    def createFuncSignatures(self) -> bool: ...

    @createFuncSignatures.setter
    def createFuncSignatures(self, value: bool) -> None: ...

    @property
    def defaultCC(self) -> unicode: ...

    @defaultCC.setter
    def defaultCC(self, value: unicode) -> None: ...

    @property
    def elideTypedefsWithSameName(self) -> bool: ...

    @elideTypedefsWithSameName.setter
    def elideTypedefsWithSameName(self, value: bool) -> None: ...

    @property
    def ignoreParamStorage(self) -> bool: ...

    @ignoreParamStorage.setter
    def ignoreParamStorage(self, value: bool) -> None: ...

    @property
    def importDataTypes(self) -> bool: ...

    @importDataTypes.setter
    def importDataTypes(self, value: bool) -> None: ...

    @property
    def importFuncs(self) -> bool: ...

    @importFuncs.setter
    def importFuncs(self, value: bool) -> None: ...

    @property
    def importLocalVariables(self) -> bool: ...

    @importLocalVariables.setter
    def importLocalVariables(self, value: bool) -> None: ...

    @property
    def optionsUpdater(self) -> ghidra.app.plugin.core.analysis.AnalysisOptionsUpdater: ...

    @property
    def organizeTypesBySourceFile(self) -> bool: ...

    @organizeTypesBySourceFile.setter
    def organizeTypesBySourceFile(self, value: bool) -> None: ...

    @property
    def outputDIEInfo(self) -> bool: ...

    @outputDIEInfo.setter
    def outputDIEInfo(self, value: bool) -> None: ...

    @property
    def outputInlineFuncComments(self) -> bool: ...

    @outputInlineFuncComments.setter
    def outputInlineFuncComments(self, value: bool) -> None: ...

    @property
    def outputLexicalBlockComments(self) -> bool: ...

    @outputLexicalBlockComments.setter
    def outputLexicalBlockComments(self, value: bool) -> None: ...

    @property
    def outputSourceLineInfo(self) -> bool: ...

    @outputSourceLineInfo.setter
    def outputSourceLineInfo(self, value: bool) -> None: ...

    @property
    def outputSourceLocationInfo(self) -> bool: ...

    @outputSourceLocationInfo.setter
    def outputSourceLocationInfo(self, value: bool) -> None: ...

    @property
    def specialCaseSizedBaseTypes(self) -> bool: ...

    @specialCaseSizedBaseTypes.setter
    def specialCaseSizedBaseTypes(self, value: bool) -> None: ...

    @property
    def tryPackDataTypes(self) -> None: ...  # No getter available.

    @tryPackDataTypes.setter
    def tryPackDataTypes(self, value: bool) -> None: ...

    @property
    def tryPackStructs(self) -> bool: ...

    @property
    def useBookmarks(self) -> bool: ...