from typing import List
from typing import overload
import docking.action
import ghidra.plugins.fsbrowser
import ghidra.util.classfinder
import java.lang


class FSBFileHandler(ghidra.util.classfinder.ExtensionPoint, object):
    """
    Extension point, used by the FSBComponentProvider to create actions that appear
     in the fsb tree, and to delegate focus and default actions.
    """









    def createActions(self) -> List[docking.action.DockingAction]:
        """
        Returns a list of {@link DockingAction}s that should be 
         {@link PluginTool#addLocalAction(docking.ComponentProvider, docking.action.DockingActionIf) added}
         to the {@link FSBComponentProvider} tree as local actions.
        @return list of {@link DockingAction}s
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def fileDefaultAction(self, fileNode: ghidra.plugins.fsbrowser.FSBFileNode) -> bool:
        """
        Called when a file node is the target of a 'default action' initiated by the user, such
         as a double click, etc.
        @param fileNode {@link FSBFileNode} that was acted upon
        @return boolean true if action was taken, false if no action was taken
        """
        ...

    def fileFocused(self, fileNode: ghidra.plugins.fsbrowser.FSBFileNode) -> bool:
        """
        Called when a file node is focused in the {@link FSBComponentProvider} tree.
        @param fileNode {@link FSBFileNode} that was focused
        @return boolean true if action was taken
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getPopupProviderActions(self) -> List[docking.action.DockingAction]:
        """
        Returns a list of {@link DockingAction}s that should be added to a popup menu.  Called
         each time a fsb browser tree popup menu is created.
         <p>
         Only use this method to provide actions when the actions need to be created freshly
         for each popup event.  Normal long-lived actions should be published by the
         {@link #createActions()} method.
        @return list of {@link DockingAction}s
        """
        ...

    def hashCode(self) -> int: ...

    def init(self, context: ghidra.plugins.fsbrowser.FSBFileHandlerContext) -> None:
        """
        Called once after creation of each instance to provide useful info
        @param context references to useful objects and services
        """
        ...

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
    def popupProviderActions(self) -> List[object]: ...