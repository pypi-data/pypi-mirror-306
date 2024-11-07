from typing import Iterator
from typing import List
from typing import overload
import ghidra.program.model.address
import ghidra.program.model.pcode
import java.lang


class PcodeOpAST(ghidra.program.model.pcode.PcodeOp):
    """
    Some extra things attached to PcodeOp for ease of walking the syntax tree
    """





    @overload
    def __init__(self, sq: ghidra.program.model.pcode.SequenceNumber, op: int, numinputs: int): ...

    @overload
    def __init__(self, a: ghidra.program.model.address.Address, uq: int, op: int, numinputs: int): ...



    @staticmethod
    def decode(decoder: ghidra.program.model.pcode.Decoder, pfact: ghidra.program.model.pcode.PcodeFactory) -> ghidra.program.model.pcode.PcodeOp:
        """
        Decode p-code from a stream
        @param decoder is the stream decoder
        @param pfact factory used to create p-code correctly
        @return new PcodeOp
        @throws DecoderException if encodings are invalid
        """
        ...

    def encodeRaw(self, encoder: ghidra.program.model.pcode.Encoder, addrFactory: ghidra.program.model.address.AddressFactory) -> None:
        """
        Encode just the opcode and input/output Varnode data for this PcodeOp to a stream
         as an {@code <op>} element
        @param encoder is the stream encoder
        @param addrFactory is a factory for looking up encoded address spaces
        @throws IOException for errors in the underlying stream
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getBasicIter(self) -> Iterator[ghidra.program.model.pcode.PcodeOp]: ...

    def getClass(self) -> java.lang.Class: ...

    def getInput(self, i: int) -> ghidra.program.model.pcode.Varnode:
        """
        @param i the i'th input varnode
        @return the i'th input varnode
        """
        ...

    def getInputs(self) -> List[ghidra.program.model.pcode.Varnode]:
        """
        @return get input varnodes
        """
        ...

    def getInsertIter(self) -> Iterator[object]: ...

    @overload
    def getMnemonic(self) -> unicode:
        """
        @return get the string representation for the pcode operation
        """
        ...

    @overload
    @staticmethod
    def getMnemonic(op: int) -> unicode:
        """
        Get string representation for p-code operation
        @param op operation code
        @return String representation of p-code operation
        """
        ...

    def getNumInputs(self) -> int:
        """
        @return number of input varnodes
        """
        ...

    @overload
    def getOpcode(self) -> int:
        """
        @return pcode operation code
        """
        ...

    @overload
    @staticmethod
    def getOpcode(s: unicode) -> int:
        """
        Get the p-code op code for the given mnemonic string.
        @param s is the mnemonic string
        @return the op code
        @throws UnknownInstructionException if there is no matching mnemonic
        """
        ...

    def getOutput(self) -> ghidra.program.model.pcode.Varnode:
        """
        @return get output varnodes
        """
        ...

    def getParent(self) -> ghidra.program.model.pcode.PcodeBlockBasic: ...

    def getSeqnum(self) -> ghidra.program.model.pcode.SequenceNumber:
        """
        @return the sequence number this pcode is within some number of pcode
        """
        ...

    def getSlot(self, vn: ghidra.program.model.pcode.Varnode) -> int:
        """
        Assuming vn is an input to this op, return its input slot number
        @param vn is the input varnode
        @return the slot number
        """
        ...

    def hashCode(self) -> int: ...

    def insertInput(self, vn: ghidra.program.model.pcode.Varnode, slot: int) -> None:
        """
        Insert an input varnode at the given index of input varnodes
        @param vn varnode to insert
        @param slot insert index in input varnode list
        """
        ...

    def isAssignment(self) -> bool:
        """
        @return true if the pcode assigns a value to an output varnode
        """
        ...

    @overload
    def isCommutative(self) -> bool:
        """
        Return true if the PcodeOp is commutative.
         If true, the operation has exactly two inputs that can be switched without affecting the output.
        @return true if the operation is commutative
        """
        ...

    @overload
    @staticmethod
    def isCommutative(opcode: int) -> bool:
        """
        Return true if the given opcode represents a commutative operation.
         If true, the operation has exactly two inputs that can be switched without affecting the output.
        @param opcode is the opcode
        @return true if the operation is commutative
        """
        ...

    def isDead(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def removeInput(self, slot: int) -> None:
        """
        Remove a varnode at the given slot from the list of input varnodes
        @param slot index of input varnode to remove
        """
        ...

    def setBasicIter(self, iter: Iterator[ghidra.program.model.pcode.PcodeOp]) -> None:
        """
        Set the iterator being used to iterate the pcode within a basic block.
        @param iter
        """
        ...

    def setInput(self, vn: ghidra.program.model.pcode.Varnode, slot: int) -> None:
        """
        Set/Replace an input varnode at the given slot.
        @param vn varnode to replace
        @param slot index of input varnode to be replaced
        """
        ...

    def setInsertIter(self, iter: Iterator[object]) -> None:
        """
        Set the iterator being used to iterate the pcode to insert within a block.
        @param iter
        """
        ...

    def setOpcode(self, o: int) -> None:
        """
        Set the pcode operation code
        @param o pcode operation code
        """
        ...

    def setOrder(self, ord: int) -> None:
        """
        Set relative position information of PcodeOps within
         a basic block, may change as basic block is edited.
        @param ord relative position of pcode op in basic block
        """
        ...

    def setOutput(self, vn: ghidra.program.model.pcode.Varnode) -> None:
        """
        Set the output varnode for the pcode operation.
        @param vn new output varnode
        """
        ...

    def setParent(self, par: ghidra.program.model.pcode.PcodeBlockBasic) -> None:
        """
        Set the parent basic block this pcode is contained within.
        @param par parent basic block.
        """
        ...

    def setTime(self, t: int) -> None:
        """
        Set a unique number for pcode ops that are attached to the same address
        @param t unique id
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
    def basicIter(self) -> java.util.Iterator: ...

    @basicIter.setter
    def basicIter(self, value: java.util.Iterator) -> None: ...

    @property
    def dead(self) -> bool: ...

    @property
    def insertIter(self) -> java.util.Iterator: ...

    @insertIter.setter
    def insertIter(self, value: java.util.Iterator) -> None: ...

    @property
    def parent(self) -> ghidra.program.model.pcode.PcodeBlockBasic: ...

    @parent.setter
    def parent(self, value: ghidra.program.model.pcode.PcodeBlockBasic) -> None: ...