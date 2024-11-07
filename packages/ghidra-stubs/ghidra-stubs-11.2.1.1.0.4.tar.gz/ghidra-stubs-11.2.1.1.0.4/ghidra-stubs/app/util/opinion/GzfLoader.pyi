from typing import List
from typing import overload
import ghidra.app.util
import ghidra.app.util.bin
import ghidra.app.util.importer
import ghidra.app.util.opinion
import ghidra.framework.model
import ghidra.program.model.listing
import ghidra.util.task
import java.lang
import java.util


class GzfLoader(object, ghidra.app.util.opinion.Loader):
    """
    Loads a packed Ghidra program.
    """

    COMMAND_LINE_ARG_PREFIX: unicode = u'-loader'
    GZF_NAME: unicode = u'GZF Input Format'
    OPTIONS_PROJECT_SAVE_STATE_KEY: unicode = u'LOADER_OPTIONS'
    loggingDisabled: bool = False



    def __init__(self): ...



    @overload
    def compareTo(self, __a0: ghidra.app.util.opinion.Loader) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def equals(self, __a0: object) -> bool: ...

    def findSupportedLoadSpecs(self, provider: ghidra.app.util.bin.ByteProvider) -> java.util.Collection: ...

    def getClass(self) -> java.lang.Class: ...

    def getDefaultOptions(self, provider: ghidra.app.util.bin.ByteProvider, loadSpec: ghidra.app.util.opinion.LoadSpec, domainObject: ghidra.framework.model.DomainObject, loadIntoProgram: bool) -> List[ghidra.app.util.Option]: ...

    def getName(self) -> unicode: ...

    def getPreferredFileName(self, provider: ghidra.app.util.bin.ByteProvider) -> unicode: ...

    def getTier(self) -> ghidra.app.util.opinion.LoaderTier: ...

    def getTierPriority(self) -> int: ...

    def hashCode(self) -> int: ...

    def load(self, __a0: ghidra.app.util.bin.ByteProvider, __a1: unicode, __a2: ghidra.framework.model.Project, __a3: unicode, __a4: ghidra.app.util.opinion.LoadSpec, __a5: List[object], __a6: ghidra.app.util.importer.MessageLog, __a7: object, __a8: ghidra.util.task.TaskMonitor) -> ghidra.app.util.opinion.LoadResults: ...

    def loadInto(self, __a0: ghidra.app.util.bin.ByteProvider, __a1: ghidra.app.util.opinion.LoadSpec, __a2: List[object], __a3: ghidra.app.util.importer.MessageLog, __a4: ghidra.program.model.listing.Program, __a5: ghidra.util.task.TaskMonitor) -> None: ...

    def loadsIntoNewFolder(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def supportsLoadIntoProgram(self) -> bool: ...

    @overload
    def supportsLoadIntoProgram(self, __a0: ghidra.program.model.listing.Program) -> bool: ...

    def toString(self) -> unicode: ...

    def validateOptions(self, __a0: ghidra.app.util.bin.ByteProvider, __a1: ghidra.app.util.opinion.LoadSpec, __a2: List[object], __a3: ghidra.program.model.listing.Program) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def name(self) -> unicode: ...

    @property
    def tier(self) -> ghidra.app.util.opinion.LoaderTier: ...

    @property
    def tierPriority(self) -> int: ...