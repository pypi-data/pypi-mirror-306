# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CalTableFlatBuffers

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


class KeyValue:
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAs(cls, buf, offset=0):  # noqa: N802
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = KeyValue()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsKeyValue(cls, buf, offset=0):  # noqa: N802
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)

    # KeyValue
    def Init(self, buf, pos):  # noqa: N802
        self._tab = flatbuffers.table.Table(buf, pos)

    # KeyValue
    def Key(self):  # noqa: N802
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # KeyValue
    def Value(self):  # noqa: N802
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None


def Start(builder):  # noqa: N802
    builder.StartObject(2)


def KeyValueStart(builder):  # noqa: N802
    """This method is deprecated. Please switch to Start."""
    return Start(builder)


def AddKey(builder, key):  # noqa: N802
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(key), 0)


def KeyValueAddKey(builder, key):  # noqa: N802
    """This method is deprecated. Please switch to AddKey."""
    return AddKey(builder, key)


def AddValue(builder, value):  # noqa: N802
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(value), 0)


def KeyValueAddValue(builder, value):  # noqa: N802
    """This method is deprecated. Please switch to AddValue."""
    return AddValue(builder, value)


def End(builder):  # noqa: N802
    return builder.EndObject()


def KeyValueEnd(builder):  # noqa: N802
    """This method is deprecated. Please switch to End."""
    return End(builder)
