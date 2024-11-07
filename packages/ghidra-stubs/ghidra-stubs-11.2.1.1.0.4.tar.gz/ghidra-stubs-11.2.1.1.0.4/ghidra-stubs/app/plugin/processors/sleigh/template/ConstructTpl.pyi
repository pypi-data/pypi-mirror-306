from typing import List
from typing import overload
import ghidra.app.plugin.processors.sleigh.template
import ghidra.program.model.pcode
import java.lang


class ConstructTpl(object):
    """
    A constructor template, representing the semantic action of a SLEIGH constructor, without
     its final context.  The constructor template is made up of a list of p-code op templates,
     which are in turn made up of varnode templates.
     This is one step removed from the final array of PcodeOp objects, but:
       - Constants may still need to incorporate context dependent address resolution and relative offsets.
       - Certain p-code operations may still need expansion to include a dynamic LOAD or STORE operation.
       - The list may hold "build" directives for sub-constructor templates.
       - The list may still hold "label" information for the final resolution of relative jump offsets.
 
     The final PcodeOps are produced by handing this to the build() method of PcodeEmit which has
     the InstructionContext necessary for final resolution.
    """





    @overload
    def __init__(self):
        """
        Constructor for use with decode
        """
        ...

    @overload
    def __init__(self, opvec: List[ghidra.app.plugin.processors.sleigh.template.OpTpl]):
        """
        Manually build a constructor template. This is useful for building constructor templates
         outside of the normal SLEIGH pipeline, as for an internally created InjectPayload.
        @param opvec is the list of p-code op templates making up the constructor
        """
        ...

    @overload
    def __init__(self, opvec: List[ghidra.app.plugin.processors.sleigh.template.OpTpl], res: ghidra.app.plugin.processors.sleigh.template.HandleTpl, nmLabels: int):
        """
        Manually build a constructor template from pieces.  This is used to translate from the
         internal SLEIGH compiler pcodeCPort.semantics.ConstructTpl
        @param opvec is the list of p-code op templates making up the constructor
        @param res is the result handle template for the constructor
        @param nmLabels is the number of labels int the template
        """
        ...



    def decode(self, decoder: ghidra.program.model.pcode.Decoder) -> int:
        """
        Decode this template from a {@code <construct_tpl>} tag in the stream.
        @param decoder is the stream
        @return the constructor section id described by the tag
        @throws DecoderException for errors in the encoding
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getNumLabels(self) -> int:
        """
        @return the number of labels needing resolution in this template
        """
        ...

    def getOpVec(self) -> List[ghidra.app.plugin.processors.sleigh.template.OpTpl]:
        """
        @return the list of p-code op templates making up this constructor template
        """
        ...

    def getResult(self) -> ghidra.app.plugin.processors.sleigh.template.HandleTpl:
        """
        @return the (possibly dynamic) location of the final semantic value produced by this constructor
        """
        ...

    def hashCode(self) -> int: ...

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
    def numLabels(self) -> int: ...

    @property
    def opVec(self) -> List[ghidra.app.plugin.processors.sleigh.template.OpTpl]: ...

    @property
    def result(self) -> ghidra.app.plugin.processors.sleigh.template.HandleTpl: ...