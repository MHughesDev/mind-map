from vault_pipeline.chunking import chunk_text, normalize_text


def test_normalize_text_collapses_whitespace() -> None:
    raw = "  a\tb\n\nc  "
    assert normalize_text(raw) == "a b c"


def test_chunk_text_overlap_and_order() -> None:
    text = " ".join(f"token{i}" for i in range(120))
    chunks = list(chunk_text(text, chunk_size=80, overlap=20))
    assert len(chunks) > 1
    assert chunks[0].index == 0
    assert all(chunks[i].index == i for i in range(len(chunks)))
    assert all(chunks[i].start_char < chunks[i + 1].end_char for i in range(len(chunks) - 1))

