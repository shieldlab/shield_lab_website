"""Count and render publication topics from the canonical bibliography."""
from collections import Counter
from html import escape


def rank_topics(records, topic_data, limit=5):
    """Return the latest three-year window and ranked nonempty topic counts."""
    dated = [(int(str(p["year"])), p) for p in records if str(p.get("year", "")).isdigit()]
    if not dated:
        return None, []
    latest = max(year for year, _ in dated)
    first = latest - 2
    known = set(topic_data["taxonomy"])
    counts = Counter()
    for year, paper in dated:
        if first <= year <= latest:
            tags = set(topic_data["assignments"].get(str(paper["index"]), []))
            counts.update(tags & known)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0].casefold(), item[0]))
    return (first, latest), ordered[:limit]


def render_topic_chart(records, topic_data):
    _, ordered = rank_topics(records, topic_data, limit=None)
    ranked = ordered[:5]
    if not ranked:
        return ""
    maximum = ranked[0][1]
    def row(topic, count):
        return (
            f'<li><span class="topic-chart-label">{escape(topic)}</span>'
            f'<span class="topic-chart-track" aria-hidden="true"><span style="--topic-width:{100*count/maximum:.2f}%"></span></span>'
            f'<strong class="topic-chart-count">{count}</strong></li>'
        )
    rows = "".join(row(topic, count) for topic, count in ranked)
    featured = ""
    quantum = dict(ordered[5:]).get("Quantum AI")
    if quantum:
        featured = f'<ul class="topic-chart-featured" role="list" aria-label="Featured topic">{row("Quantum AI", quantum)}</ul>'
    return (
        '<section class="publication-topic-chart" id="top-publication-topics" aria-labelledby="publication-topic-chart-title">'
        '<h2 id="publication-topic-chart-title">Top Topics in Recent Publications</h2>'
        f'<ol role="list">{rows}</ol>{featured}</section>'
    )
