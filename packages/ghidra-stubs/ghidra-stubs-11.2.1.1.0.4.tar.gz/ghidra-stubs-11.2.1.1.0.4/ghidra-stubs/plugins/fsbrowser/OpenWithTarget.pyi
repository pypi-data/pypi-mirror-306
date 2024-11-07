from typing import List
from typing import overload
import ghidra.app.services
import ghidra.framework.plugintool
import ghidra.plugins.fsbrowser
import java.lang
import javax.swing


class OpenWithTarget(object):
    """
    Represents a way to open a DomainFile in a ProgramManager
    """





    def __init__(self, name: unicode, pm: ghidra.app.services.ProgramManager, icon: javax.swing.Icon): ...



    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def getAll() -> List[ghidra.plugins.fsbrowser.OpenWithTarget]:
        """
        Returns a list of all running tools and tool templates that can be used to open a domainfile.
        @return list of OpenWithTarget instances, maybe empty but not null
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getDefault(tool: ghidra.framework.plugintool.PluginTool) -> ghidra.plugins.fsbrowser.OpenWithTarget:
        """
        Returns an OpenWithTarget, or null, that represents the specified tool's default ability 
         to open a {@link DomainFile}.
        @param tool a {@link PluginTool}
        @return a {@link OpenWithTarget}, or null if the specified tool can't open a domain file
        """
        ...

    def getIcon(self) -> javax.swing.Icon: ...

    def getName(self) -> unicode: ...

    def getPm(self) -> ghidra.app.services.ProgramManager: ...

    @staticmethod
    def getRunningProgramManager(tool: ghidra.framework.plugintool.PluginTool) -> ghidra.plugins.fsbrowser.OpenWithTarget:
        """
        Returns an OpenWithTarget, or null, that represents a running {@link ProgramManager}.
        @param tool a {@link PluginTool}
        @return a {@link OpenWithTarget}, or null if there is no open {@link ProgramManager}
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def open(self, __a0: List[object]) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def icon(self) -> javax.swing.Icon: ...

    @property
    def name(self) -> unicode: ...

    @property
    def pm(self) -> ghidra.app.services.ProgramManager: ...