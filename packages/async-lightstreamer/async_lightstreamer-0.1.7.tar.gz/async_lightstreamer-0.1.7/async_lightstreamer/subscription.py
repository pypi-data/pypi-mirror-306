import enum
from typing import Callable, Dict, List


class Mode(str, enum.Enum):
    RAW = "RAW"
    MERGE = "MERGE"


class LightstreamerSubscription:
    """Represents a Subscription to be submitted to a Lightstreamer Server."""

    def __init__(
        self,
        mode: Mode,
        items: List[str],
        fields: List[str],
        adapter: str = "",
    ):
        self.item_names = items
        self._items_map: Dict[int, Dict] = {}
        self.field_names = fields
        self.adapter = adapter
        self.mode = mode
        self.snapshot = "true"
        self._listeners: List[Callable] = []

    @staticmethod
    def _decode(value, last):
        """Decode the field value according to Lightstreamer Text Protocol specifications."""

        if value == "$":
            return ""
        elif value == "#":
            return None
        elif not value:
            return last
        elif value[0] in "#$":
            value = value[1:]

        return value

    def addlistener(self, listener: Callable) -> "LightstreamerSubscription":
        self._listeners.append(listener)
        return self

    async def notifyupdate(self, item_line: str) -> None:
        """Invoked by LSClient each time Lightstreamer Server pushes a new item event."""

        # tokenize the item line as sent by Lightstreamer
        toks = item_line.rstrip("\r\n").split("|")
        undecoded_item = dict(list(zip(self.field_names, toks[1:], strict=True)))

        # retrieve the previous item stored into the map, if present, otherwise create a new empty dict
        item_pos = int(toks[0])
        curr_item = self._items_map.get(item_pos, {})
        # update the map with new values, merging with the previous ones if any
        self._items_map[item_pos] = {
            k: self._decode(v, curr_item.get(k))
            for k, v in list(undecoded_item.items())
        }
        # make an item info as a new event to be passed to listeners
        item_info = {
            "pos": item_pos,
            "name": self.item_names[item_pos - 1],
            "values": self._items_map[item_pos],
        }

        # update each registered listener with new event
        for on_item_update in self._listeners:
            await on_item_update(item_info)
