from typing import overload
import docking
import ghidra.features.base.codecompare.panel
import ghidra.program.model.listing
import java.awt
import java.awt.event
import java.lang


class CodeComparisonActionContext(docking.DefaultActionContext, ghidra.features.base.codecompare.panel.CodeComparisonPanelActionContext):




    def __init__(self, provider: docking.ComponentProvider, panel: ghidra.features.base.codecompare.panel.CodeComparisonPanel, component: java.awt.Component):
        """
        Constructor
        @param provider the ComponentProvider containing the code comparison panel
        @param panel the CodeComparisonPanel that generated this context
        @param component the focusable component for associated with the comparison panel
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getCodeComparisonPanel(self) -> ghidra.features.base.codecompare.panel.CodeComparisonPanel: ...

    def getComponentProvider(self) -> docking.ComponentProvider: ...

    def getContextObject(self) -> object: ...

    def getEventClickModifiers(self) -> int: ...

    def getMouseEvent(self) -> java.awt.event.MouseEvent: ...

    def getSourceComponent(self) -> java.awt.Component: ...

    def getSourceFunction(self) -> ghidra.program.model.listing.Function:
        """
        Returns the function that is the source of the info being applied. This will be whichever
         side of the function diff window that isn't active.
        @return the function to get information from
        """
        ...

    def getSourceObject(self) -> object: ...

    def getTargetFunction(self) -> ghidra.program.model.listing.Function:
        """
        Returns the function that is the target of the info being applied. This will be whichever
         side of the function diff window that is active.
        @return the function to apply information to
        """
        ...

    def hasAnyEventClickModifiers(self, modifiersMask: int) -> bool: ...

    def hashCode(self) -> int: ...

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
    def sourceFunction(self) -> ghidra.program.model.listing.Function: ...

    @property
    def targetFunction(self) -> ghidra.program.model.listing.Function: ...