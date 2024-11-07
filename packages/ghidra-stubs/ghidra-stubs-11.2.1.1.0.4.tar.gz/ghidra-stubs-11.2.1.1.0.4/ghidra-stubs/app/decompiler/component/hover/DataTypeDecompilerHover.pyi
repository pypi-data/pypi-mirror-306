from typing import overload
import docking.widgets.fieldpanel.field
import docking.widgets.fieldpanel.support
import ghidra.app.decompiler
import ghidra.app.decompiler.component.hover
import ghidra.app.plugin.core.hover
import ghidra.framework.options
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.program.util
import java.lang
import javax.swing


class DataTypeDecompilerHover(ghidra.app.plugin.core.hover.AbstractConfigurableHover, ghidra.app.decompiler.component.hover.DecompilerHoverService):








    def componentHidden(self) -> None: ...

    def componentShown(self) -> None: ...

    def dispose(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getFieldDataType(field: ghidra.app.decompiler.ClangFieldToken) -> ghidra.program.model.data.DataType: ...

    def getHoverComponent(self, program: ghidra.program.model.listing.Program, programLocation: ghidra.program.util.ProgramLocation, fieldLocation: docking.widgets.fieldpanel.support.FieldLocation, field: docking.widgets.fieldpanel.field.Field) -> javax.swing.JComponent: ...

    def getPriority(self) -> int: ...

    def hashCode(self) -> int: ...

    def hoverModeSelected(self) -> bool: ...

    def initializeOptions(self) -> None: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def optionsChanged(self, __a0: ghidra.framework.options.ToolOptions, __a1: unicode, __a2: object, __a3: object) -> None: ...

    def scroll(self, __a0: int) -> None: ...

    def setOptions(self, __a0: ghidra.framework.options.Options, __a1: unicode) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

