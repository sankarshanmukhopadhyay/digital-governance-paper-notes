import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("paper_radar", ROOT / "scripts" / "paper_radar.py")
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)

intake_spec = importlib.util.spec_from_file_location("paper_radar_intake", ROOT / "scripts" / "paper_radar_intake.py")
intake = importlib.util.module_from_spec(intake_spec)
intake_spec.loader.exec_module(intake)

CFG = {
    "candidate_threshold": 9,
    "judgment_threshold": 7,
    "themes": [{"name": "ai-governance", "anchors": ["AI", "artificial intelligence", "agentic"]}],
    "governance_signals": ["governance", "authority", "redress", "interoperability", "accountability"],
    "material_governance_signals": ["authority", "redress", "interoperability", "accountability"],
    "candidate_title_signals": ["governance", "authority", "redress", "accountability"],
    "exclusion_signals": ["protein folding"],
    "source_weights": {"arxiv": 1, "crossref": 1, "openalex": 1},
    "issue_intake": {"deferred_reconsider_days": 90},
    "breadth": {
        "governance_relevance_threshold": 0.35,
        "horizon_limit": 2,
        "serendipity_limit": 1,
        "serendipity_novelty_threshold": 0.68,
        "novelty_rate_threshold": 0.60,
        "quality_baseline": 0.70,
        "underrepresented_domain_max": 1,
    },
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

    def test_issue_intake_only_selects_candidate_and_judgment(self):
        payload = {"items": [
            {"title": "Candidate", "state": "candidate", "already_represented": False},
            {"title": "Judgment", "state": "needs_judgment", "already_represented": False},
            {"title": "Deferred", "state": "deferred", "already_represented": False},
            {"title": "Known", "state": "candidate", "already_represented": True},
        ]}
        self.assertEqual(
            [item["title"] for item in intake.select_items(payload)],
            ["Candidate", "Judgment"],
        )

    def test_issue_intake_maps_radar_labels(self):
        cfg = {"issue_intake": {"candidate_label": "radar:candidate", "judgment_label": "radar:needs-judgment"}}
        self.assertEqual(intake.intake_label({"state": "candidate"}, cfg), "radar:candidate")
        self.assertEqual(intake.intake_label({"state": "needs_judgment"}, cfg), "radar:needs-judgment")

    def test_closed_declined_issue_is_suppressed(self):
        issue = {"state": "closed", "labels": [{"name": "disposition:declined"}], "closed_at": "2026-01-01T00:00:00Z"}
        self.assertTrue(radar.issue_should_suppress(issue, CFG, radar.dt.date(2026, 9, 22)))

    def test_recent_deferred_issue_is_suppressed(self):
        issue = {"state": "closed", "labels": [{"name": "disposition:deferred"}], "closed_at": "2026-09-01T00:00:00Z"}
        self.assertTrue(radar.issue_should_suppress(issue, CFG, radar.dt.date(2026, 9, 22)))

    def test_old_deferred_issue_can_resurface(self):
        issue = {"state": "closed", "labels": [{"name": "disposition:deferred"}], "closed_at": "2026-05-01T00:00:00Z"}
        self.assertFalse(radar.issue_should_suppress(issue, CFG, radar.dt.date(2026, 9, 22)))

    def test_closed_nonterminal_issue_does_not_suppress(self):
        issue = {"state": "closed", "labels": [], "closed_at": "2026-09-01T00:00:00Z"}
        self.assertFalse(radar.issue_should_suppress(issue, CFG, radar.dt.date(2026, 9, 22)))

    def test_repository_date_is_not_rendered_as_verified_published(self):
        item = {"freshness_status": "source_consistent", "earliest_known_publication_at": "2026-04-03", "source_records": [{"source_system": "arxiv", "date_semantics": "repository_submission", "dates": {"published": "2026-04-03"}}]}
        line = radar.report_date_line(item)
        self.assertTrue(line.startswith("- Source date:"))
        self.assertNotIn("- Published:", line)

    def test_crossref_registered_publication_can_render_as_published(self):
        item = {"freshness_status": "verified", "earliest_known_publication_at": "2026-09-10", "source_records": [{"source_system": "crossref", "date_semantics": "registered_publication_metadata", "dates": {"published": "2026-09-10"}}]}
        self.assertEqual(radar.report_date_line(item), "- Published: 2026-09-10")


    def test_core_scoring_declares_core_without_changing_candidate_result(self):
        item = {"source_system": "openalex", "title": "Agentic AI Governance Authority and Redress", "abstract": "artificial intelligence interoperability governance authority redress accountability"}
        scored = radar.score(item, CFG, "ai-governance", "AI governance authority", set(), [])
        self.assertEqual(scored["state"], "candidate")
        self.assertEqual(scored["discovery_class"], "core")
        self.assertTrue(scored["selected_for_intake"])

    def test_adjacent_novelty_cannot_bypass_governance_gate(self):
        theme = {"name": "digital-markets", "primary_topic": "Economic & Market Infrastructure", "anchors": ["digital markets"]}
        corpus = [{"tokens": {"agentic", "governance", "authority"}, "primary_domain": "AI Governance", "publication": "Example"}]
        item = {"source_system": "openalex", "title": "Digital Markets Pricing Models", "abstract": "digital markets pricing demand supply", "publication": "Journal X"}
        scored = radar.breadth.score_adjacent(
            item, CFG, theme, "digital markets", set(), [], corpus,
            radar.norm, radar.identity_keys, radar.phrase_in_text,
        )
        self.assertEqual(scored["state"], "deferred")
        self.assertGreater(scored["novelty_score"], 0.5)
        self.assertLess(scored["governance_relevance_score"], CFG["breadth"]["governance_relevance_threshold"])

    def test_adjacent_governance_candidate_records_explanation_and_novelty(self):
        theme = {"name": "digital-markets", "primary_topic": "Economic & Market Infrastructure", "anchors": ["digital markets"]}
        corpus = [{"tokens": {"agentic", "governance", "authority"}, "primary_domain": "AI Governance", "publication": "Example"}]
        item = {
            "source_system": "openalex",
            "title": "Digital Markets Governance and Platform Accountability",
            "abstract": "digital markets regulation accountability authority rights institutional enforcement",
            "publication": "Journal Y",
        }
        scored = radar.breadth.score_adjacent(
            item, CFG, theme, "digital markets governance", set(), [], corpus,
            radar.norm, radar.identity_keys, radar.phrase_in_text,
        )
        self.assertEqual(scored["state"], "candidate")
        self.assertEqual(scored["discovery_class"], "horizon")
        self.assertIsNotNone(scored["novelty_score"])
        self.assertTrue(scored["why_this_appeared"])
        self.assertEqual(scored["primary_topic"], "Economic & Market Infrastructure")

    def test_non_core_mix_enforces_horizon_and_serendipity_quotas(self):
        items = []
        for i, novelty in enumerate([0.95, 0.90, 0.80, 0.50, 0.40, 0.30]):
            items.append({
                "title": f"Paper {i}",
                "state": "candidate",
                "already_represented": False,
                "discovery_class": "horizon",
                "governance_relevance_score": 0.8,
                "quality_score": 0.8,
                "novelty_score": novelty,
                "why_this_appeared": "eligible",
                "selected_for_intake": False,
            })
        mixed = radar.breadth.apply_non_core_mix(items, CFG)
        selected = [x for x in mixed if x.get("selected_for_intake")]
        self.assertEqual(sum(x["discovery_class"] == "serendipity" for x in selected), 1)
        self.assertLessEqual(sum(x["discovery_class"] == "horizon" for x in selected), 2)
        self.assertTrue(all(x["state"] == "deferred" for x in mixed if not x.get("selected_for_intake")))

    def test_missing_corpus_does_not_become_serendipity_by_assumption(self):
        item = {
            "title": "Adjacent governance paper",
            "state": "candidate",
            "already_represented": False,
            "discovery_class": "horizon",
            "governance_relevance_score": 0.9,
            "quality_score": 0.8,
            "novelty_score": None,
            "why_this_appeared": "eligible",
            "selected_for_intake": False,
        }
        mixed = radar.breadth.apply_non_core_mix([item], CFG)
        self.assertEqual(mixed[0]["discovery_class"], "horizon")
        self.assertTrue(mixed[0]["selected_for_intake"])

    def test_intake_ignores_non_core_overflow(self):
        payload = {"items": [
            {"title": "Selected", "state": "candidate", "already_represented": False, "selected_for_intake": True},
            {"title": "Overflow", "state": "candidate", "already_represented": False, "selected_for_intake": False},
        ]}
        self.assertEqual([x["title"] for x in intake.select_items(payload)], ["Selected"])

    def test_telemetry_reports_class_source_and_novelty_mix(self):
        items = [
            {"state": "candidate", "already_represented": False, "selected_for_intake": True, "discovery_class": "core", "publication": "A", "theme": "ai-governance", "novelty_score": None, "source_previously_seen": None},
            {"state": "candidate", "already_represented": False, "selected_for_intake": True, "discovery_class": "horizon", "publication": "B", "primary_topic": "Privacy", "novelty_score": 0.7, "source_previously_seen": False},
            {"state": "candidate", "already_represented": False, "selected_for_intake": True, "discovery_class": "serendipity", "publication": "C", "primary_topic": "Markets", "novelty_score": 0.9, "source_previously_seen": False},
        ]
        metrics = radar.breadth.telemetry(items, CFG)
        self.assertEqual(metrics["candidate_volume_by_class"], {"core": 1, "horizon": 1, "serendipity": 1})
        self.assertEqual(metrics["distinct_sources"], 3)
        self.assertEqual(metrics["new_source_count"], 2)
        self.assertEqual(metrics["novelty_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
