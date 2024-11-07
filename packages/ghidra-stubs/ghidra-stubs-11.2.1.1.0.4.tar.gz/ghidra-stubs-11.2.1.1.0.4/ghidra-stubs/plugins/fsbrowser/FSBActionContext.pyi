from typing import List
from typing import overload
import docking
import docking.widgets.tree
import ghidra.formats.gfilesystem
import ghidra.plugins.fsbrowser
import java.awt
import java.awt.event
import java.lang


class FSBActionContext(docking.DefaultActionContext):
    """
    FSBComponentProvider context for actions
    """





    def __init__(self, __a0: ghidra.plugins.fsbrowser.FSBComponentProvider, __a1: List[object], __a2: java.awt.event.MouseEvent, __a3: docking.widgets.tree.GTree): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getComponentProvider(self) -> ghidra.plugins.fsbrowser.FSBComponentProvider: ...

    def getContextObject(self) -> List[ghidra.plugins.fsbrowser.FSBNode]: ...

    def getEventClickModifiers(self) -> int: ...

    def getFSRL(self, dirsOk: bool) -> ghidra.formats.gfilesystem.FSRL:
        """
        Returns the {@link FSRL} of the currently selected item, as long as it conforms to
         the dirsOk requirement.
        @param dirsOk boolean flag, if true the selected item can be either a file or directory
         element, if false, it must be a file or the root of a file system that has a container
         file
        @return FSRL of the single selected item, null if no items selected or more than 1 item
         selected
        """
        ...

    def getFSRLs(self, dirsOk: bool) -> List[ghidra.formats.gfilesystem.FSRL]:
        """
        Returns a list of FSRLs of the currently selected nodes in the tree.
        @param dirsOk boolean flag, if true the selected items can be either a file or directory
         element, if false, it must be a file or the root of a file system that has a container
         file before being included in the resulting list
        @return list of FSRLs of the currently selected items, maybe empty but never null
        """
        ...

    def getFileFSRL(self) -> ghidra.formats.gfilesystem.FSRL:
        """
        Returns the FSRL of the currently selected file node
        @return FSRL of the currently selected file, or null if not file or more than 1 selected
        """
        ...

    def getFileFSRLs(self) -> List[ghidra.formats.gfilesystem.FSRL]:
        """
        Returns a list of FSRLs of the currently selected file nodes in the tree.
        @return list of FSRLs of the currently selected file items, maybe empty but never null
        """
        ...

    def getLoadableFSRL(self) -> ghidra.formats.gfilesystem.FSRL:
        """
        Returns the FSRL of the currently selected item, if it is a 'loadable' item.
        @return FSRL of the currently selected loadable item, or null if nothing selected or
         more than 1 selected
        """
        ...

    def getMouseEvent(self) -> java.awt.event.MouseEvent: ...

    def getSelectedCount(self) -> int:
        """
        Returns the number of selected nodes in the tree.
        @return returns the number of selected nodes in the tree.
        """
        ...

    def getSelectedNode(self) -> ghidra.plugins.fsbrowser.FSBNode:
        """
        Returns the currently selected tree node
        @return the currently selected tree node, or null if no nodes or more than 1 node is selected
        """
        ...

    def getSelectedNodes(self) -> List[ghidra.plugins.fsbrowser.FSBNode]:
        """
        Returns a list of the currently selected tree nodes.
        @return list of currently selected tree nodes
        """
        ...

    def getSourceComponent(self) -> docking.widgets.tree.GTree: ...

    def getSourceObject(self) -> object: ...

    def getTree(self) -> docking.widgets.tree.GTree:
        """
        Gets the {@link FileSystemBrowserPlugin} provider's  tree.
        @return The {@link FileSystemBrowserPlugin} provider's  tree.
        """
        ...

    def hasAnyEventClickModifiers(self, modifiersMask: int) -> bool: ...

    def hasSelectedLinkedNodes(self) -> bool: ...

    def hasSelectedNodes(self) -> bool:
        """
        Returns true if there are selected nodes in the browser tree.
        @return boolean true if there are selected nodes in the browser tree
        """
        ...

    def hashCode(self) -> int: ...

    def isBusy(self) -> bool:
        """
        Returns true if the GTree is busy
        @return boolean true if the GTree is busy
        """
        ...

    def isSelectedAllDirs(self) -> bool:
        """
        Returns true if the currently selected items are all directory items
        @return boolean true if the currently selected items are all directory items
        """
        ...

    def notBusy(self) -> bool:
        """
        Returns true if the GTree is not busy
        @return boolean true if GTree is not busy
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setContextObject(self, contextObject: object) -> docking.DefaultActionContext: ...

    def setEventClickModifiers(self, modifiers: int) -> None: ...

    def setMouseEvent(self, e: java.awt.event.MouseEvent) -> docking.DefaultActionContext: ...

    def setSourceComponent(self, sourceComponent: java.awt.Component) -> docking.ActionContext: ...

    def setSourceObject(self, sourceObject: object) -> docking.DefaultActionContext: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def busy(self) -> bool: ...

    @property
    def componentProvider(self) -> ghidra.plugins.fsbrowser.FSBComponentProvider: ...

    @property
    def contextObject(self) -> List[object]: ...

    @property
    def fileFSRL(self) -> ghidra.formats.gfilesystem.FSRL: ...

    @property
    def fileFSRLs(self) -> List[object]: ...

    @property
    def loadableFSRL(self) -> ghidra.formats.gfilesystem.FSRL: ...

    @property
    def selectedAllDirs(self) -> bool: ...

    @property
    def selectedCount(self) -> int: ...

    @property
    def selectedNode(self) -> ghidra.plugins.fsbrowser.FSBNode: ...

    @property
    def selectedNodes(self) -> List[object]: ...

    @property
    def sourceComponent(self) -> docking.widgets.tree.GTree: ...

    @property
    def tree(self) -> docking.widgets.tree.GTree: ...