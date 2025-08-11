import pytest

from scripts.sbir_crew import parse_overall_score, split_multi_idea_blocks


def test_parse_overall_score_int_and_decimal():
    assert parse_overall_score("Overall Score: 8/10") == 8.0
    assert parse_overall_score("Some text... Overall Score: 8.6/10 ...end") == 8.6
    assert parse_overall_score("No score present") is None


def test_split_multi_idea_blocks_basic():
    draft = (
        """### IDEA: Alpha
Intro text
## Volume 1
Alpha V1 content
## Volume 2
Alpha V2 content
### IDEA: Beta
## Volume 1
Beta V1 content
"""
    )
    blocks = split_multi_idea_blocks(draft)

    assert isinstance(blocks, list)
    assert len(blocks) == 2

    # Titles
    assert blocks[0]["title"] == "Alpha"
    assert blocks[1]["title"] == "Beta"

    # Volumes lists
    assert all(isinstance(b.get("volumes"), list) for b in blocks)
    assert all(v.startswith("## Volume ") for v in blocks[0]["volumes"])  # basic shape

    # Alpha has two volumes, Beta has one
    assert len(blocks[0]["volumes"]) == 2
    assert len(blocks[1]["volumes"]) == 1
