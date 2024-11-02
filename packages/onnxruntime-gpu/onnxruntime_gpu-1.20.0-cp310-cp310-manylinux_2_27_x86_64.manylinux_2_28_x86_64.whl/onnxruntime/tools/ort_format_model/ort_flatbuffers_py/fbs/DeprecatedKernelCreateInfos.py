# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbs

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# deprecated: no longer using kernel def hashes
class DeprecatedKernelCreateInfos(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DeprecatedKernelCreateInfos()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsDeprecatedKernelCreateInfos(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    @classmethod
    def DeprecatedKernelCreateInfosBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x4F\x52\x54\x4D", size_prefixed=size_prefixed)

    # DeprecatedKernelCreateInfos
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DeprecatedKernelCreateInfos
    def NodeIndices(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # DeprecatedKernelCreateInfos
    def NodeIndicesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint32Flags, o)
        return 0

    # DeprecatedKernelCreateInfos
    def NodeIndicesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # DeprecatedKernelCreateInfos
    def NodeIndicesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # DeprecatedKernelCreateInfos
    def KernelDefHashes(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 8))
        return 0

    # DeprecatedKernelCreateInfos
    def KernelDefHashesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint64Flags, o)
        return 0

    # DeprecatedKernelCreateInfos
    def KernelDefHashesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # DeprecatedKernelCreateInfos
    def KernelDefHashesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def DeprecatedKernelCreateInfosStart(builder):
    builder.StartObject(2)

def Start(builder):
    DeprecatedKernelCreateInfosStart(builder)

def DeprecatedKernelCreateInfosAddNodeIndices(builder, nodeIndices):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(nodeIndices), 0)

def AddNodeIndices(builder, nodeIndices):
    DeprecatedKernelCreateInfosAddNodeIndices(builder, nodeIndices)

def DeprecatedKernelCreateInfosStartNodeIndicesVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartNodeIndicesVector(builder, numElems: int) -> int:
    return DeprecatedKernelCreateInfosStartNodeIndicesVector(builder, numElems)

def DeprecatedKernelCreateInfosAddKernelDefHashes(builder, kernelDefHashes):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(kernelDefHashes), 0)

def AddKernelDefHashes(builder, kernelDefHashes):
    DeprecatedKernelCreateInfosAddKernelDefHashes(builder, kernelDefHashes)

def DeprecatedKernelCreateInfosStartKernelDefHashesVector(builder, numElems):
    return builder.StartVector(8, numElems, 8)

def StartKernelDefHashesVector(builder, numElems: int) -> int:
    return DeprecatedKernelCreateInfosStartKernelDefHashesVector(builder, numElems)

def DeprecatedKernelCreateInfosEnd(builder):
    return builder.EndObject()

def End(builder):
    return DeprecatedKernelCreateInfosEnd(builder)
