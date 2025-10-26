import pytest

from app.chat.utils import build_title_for_document
from app.schema import (
    Document,
    DocumentMetadataKeysEnum,
    SecDocumentMetadata,
    SecDocumentTypeEnum,
)


def test_build_title_for_document_without_metadata():
    document = Document(url="https://example.com", metadata_map=None)

    assert build_title_for_document(document) == "No Title Document"


def test_build_title_for_document_with_sec_metadata():
    metadata = SecDocumentMetadata(
        company_name="Example Corp",
        company_ticker="EX",
        doc_type=SecDocumentTypeEnum.TEN_K,
        year=2024,
    )
    document = Document(
        url="https://example.com",
        metadata_map={DocumentMetadataKeysEnum.SEC_DOCUMENT: metadata.model_dump()},
    )

    assert (
        build_title_for_document(document)
        == "Example Corp (EX) 10-K (2024)"
    )


def test_build_description_for_document_without_metadata():
    pytest.importorskip("llama_index")
    from app.chat.engine import build_description_for_document

    document = Document(url="https://example.com", metadata_map=None)

    assert (
        build_description_for_document(document)
        == "A document containing useful information that the user pre-selected to discuss with the assistant."
    )
