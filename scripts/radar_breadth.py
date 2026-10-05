#!/usr/bin/env python3
"""Coverage scoring, corpus novelty, intake mixing, and telemetry for Paper Radar."""
from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path


def norm_text(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).split())


def token_set(value: str) -> set[str]:
    return {token for token in norm_text(value).split() if len(token) > 3}


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf'^{re.escape(key)}:\s*["\']?(.*?)["\']?\s*$', text, re.M)
    return match.group(1).strip() if match else ""


def load_recent_corpus(root: Path, limit: int = 30) -> list[dict]:
    reviews = sorted(root.glob("reviews/**/*.md"), reverse=True)[: max(0, int(limit))]
    corpus = []
    for path in reviews:
        text = path.read_text(encoding="utf-8")
        title = frontmatter_value(text, "title")
        key_insight = frontmatter_value(text, "key_insight")
        primary_domain = frontmatter_value(text, "primary_domain")
        publication = frontmatter_value(text, "publication")
        comparison_text = " ".join(part for part in (title, key_insight, primary_domain) if part)
        corpus.append({
            "path": str(path.relative_to(root)),
            "title": title,
            "primary_domain": primary_domain,
            "publication": publication,
            "tokens": token_set(comparison_text),
        })
    return corpus


def corpus_similarity(item: dict, corpus: list[dict]) -> float | None:
    candidate = token_set((item.get("title") or "") + " " + (item.get("abstract") or ""))
    if not candidate or not corpus:
        return None
    scores = []
    for review in corpus:
        other = review.get("tokens") or set()
        if not other:
            continue
        union = candidate | other
        if union:
            scores.append(len(candidate & other) / len(union))
    return max(scores) if scores else None


def governance_relevance(item: dict, cfg: dict) -> float:
    text = norm_text((item.get("title") or "") + " " + (item.get("abstract") or ""))
    signals = [s for s in cfg.get("governance_signals", []) if f" {norm_text(s)} " in f" {text} "]
    material = [s for s in cfg.get("material_governance_signals", []) if f" {norm_text(s)} " in f" {text} "]
    raw = len(signals) + (2 * len(material))
    return min(1.0, raw / 8.0)


def quality_score(item: dict, cfg: dict) -> float:
    source_weight = float((cfg.get("source_weights") or {}).get(item.get("source_system"), 0))
    baseline = float((cfg.get("breadth") or {}).get("quality_baseline", 0.7))
    return min(1.0, max(0.0, baseline + (0.05 * source_weight)))


def domain_frequency(corpus: list[dict]) -> Counter:
    return Counter(review.get("primary_domain") for review in corpus if review.get("primary_domain"))


def source_seen(item: dict, corpus: list[dict]) -> bool:
    publication = norm_text(item.get("publication") or "")
    if not publication:
        return False
    return any(publication == norm_text(review.get("publication") or "") for review in corpus)


def score_coverage(
    item: dict,
    cfg: dict,
    theme: dict,
    query: str,
    existing_keys: set[str],
    existing_titles: list[str],
    corpus: list[dict],
    norm,
    identity_keys,
    phrase_in_text,
) -> dict:
    """Score a first-class Coverage record without weakening the governance gate."""
    title = norm(item.get("title", ""))
    text = norm((item.get("title") or "") + " " + (item.get("abstract") or ""))
    anchors = [a for a in theme.get("anchors", []) if phrase_in_text(text, a)]
    context_signals = [s for s in theme.get("context_signals", []) if phrase_in_text(text, s)]
    title_context_signals = [s for s in theme.get("context_signals", []) if phrase_in_text(title, s)]
    signals = [s for s in cfg.get("governance_signals", []) if phrase_in_text(text, s)]
    material = [s for s in cfg.get("material_governance_signals", []) if phrase_in_text(text, s)]
    exclusions = [s for s in cfg.get("exclusion_signals", []) if phrase_in_text(text, s)]
    near_existing = any(title and (title == t or (len(title) > 28 and (title in t or t in title))) for t in existing_titles)
    exact_existing = bool(identity_keys(item) & existing_keys)

    similarity = corpus_similarity(item, corpus)
    novelty = None if similarity is None else max(0.0, min(1.0, 1.0 - similarity))
    relevance = governance_relevance(item, cfg)
    quality = quality_score(item, cfg)
    threshold = float((cfg.get("breadth") or {}).get("governance_relevance_threshold", 0.35))

    if exact_existing or near_existing:
        state = "represented"
    elif not anchors or exclusions:
        state = "deferred"
    elif theme.get("context_signals") and not context_signals:
        state = "deferred"
    elif theme.get("require_title_context") and not title_context_signals:
        state = "deferred"
    elif not material:
        state = "deferred"
    elif relevance >= threshold:
        state = "candidate"
    else:
        state = "deferred"

    novelty_component = novelty if novelty is not None else 0.0
    points = round(10.0 * ((0.45 * relevance) + (0.35 * quality) + (0.20 * novelty_component)), 2)

    counts = domain_frequency(corpus)
    topic = theme.get("primary_topic") or theme.get("name") or "coverage"
    topic_count = counts.get(topic, 0)
    underrepresented = topic_count <= int((cfg.get("breadth") or {}).get("underrepresented_domain_max", 1))

    if state == "represented":
        rationale = "Already represented in the review corpus or editorial issue history."
    elif state == "deferred" and not anchors:
        rationale = "Coverage record lacked the configured institutional-domain anchor."
    elif state == "deferred" and theme.get("context_signals") and not context_signals:
        rationale = "Coverage record matched an institutional term but lacked a digital or technology context signal."
    elif state == "deferred" and theme.get("require_title_context") and not title_context_signals:
        rationale = "Coverage record mentioned digital or technology context only in the body/abstract, not in the paper title; it is deferred to preserve intake precision."
    elif state == "deferred" and not material:
        rationale = "Coverage record lacked a material governance mechanism such as authority, accountability, rights, liability, redress, or enforcement."
    elif state == "deferred":
        rationale = "Coverage record did not satisfy the minimum governance-relevance gate."
    else:
        novelty_text = "unknown" if novelty is None else f"{novelty:.2f}"
        representation = "underrepresented" if underrepresented else "represented"
        rationale = (
            f"Governance-relevant work in {topic}; recent-corpus novelty={novelty_text}; "
            f"the topic is {representation} in the comparison window."
        )

    item.update({
        "theme": theme.get("name"),
        "matched_query": query,
        "theme_anchors": anchors,
        "context_signals": context_signals,
        "title_context_signals": title_context_signals,
        "governance_signals": signals,
        "material_governance_signals": material,
        "candidate_title_signals": [],
        "query_matches": [],
        "exclusion_signals": exclusions,
        "score": points,
        "state": state,
        "already_represented": bool(exact_existing or near_existing),
        "discovery_class": "coverage",
        "theme_kind": "coverage",
        "primary_topic": topic,
        "specificity_rank": int(theme.get("specificity_rank", 90)),
        "secondary_topics": sorted(set(anchors + material)),
        "governance_relevance_score": round(relevance, 4),
        "quality_score": round(quality, 4),
        "similarity_to_recent_corpus": None if similarity is None else round(similarity, 4),
        "novelty_score": None if novelty is None else round(novelty, 4),
        "source_previously_seen": source_seen(item, corpus),
        "underrepresented_domain": underrepresented,
        "why_this_appeared": rationale,
        "selected_for_intake": False,
    })
    return item


def score_adjacent(*args, **kwargs):
    """Backward-compatible alias retained for tests and older local tooling."""
    return score_coverage(*args, **kwargs)


def _selection_value(item: dict) -> tuple:
    relevance = item.get("governance_relevance_score")
    relevance = 1.0 if relevance is None and item.get("discovery_class") == "core" else float(relevance or 0)
    quality = item.get("quality_score")
    quality = 0.75 if quality is None else float(quality)
    novelty = float(item.get("novelty_score") or 0)
    score = float(item.get("score") or 0) / 10.0
    return (0.45 * relevance) + (0.25 * quality) + (0.20 * score) + (0.10 * novelty)


def apply_intake_mix(items: list[dict], cfg: dict) -> list[dict]:
    """Select a bounded intake while preventing one theme from crowding out qualified alternatives."""
    breadth = cfg.get("breadth") or {}
    intake_limit = max(1, int(breadth.get("intake_limit", 18)))
    max_theme_share = min(1.0, max(0.1, float(breadth.get("max_theme_share", 0.5))))
    theme_cap = max(1, int(math.floor(intake_limit * max_theme_share)))
    novelty_threshold = float(breadth.get("serendipity_novelty_threshold", 0.68))
    serendipity_limit = max(0, int(breadth.get("serendipity_limit", 2)))

    eligible = [
        x for x in items
        if x.get("state") in {"candidate", "needs_judgment"}
        and not x.get("already_represented")
    ]
    ranked = sorted(
        eligible,
        key=lambda x: (-_selection_value(x), -int(x.get("specificity_rank", 0)), x.get("title") or ""),
    )

    selected: list[dict] = []
    per_theme: Counter = Counter()

    novel = [
        x for x in ranked
        if x.get("discovery_class") == "coverage"
        and x.get("novelty_score") is not None
        and float(x.get("novelty_score") or 0) >= novelty_threshold
    ][:serendipity_limit]
    novel_ids = {id(x) for x in novel}
    for item in novel:
        selected.append(item)
        per_theme[item.get("theme") or "unknown"] += 1

    for item in ranked:
        if len(selected) >= intake_limit:
            break
        if id(item) in novel_ids:
            continue
        theme = item.get("theme") or "unknown"
        alternatives_exist = any(
            other is not item
            and id(other) not in {id(x) for x in selected}
            and (other.get("theme") or "unknown") != theme
            for other in ranked
        )
        if alternatives_exist and per_theme[theme] >= theme_cap:
            continue
        selected.append(item)
        per_theme[theme] += 1

    # Conditional guard: if qualified alternatives are insufficient, fill remaining capacity
    # rather than suppressing strong work solely to satisfy a distribution target.
    if len(selected) < intake_limit:
        selected_ids = {id(x) for x in selected}
        for item in ranked:
            if len(selected) >= intake_limit:
                break
            if id(item) not in selected_ids:
                selected.append(item)
                selected_ids.add(id(item))

    selected_ids = {id(x) for x in selected}
    for item in items:
        if id(item) in selected_ids:
            item["selected_for_intake"] = True
            if id(item) in novel_ids:
                item["discovery_class"] = "serendipity"
                item["why_this_appeared"] = (
                    item.get("why_this_appeared", "")
                    + " Selected through the bounded Serendipity lane because novelty cleared the configured threshold."
                ).strip()
        elif item.get("state") in {"candidate", "needs_judgment"} and not item.get("already_represented"):
            item["selected_for_intake"] = False
            item["intake_status"] = "qualified-overflow"
            item["why_this_appeared"] = (
                item.get("why_this_appeared", "")
                + " Qualified for Radar but not selected in this cycle's bounded intake."
            ).strip()
    return items


def apply_non_core_mix(items: list[dict], cfg: dict) -> list[dict]:
    """Backward-compatible wrapper. New code should call apply_intake_mix on the combined candidate set."""
    return apply_intake_mix(items, cfg)


def telemetry(items: list[dict], cfg: dict) -> dict:
    qualified = [
        x for x in items
        if x.get("state") in {"candidate", "needs_judgment"}
        and not x.get("already_represented")
    ]
    surfaced = [x for x in qualified if x.get("selected_for_intake", True)]
    overflow = [x for x in qualified if not x.get("selected_for_intake", True)]

    class_counts = Counter(x.get("discovery_class", "core") for x in surfaced)
    sources = Counter(x.get("publication") or x.get("source_system") or "unknown" for x in surfaced)
    topics = Counter(x.get("primary_topic") or x.get("theme") or "unknown" for x in surfaced)
    themes = Counter(x.get("theme") or "unknown" for x in surfaced)
    qualified_themes = Counter(x.get("theme") or "unknown" for x in qualified)
    total = len(surfaced)
    top_five = sum(count for _, count in sources.most_common(5))
    novelty_threshold = float((cfg.get("breadth") or {}).get("novelty_rate_threshold", 0.60))
    novelty_observed = [x for x in surfaced if x.get("novelty_score") is not None]
    novel = [x for x in novelty_observed if float(x["novelty_score"]) >= novelty_threshold]
    largest_theme, largest_count = ("", 0)
    if themes:
        largest_theme, largest_count = themes.most_common(1)[0]
    largest_share = round(largest_count / total, 4) if total else 0.0
    warning_threshold = float((cfg.get("breadth") or {}).get("dominance_warning_share", 0.6))

    return {
        "qualified_total": len(qualified),
        "surfaced_total": total,
        "qualified_overflow_total": len(overflow),
        "candidate_volume_by_class": dict(sorted(class_counts.items())),
        "distinct_sources": len(sources),
        "new_source_count": sum(1 for x in surfaced if x.get("source_previously_seen") is False),
        "top_five_source_share": round(top_five / total, 4) if total else 0.0,
        "topic_distribution": dict(sorted(topics.items())),
        "theme_distribution": dict(sorted(themes.items())),
        "qualified_theme_distribution": dict(sorted(qualified_themes.items())),
        "largest_theme": largest_theme or None,
        "largest_theme_share": largest_share,
        "dominance_warning": bool(total and largest_share > warning_threshold),
        "novelty_rate": round(len(novel) / len(novelty_observed), 4) if novelty_observed else None,
        "novelty_observed_count": len(novelty_observed),
    }
