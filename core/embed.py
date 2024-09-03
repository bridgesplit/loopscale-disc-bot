from __future__ import annotations

from typing import Optional, Union

from discord import Colour, Embed as OriginalEmbed
from typing_extensions import Self
from settings_file import POWERED_BY_TEXT, POWERED_BY_ICON

__all__ = (
    "Embed",
)

class Embed(OriginalEmbed):
    def __init__(self, color: Optional[Union[int, Colour]] = Colour.blurple(), **kwargs):
        super().__init__(color=color, **kwargs)
    
    def credits(self) -> Self:
        super().set_footer(text=POWERED_BY_TEXT, icon_url=POWERED_BY_ICON)
        return self