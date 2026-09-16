import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("paper_radar", ROOT / "scripts" / "paper_radar.py")
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)

CFG = {
    "candidate_threshold": 7,
    "judgment_threshold": 5,
    "governance_signals": ["governance", "authority", "redress", "interoperability"],
    "exclusion_signals": ["protein folding"],
    "source_weights": {"arxiv": 1, "crossref": 1, "openalex": 1},
}


class PaperRadarTests(unittest.TestCase):
    def test_canonical_doi_key_normalises_url(self):
        self.assertEqual(radar.canonical_key({"doi": "https://doi.org/10.1000/XYZ"}), "doi:10 1000 xyz")

    def test_existing_paper_never_returns_as_fresh_candidate(self):
        item = {"source_system": "arxiv", "title": "Governance and Authority in AI Systems", "abstract": "governance authority redress interoperability", "arxiv_id": "2609.12345"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", {"arxiv:2609.12345"}, [])
        self.assertEqual(scored["state"], "published")
        self.assertTrue(scored["already_in_corpus"])

    def test_score_is_diagnostic_not_admission(self):
        item = {"source_system": "openalex", "title": "Governance Authority and Redress for AI", "abstract": "interoperability governance authority redress"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", set(), [])
        self.assertEqual(scored["state"], "candidate")
        self.assertNotIn("queue", scored)

    def test_exclusion_signal_reduces_score(self):
        item = {"source_system": "crossref", "title": "Governance for Protein Folding", "abstract": "governance authority protein folding"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", set(), [])
        self.assertLess(scored["score"], CFG["candidate_threshold"])

    def test_dedupe_prefers_higher_scoring_record(self):
        low = {"title": "Same Paper", "doi": "10.1/a", "score": 4, "state": "deferred"}
        high = {"title": "Same Paper", "doi": "10.1/a", "score": 8, "state": "candidate"}
        out = radar.dedupe([low, high])
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["score"], 8)


if __name__ == "__main__":
    unittest.main()
