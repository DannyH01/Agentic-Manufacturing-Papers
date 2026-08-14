from scraper.deduplicate import base_arxiv_id, deduplicate_papers, merge_records


def test_base_arxiv_id_removes_version():
    assert base_arxiv_id("2608.12345v3") == "2608.12345"
    assert base_arxiv_id("https://arxiv.org/abs/hep-th/9901001v2") == "hep-th/9901001"


def test_newest_version_wins_and_only_one_record_remains():
    result = deduplicate_papers([
        {"arxiv_id": "2608.12345v1", "title": "Old"},
        {"arxiv_id": "2608.12345v2", "title": "Revised"},
    ])
    assert len(result) == 1
    assert result[0]["arxiv_id"] == "2608.12345"
    assert result[0]["version"] == "v2"
    assert result[0]["title"] == "Revised"


def test_merge_counts_revision_without_adding_a_row():
    merged, new_count, updated_count = merge_records(
        [{"arxiv_id": "2608.12345", "version": "v1", "first_seen": "earlier"}],
        [{"arxiv_id": "2608.12345", "version": "v2", "first_seen": "now"}],
    )
    assert len(merged) == 1
    assert new_count == 0
    assert updated_count == 1
    assert merged[0]["version"] == "v2"
    assert merged[0]["first_seen"] == "earlier"
