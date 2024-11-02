# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbs

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class RuntimeOptimizations(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = RuntimeOptimizations()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsRuntimeOptimizations(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    @classmethod
    def RuntimeOptimizationsBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x4F\x52\x54\x4D", size_prefixed=size_prefixed)

    # RuntimeOptimizations
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # mapping from optimizer name to [RuntimeOptimizationRecord]
    # RuntimeOptimizations
    def Records(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from ort_flatbuffers_py.fbs.RuntimeOptimizationRecordContainerEntry import RuntimeOptimizationRecordContainerEntry
            obj = RuntimeOptimizationRecordContainerEntry()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # RuntimeOptimizations
    def RecordsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # RuntimeOptimizations
    def RecordsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

def RuntimeOptimizationsStart(builder):
    builder.StartObject(1)

def Start(builder):
    RuntimeOptimizationsStart(builder)

def RuntimeOptimizationsAddRecords(builder, records):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(records), 0)

def AddRecords(builder, records):
    RuntimeOptimizationsAddRecords(builder, records)

def RuntimeOptimizationsStartRecordsVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartRecordsVector(builder, numElems: int) -> int:
    return RuntimeOptimizationsStartRecordsVector(builder, numElems)

def RuntimeOptimizationsEnd(builder):
    return builder.EndObject()

def End(builder):
    return RuntimeOptimizationsEnd(builder)
