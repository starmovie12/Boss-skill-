#!/usr/bin/env python3
"""design_seed.py - roll random values on design axes to provoke divergence (never palettes or fonts).

The roll is a provocation, not a decision: domain fit, platform convention and accessibility override it, and each
override is written with its reason in _boss/design-brief.md. Use --seed to reproduce a roll.
Exit 0 always on success, 2 on usage error.
"""
import argparse
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import emit  # noqa: E402

AXES = {
    "density": ["airy, few elements per view", "balanced", "compact, information-rich", "dense data, table-first"],
    "shape_language": ["sharp and rectilinear", "softly rounded", "fully round and pill-like", "mixed: one sharp family, one round accent shape", "drawn or irregular edges"],
    "type_voice": ["one family, contrast by weight only", "serif headings with a sans body", "a characterful display face used sparingly", "monospace accents for data and labels", "condensed headings with a wide body", "humanist, handwriting-adjacent warmth"],
    "color_strategy": ["near-monochrome plus one signal hue", "analogous family of two or three neighbors", "neutral-forward with one high-chroma accent", "complementary pair with one dominant", "full-chroma expressive", "dark base with luminous accents", "light base with deep ink accents"],
    "imagery_strategy": ["no imagery, typography carries it", "real photography of the actual subject", "illustration in one consistent style", "data and diagrams as the imagery", "texture or pattern derived from the domain", "product UI shown in context"],
    "layout_archetype": ["single column, editorial rhythm", "asymmetric split with a strong left or right anchor", "modular grid of unequal tiles", "full-bleed bands alternating density", "sidebar plus workspace", "stacked cards with one featured element", "timeline or step sequence"],
    "motion_character": ["almost none, instant state changes", "subtle fades and position shifts", "springy and tactile", "one choreographed signature moment, everything else still", "scroll-linked reveals used sparingly"],
}
APP_EXTRA = {"navigation_feel": ["bottom tabs with a centered primary action", "plain bottom tabs", "single stack with a home hub", "top segmented control inside one tab"],
             "haptics": ["none beyond system defaults", "light selection ticks", "distinct success and warning patterns"]}


def roll(seed=None, platform="web"):
    seed = int(seed) if seed is not None else int(time.time() * 1000) % 1_000_000
    rng = random.Random(seed)
    axes = dict(AXES)
    if platform == "app":
        axes.update(APP_EXTRA)
    picks = {k: rng.choice(v) for k, v in axes.items()}
    return {"check": "design_seed", "seed": seed, "platform": platform, "roll": picks,
            "rule": "Provocation only. Override any axis that hurts domain fit, platform convention or accessibility, and write why."}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", help="integer seed to reproduce a roll")
    ap.add_argument("--platform", choices=["web", "app"], default="web")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.seed is not None and not str(a.seed).lstrip("-").isdigit():
        print("--seed must be an integer", file=sys.stderr)
        return 2
    return emit(roll(a.seed, a.platform), a.json, ok=True)


if __name__ == "__main__":
    sys.exit(main())
