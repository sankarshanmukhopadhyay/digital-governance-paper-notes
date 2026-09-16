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
        item = {"source_system": "openalex", "title": "Agentic AI Governance Authority and Redress", "abstract": "artificial intelligence interoperability governance authority redress accountability"}
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
        low = {"source_system": "crossref", "title": "Execution Governance for AI Orchestration and Agentic Systems", "doi": "10.1/v1", "score": 8, "state": "needs_judgment", "source_date_semantics": "registered_publication_metadata", "source_dates": {"published": "2026-09-01"}}
        high = {"source_system": "openalex", "title": "Execution Governance for AI Orchestration and Agentic Systems", "doi": "10.1/v2", "score": 9, "state": "candidate", "source_date_semantics": "index_publication_metadata", "source_dates": {"published": "2026-09-01"}}
        out = radar.dedupe([low, high])
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["score"], 9)
        self.assertIn("crossref", out[0]["also_seen_in"])
        self.assertIn("doi:10 1 v1", out[0]["alternate_identifiers"])

    def test_same_doi_different_titles_reconcile_to_one_record(self):
        a = {"source_system": "crossref", "title": "Governance for Agentic Systems", "doi": "10.1000/example", "score": 9, "state": "candidate", "source_date_semantics": "registered_publication_metadata", "source_dates": {"published": "2026-09-10"}}
        b = {"source_system": "openalex", "title": "Governance for Agentic Systems: A Framework", "doi": "10.1000/example", "score": 8, "state": "needs_judgment", "source_date_semantics": "index_publication_metadata", "source_dates": {"published": "2026-09-10"}}
        self.assertEqual(len(radar.dedupe([a, b])), 1)

    def test_conflicting_freshness_downgrades_candidate_to_judgment(self):
        recent = {"source_system": "openalex", "title": "Agentic AI Governance Authority", "doi": "10.1000/fresh", "score": 9, "state": "candidate", "source_date_semantics": "index_publication_metadata", "source_dates": {"published": "2026-09-12"}}
        older = {"source_system": "crossref", "title": "Agentic AI Governance Authority", "doi": "10.1000/fresh", "score": 9, "state": "candidate", "source_date_semantics": "registered_publication_metadata", "source_dates": {"published": "2026-04-03"}}
        out = radar.dedupe([recent, older])[0]
        self.assertEqual(out["freshness_status"], "conflicting")
        self.assertEqual(out["earliest_known_publication_at"], "2026-04-03")
        self.assertEqual(out["state"], "needs_judgment")
        self.assertTrue(out["freshness_requires_judgment"])

    def test_repository_date_is_not_rendered_as_verified_published(self):
        item = {"freshness_status": "source_consistent", "earliest_known_publication_at": "2026-04-03", "source_records": [{"source_system": "arxiv", "date_semantics": "repository_submission", "dates": {"published": "2026-04-03"}}]}
        line = radar.report_date_line(item)
        self.assertTrue(line.startswith("- Source date:"))
        self.assertNotIn("- Published:", line)

    def test_crossref_registered_publication_can_render_as_published(self):
        item = {"freshness_status": "verified", "earliest_known_publication_at": "2026-09-10", "source_records": [{"source_system": "crossref", "date_semantics": "registered_publication_metadata", "dates": {"published": "2026-09-10"}}]}
        self.assertEqual(radar.report_date_line(item), "- Published: 2026-09-10")


if __name__ == "__main__":
    unittest.main()
