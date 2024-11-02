import uuid
from metamenth.structure.cover import Cover
from typing import List
from typing import Dict
from metamenth.utils import StructureSearch


class Envelope:
    """
    The envelope of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self):
        self._UID = str(uuid.uuid4())
        self._covers: List['Cover'] = []

    @property
    def UID(self) -> str:
        return self._UID

    def add_cover(self, cover: Cover):
        """
        Adds a cover to a building
        :param cover: the building cover e.g., wall, roof
        :return:
        """
        if cover is None:
            raise ValueError("cover must be of type Cover")
        self._covers.append(cover)

    def get_cover_by_uid(self, uid: str) -> Cover:
        """
        Retrieves a cover given the uid
        :param uid: the uid of the cover
        :return:
        """
        return StructureSearch.search_by_id(self._covers, uid)

    def get_covers(self, search_term: Dict = None) -> List[Cover]:
        """
        Retrieves covers given the attributes and their values
        :param search_term: the uid of the floor
        :return:
        """
        return StructureSearch.search(self._covers, search_term)

    def __str__(self):
        cover_details = "\n".join(str(cover) for cover in self._covers)
        return (
            f"Cover("
            f"UID: {self.UID}, "
            f"Layers:\n{cover_details})"
        )
