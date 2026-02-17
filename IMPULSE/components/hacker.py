from typing import Optional, TYPE_CHECKING


from IMPULSE import color
from IMPULSE.components.base_component import BaseComponent

if TYPE_CHECKING:
    from IMPULSE.entity import Actor


class Hacker(BaseComponent):
    def __init__(self, virus_list):
        self.virus_list=virus_list

    def get_virus_list(self):
        return self.virus_list

    def add_virus(self, virus):
        self.virus_list.append(virus)