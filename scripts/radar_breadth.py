#!/usr/bin/env python3
"""Controlled-breadth scoring, corpus novelty, quotas, and telemetry for Paper Radar."""
from __future__ import annotations

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
    """Load a deterministic recent-review comparison window from canonical review files."""
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
    """Return maximum token-set Jaccard similarity to the comparison corpus."""
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


def score_adjacent(
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
    """Score an adjacent-domain record without weakening Core Radar semantics."""
    title = norm(item.get("title", ""))
    text = norm((item.get("title") or "") + " " + (item.get("abstract") or ""))
    anchors = [a for a in theme.get("anchors", []) if phrase_in_text(text, a)]
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
    elif relevance >= threshold:
        state = "candidate"
    else:
        state = "deferred"

    novelty_component = novelty if novelty is not None else 0.0
    points = round(10.0 * ((0.45 * relevance) + (0.35 * quality) + (0.20 * novelty_component)), 2)

    counts = domain_frequency(corpus)
    topic = theme.get("primary_topic") or theme.get("name") or "adjacent"
    topic_count = counts.get(topic, 0)
    underrepresented = topic_count <= int((cfg.get("breadth") or {}).get("underrepresented_domain_max", 1))

    if state == "represented":
        rationale = "Already represented in the review corpus or editorial issue history."
    elif state == "deferred" and not anchors:
        rationale = "Adjacent-domain record lacked the configured domain anchor required for controlled breadth."
    elif state == "deferred":
        rationale = "Adjacent-domain record did not satisfy the minimum governance-relevance gate."
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
        "governance_signals": signals,
        "material_governance_signals": material,
        "candidate_title_signals": [],
        "query_matches": [],
        "exclusion_signals": exclusions,
        "score": points,
        "state": state,
        "already_represented": bool(exact_existing or near_existing),
        "discovery_class": "horizon",
        "primary_topic": topic,
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


def apply_non_core_mix(items: list[dict], cfg: dict) -> list[dict]:
    """Select bounded Horizon/Serendipity intake while retaining overflow as evidence."""
    breadth = cfg.get("breadth") or {}
    horizon_limit = int(breadth.get("horizon_limit", 4))
    serendipity_limit = int(breadth.get("serendipity_limit", 2))
    novelty_threshold = float(breadth.get("serendipity_novelty_threshold", 0.68))
    relevance_threshold = float(breadth.get("governance_relevance_threshold", 0.35))

    eligible = [
        x for x in items
        if x.get("state") in {"candidate", "needs_judgment"}
        and not x.get("already_represented")
        and float(x.get("governance_relevance_score") or 0) >= relevance_threshold
    ]

    serendipity = sorted(
        [x for x in eligible if x.get("novelty_score") is not None and float(x["novelty_score"]) >= novelty_threshold],
        key=lambda x: (-float(x.get("novelty_score") or 0), -float(x.get("governance_relevance_score") or 0), x.get("title") or ""),
    )[:serendipity_limit]
    serendipity_ids = {id(x) for x in serendipity}

    horizon = sorted(
        [x for x in eligible if id(x) not in serendipity_ids],
        key=lambda x: (-float(x.get("governance_relevance_score") or 0), -float(x.get("quality_score") or 0), -float(x.get("novelty_score") or 0), x.get("title") or ""),
    )[:horizon_limit]
    horizon_ids = {id(x) for x in horizon}

    for item in items:
        if id(item) in serendipity_ids:
            item["discovery_class"] = "serendipity"
            item["selected_for_intake"] = True
            item["why_this_appeared"] = (
                item.get("why_this_appeared", "")
                + " Selected as a bounded Serendipity candidate because novelty cleared the configured threshold."
            ).strip()
        elif id(item) in horizon_ids:
            item["discovery_class"] = "horizon"
            item["selected_for_intake"] = True
        elif item.get("discovery_class") in {"horizon", "serendipity"} and item.get("state") in {"candidate", "needs_judgment"}:
            item["state"] = "deferred"
            item["selected_for_intake"] = False
            item["why_this_appeared"] = (
                item.get("why_this_appeared", "")
                + " Eligible but outside this cycle's configured non-Core quota."
            ).strip()
    return items


def telemetry(items: list[dict], cfg: dict) -> dict:
    surfaced = [
        x for x in items
        if x.get("state") in {"candidate", "needs_judgment"}
        and not x.get("already_represented")
        and x.get("selected_for_intake", True)
    ]
    class_counts = Counter(x.get("discovery_class", "core") for x in surfaced)
    sources = Counter(x.get("publication") or x.get("source_system") or "unknown" for x in surfaced)
    topics = Counter(x.get("primary_topic") or x.get("theme") or "unknown" for x in surfaced)
    total = len(surfaced)
    top_five = sum(count for _, count in sources.most_common(5))
    novelty_threshold = float((cfg.get("breadth") or {}).get("novelty_rate_threshold", 0.60))
    novelty_observed = [x for x in surfaced if x.get("novelty_score") is not None]
    novel = [x for x in novelty_observed if float(x["novelty_score"]) >= novelty_threshold]
    return {
        "surfaced_total": total,
        "candidate_volume_by_class": dict(sorted(class_counts.items())),
        "distinct_sources": len(sources),
        "new_source_count": sum(1 for x in surfaced if x.get("source_previously_seen") is False),
        "top_five_source_share": round(top_five / total, 4) if total else 0.0,
        "topic_distribution": dict(sorted(topics.items())),
        "novelty_rate": round(len(novel) / len(novelty_observed), 4) if novelty_observed else None,
        "novelty_observed_count": len(novelty_observed),
    }
