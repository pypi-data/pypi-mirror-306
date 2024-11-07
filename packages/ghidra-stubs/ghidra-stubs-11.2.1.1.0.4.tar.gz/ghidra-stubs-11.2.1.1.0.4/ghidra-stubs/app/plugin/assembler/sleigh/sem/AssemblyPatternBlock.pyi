from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.expr
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.processors.sleigh
import ghidra.app.plugin.processors.sleigh.expression
import ghidra.app.plugin.processors.sleigh.pattern
import ghidra.program.model.lang
import java.lang


class AssemblyPatternBlock(object, java.lang.Comparable):
    """
    The analog of PatternBlock, designed for use by the assembler
 
 
     It is suitable for the assembler because it is represented byte-by-byte, and it offers a number
     of useful conversions and operations.
 
 
     TODO: A lot of this could probably be factored into the PatternBlock class, but it was
     best to experiment in another class altogether to avoid breaking things.
    """









    def combine(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Combine this pattern block with another given block
 
         <p>
         Two blocks can be combined in their corresponding defined bits agree. When blocks are
         combined, their bytes are aligned according to their shifts, and the defined bits are taken
         from either block. If neither block defines a bit (i.e., the mask bit at that position is 0
         for both input blocks, then the output has an undefined bit in the corresponding position. If
         both blocks define the bit, but they have opposite values, then the result is an error.
        @param that the other block
        @return the new combined block, or null if the blocks disagree for any bit
        """
        ...

    @overload
    def compareTo(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def copy(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Duplicate this pattern block
        @return the duplicate
        """
        ...

    def countPossibleVals(self) -> int: ...

    def equals(self, obj: object) -> bool: ...

    def fillMask(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Fill all unknown bits with 0 bits
        @return the result
        """
        ...

    @staticmethod
    def fromBytes(offset: int, vals: List[int]) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Get a pattern block with the given (fully-included) values at the given offset
        @param offset the offset (0-up, left-to-right)
        @param vals the values
        @return a pattern block (having a full mask)
        """
        ...

    @staticmethod
    def fromContextField(cf: ghidra.app.plugin.processors.sleigh.expression.ContextField, val: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Encode the given masked long into a pattern block as specified by a given context field
        @param cf the context field specifying the location of the value to encode
        @param val the value to encode
        @return the pattern block with the encoded value
        """
        ...

    @staticmethod
    def fromLength(length: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Allocate a fully-undefined pattern block of the given length
        @param length the length in bytes
        @return the block of all unknown bits
        """
        ...

    @staticmethod
    def fromPattern(pat: ghidra.app.plugin.processors.sleigh.pattern.DisjointPattern, minLen: int, context: bool) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Convert a block from a disjoint pattern into an assembly pattern block
        @param pat the pattern to convert
        @param minLen the minimum byte length of the block
        @param context true to select the context block, false to select the instruction block
        @return the converted pattern block
        """
        ...

    @staticmethod
    def fromRegisterValue(rv: ghidra.program.model.lang.RegisterValue) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Convert a register value into a pattern block
 
         <p>
         This is used primarily to compute default context register values, and pass them into an
         assembler.
        @param rv the register value
        @return the pattern block
        """
        ...

    @staticmethod
    def fromString(str: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Convert a string representation to a pattern block
        @see NumericUtilities#convertHexStringToMaskedValue(AtomicLong, AtomicLong, String, int, int,
              String)
        @param str the string to convert
        @return the resulting pattern block
        """
        ...

    @staticmethod
    def fromTokenField(tf: ghidra.app.plugin.processors.sleigh.expression.TokenField, val: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Encode the given masked long into a pattern block as specified by a given token field
        @param tf the token field specifying the location of the value to encode
        @param val the value to encode
        @return the pattern block with the encoded value
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getMask(self) -> List[int]:
        """
        Get the mask array
 
         <p>
         Modifications to the returned array will affect the pattern block. It is <em>not</em> a copy.
         Furthermore, the offset is not incorporated. See {@link #getOffset()}. For a copy of the
         array with offset applied, use {@link #getMaskAll()}.
        @return the array
        """
        ...

    def getMaskAll(self) -> List[int]:
        """
        Get an array representing the full mask of the pattern
 
         <p>
         This is a copy of the {@link #getMask()} array, but with 0s prepended to apply the offset.
         See {@link #getOffset()}.
        @return the array
        """
        ...

    def getMaskedValue(self, unmasked: List[int]) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Mask the given {@code unmasked} value with the mask contained in this pattern block.
 
         <p>
         The returned {@link AssemblyPatternBlock} has an identical mask as {@code this} but with a 
         value taken from the given {@code unmasked}.
        @param unmasked the value to be masked into the result
        @return a combination of the given unmasked value and this mask
        """
        ...

    def getOffset(self) -> int:
        """
        Get the number of undefined bytes preceding the mask and values arrays
        @return the offset
        """
        ...

    def getSpecificity(self) -> int:
        """
        Counts the total number of known bits in the pattern
 
         <p>
         At a slightly lower level, counts the number of 1-bits in the mask.
        @return the count
        """
        ...

    def getVals(self) -> List[int]:
        """
        Get the values array
 
         <p>
         Modifications to the returned array will affect the pattern block. It is <em>not</em> a copy.
         Furthermore, the offset is not incorporated. See {@link #getOffset()}. For a copy of the
         array with offset applied, use {@link #getValsAll()}.
        @return the array
        """
        ...

    def getValsAll(self) -> List[int]:
        """
        Get an array representing the full value of the pattern
 
         <p>
         This is a copy of the {@link #getVals()} array, but with 0s prepended to apply the offset.
         See {@link #getOffset()}.
        @return the array
        """
        ...

    def hashCode(self) -> int: ...

    def isFullMask(self) -> bool:
        """
        Check if there are any unknown bits
        @return true if no unknown bits are present, false otherwise
        """
        ...

    def isZero(self) -> bool:
        """
        Check if all bits are 0 bits
        @return true if all are 0, false otherwise
        """
        ...

    def length(self) -> int:
        """
        Get the length (plus the offset) of this pattern block
        @return the total length
        """
        ...

    @overload
    def maskOut(self, other: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Set all bits that are known (1 in mask) in {@code other} to unknown.
 
         <p>
         Other must have the same or shorter length than this.
        @param other the other pattern block whose mask bits are examined
        @return a copy of this pattern with mask bits set to unknown
        """
        ...

    @overload
    def maskOut(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Set all bits read by a given context operation to unknown
 
         <p>
         This is used during resolution to remove a context requirement passed upward by a child. When
         a parent constructor writes the required value to the context register, that requirement need
         not be passed further upward, since the write satisfies the requirement.
        @param cop the context operation
        @return the result
        """
        ...

    @staticmethod
    def nop() -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Get an empty pattern block
        @return the pattern block
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def possibleVals(self) -> List[java.lang.Iterable]:
        """
        Get an iterable over all the possible fillings of the value, given a partial mask
 
         <p>
         This is meant to be used idiomatically, as in an enhanced for loop:
 
         <pre>
         for (byte[] val : pattern.possibleVals()) {
         	System.out.println(format(val));
         }
         </pre>
 
         <p>
         <b>NOTE:</b> A single byte array is instantiated with the call to
         {@link Iterable#iterator()}. Each call to {@link Iterator#next()} modifies the one byte array
         and returns it. As such, if you intend to preserve the value in the array for later use, you
         <em>must</em> make a copy.
        @return the iterable.
        """
        ...

    def readBytes(self, start: int, len: int) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong:
        """
        Decode {@code len} bytes (values and mask) in big-endian format, beginning at {@code start}
        @param start the first byte to decode
        @param len the number of bytes to decode
        @return the decoded masked long
        """
        ...

    def readContextOp(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong:
        """
        Read the input of a context operation from this pattern block
        @param cop the context operation
        @return the decoded input, as a masked value
        """
        ...

    def readMaskBytes(self, start: int, len: int) -> long:
        """
        Decode {@code len} mask bytes in big-endian format, beginning at {@code start}
        @param start the first byte to decode
        @param len the number of bytes to decode
        @return the decoded long
        """
        ...

    def readValBytes(self, start: int, len: int) -> long:
        """
        Decode {@code len} value bytes in big-endian format, beginning at {@code start}
        @param start the first byte to decode
        @param len the number of bytes to decode
        @return the decoded long
        """
        ...

    def shift(self, amt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Shift, i.e., increase the offset of, this pattern block
        @param amt the amount to shift right
        @return the shifted pattern block
        """
        ...

    def toBigInteger(self, n: int) -> long:
        """
        Decode the values array into a {@link BigInteger} of length {@code n} bytes
 
         <p>
         The array is either truncated or zero-extended <em>on the right</em> to match the requested
         number of bytes, then decoded in big-endian format as an unsigned value.
        @param n the number of bytes (left-to-right) to decode
        @return the decoded big integer
        """
        ...

    def toString(self) -> unicode: ...

    def trim(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Remove all unknown bits from both left and right
        @return new value without any left or right unknown bits (but may have unknown bits in the
                 middle)
        """
        ...

    def truncate(self, amt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Truncate (unshift) this pattern block by removing bytes from the left
        @param amt the amount to truncate or shift left
        @return the truncated pattern block
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def writeContextOp(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp, val: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Encode the given value into a copy of this pattern block as specified by a context operation
 
         <p>
         <b>NOTE:</b> this method is given as a special operation, instead of a conversion factory
         method, because this is a write operation, not a combine operation. As such, the bits
         (including undefined bits) replace the bits in the existing pattern block. Were this a
         conversion method, we would lose the distinction between unknown bits being written, and bits
         whose values are simply not included in the write.
        @param cop the context operation specifying the location of the value to encode
        @param val the value to encode
        @return the new copy with the encoded value
        """
        ...

    @property
    def fullMask(self) -> bool: ...

    @property
    def mask(self) -> List[int]: ...

    @property
    def maskAll(self) -> List[int]: ...

    @property
    def offset(self) -> int: ...

    @property
    def specificity(self) -> int: ...

    @property
    def vals(self) -> List[int]: ...

    @property
    def valsAll(self) -> List[int]: ...

    @property
    def zero(self) -> bool: ...