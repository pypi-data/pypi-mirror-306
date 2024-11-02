from pathlib import Path
from uuid import uuid4

import pytest

from megaparse.core.parser.llama import LlamaParser
from megaparse.core.parser.megaparse_vision import MegaParseVision
from megaparse.core.megaparse import MegaParse

from langchain_core.language_models import FakeListChatModel


@pytest.mark.asyncio
async def test_megaparse_xls_processor():
    p = Path("./tests/xls/file_example_XLS_50.xls")
    processor = MegaParse()
    result = await processor.aload(file_path=p)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_megaparse_xlsx_processor():
    p = Path("./tests/xls/file_example_XLSX_50.xlsx")
    processor = MegaParse()
    result = await processor.aload(file_path=p)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_megaparse_xls_processor_fail():
    p = Path("./tests/xls/file_example_XLS_50.xls")
    parser = LlamaParser(api_key=str(uuid4()))
    processor = MegaParse(parser=parser)
    with pytest.raises(ValueError):
        await processor.aload(file_path=p)

    parser = MegaParseVision(model=FakeListChatModel(responses=["good"]))  # type: ignore
    processor = MegaParse(parser=parser)
    with pytest.raises(ValueError):
        await processor.aload(file_path=p)
