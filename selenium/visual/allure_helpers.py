"""Small Allure helpers for KT08 (PNG attach + metadata)."""

from __future__ import annotations

from pathlib import Path

import allure
from allure_commons.types import AttachmentType


def attach_png(path: Path | str, name: str) -> None:
    path = Path(path)
    if not path.is_file():
        return
    allure.attach.file(
        str(path),
        name=name,
        attachment_type=AttachmentType.PNG,
    )


def attach_text(body: str, name: str) -> None:
    allure.attach(body, name=name, attachment_type=AttachmentType.TEXT)
