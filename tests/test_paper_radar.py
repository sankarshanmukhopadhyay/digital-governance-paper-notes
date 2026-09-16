import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("paper_radar", ROOT / "scripts" / "paper_radar.py")
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)

CFG = {
    "candidate_threshold": 9,
    "judgment_threshold": 7,
    "themes": [{"name": "ai-governance", "anchors": ["AI", "artificial intelligence", "agentic"]}],
    "governance_signals": ["governance", "authority", "redress", "interoperability", "accountability"],
    "material_governance_signals": ["authority", "redress", "interoperability", "accountability"],
    "candidate_title_signals": ["governance", "authority", "redress", "accountability"],
    "exclusion_signals": ["protein folding"],
    "source_weights": {"arxiv": 1, "crossref": 1, "openalex": 1},
}


class PaperRadarTests(unittest.TestCase):
    def test_canonical_doi_key_normalises_url(self):
        self.assertEqual(radar.canonical_key({"doi": "https://doi.org/10.1000/XYZ"}), "doi:10 1000 xyz")

    def test_existing_paper_never_returns_as_fresh_candidate(self):
        item = {"source_system": "arxiv", "title": "Governance and Authority in AI Systems", "abstract": "governance authority redress interoperability accountability", "arxiv_id": "2609.12345"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", {"arxiv:2609.12345"}, [])
        self.assertEqual(scored["state"], "represented")
        self.assertTrue(scored["already_represented"])

    def test_issue_reference_extraction_captures_arxiv(self):
        keys, _ = radar.extract_refs("Paper: https://arxiv.org/abs/2609.17416")
        self.assertIn("arxiv:2609.17416", keys)

    def test_score_is_diagnostic_not_admission(self):
        item = {"source_system": "openalex", "title": "AI Governance Authority and Redress", "abstract": "interoperability governance authority redress accountability"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", set(), [])
        self.assertEqual(scored["state"], "candidate")
        self.assertNotIn("queue", scored)

    def test_high_score_without_material_governance_is_not_candidate(self):
        item = {"source_system": "openalex", "title": "AI Governance Systems", "abstract": "governance governance governance"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", set(), [])
        self.assertNotEqual(scored["state"], "candidate")

    def test_missing_theme_anchor_forces_deferred(self):
        item = {"source_system": "openalex", "title": "Fiscal Governance and Authority", "abstract": "governance authority redress interoperability accountability"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", set(), [])
        self.assertEqual(scored["state"], "deferred")

    def test_exclusion_signal_reduces_score(self):
        item = {"source_system": "crossref", "title": "AI Governance for Protein Folding", "abstract": "governance authority redress interoperability protein folding"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", set(), [])
        self.assertLess(scored["score"], CFG["candidate_threshold"])

    def test_dedupe_collapses_version_dois_by_title(self):
        low = {"source_system": "crossref", "title": "Execution Governance for AI Orchestration and Agentic Systems", "doi": "10.1/v1", "score": 8, "state": "needs_judgment"}
        high = {"source_system": "openalex", "title": "Execution Governance for AI Orchestration and Agentic Systems", "doi": "10.1/v2", "score": 9, "state": "candidate"}
        out = radar.dedupe([low, high])
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["score"], 9)
        self.assertIn("crossref", out[0]["also_seen_in"])
        self.assertIn("doi:10 1 v1", out[0]["alternate_identifiers"])


if __name__ == "__main__":
    unittest.main()
