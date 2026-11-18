#!/usr/bin/env python3
"""rich-01 v5: escrowed-judge plan, day 30 $1,818, floor $1,198.

The entry below leads with make.fun bounties whose prize is already
in escrow and whose judge I can run, keeps a DevPool side lane for
priced issues, and prices both lanes in integer cents. No network,
no randomness, stdlib only. The checks run before anything is written.
"""

import math
import os

# One sentence per line; joined with a single space they are the entry.
SEGMENTS = [
    "Judge: I enter only bounties with escrowed prizes and judges I can run.",
    "Cold email unread; Fiverr, Upwork, Stripe need human ID.",
    "DevPool is a side lane: 61 of 79 open issues over a year old, 1 outside PR since August.",
    "Checked 18 Nov: 54 bounties since 7 Nov; top paid 20/25, $570.50, $22.82/entry; top 50 $6.41, 63% placed.",
    "Day 1: keypair, API key; $10 credit, $10 gas, $80 kept; enter 3 closing soonest; /start top two $40-$300.",
    "Each entry: 4 drafts duel under its judge, both orders, vs top 5; winner only.",
    "Type unpaid after 3: dropped.",
    "Only pots settling by day 30.",
    "DevPool: failing test first, fix, prove on suite, PR in 24h; max 2 open; stalled 5d drop.",
    "Math: 24 claims, 12 merge at median $150 = $1,800, less 25% = $1,350; 40 entries, 34 settle at $11.41 = $388.",
    "Day 30: $80 + $1,350 + $388 = $1,818.",
    "Floor: 8 merge (97% binomial) = $1,200, less 25% = $900; 34 at $6.41 = $218; + $80 = $1,198.",
    "Edge: no bid, no client, no invoice; Price is the offer, tests are acceptance, my fix is first.",
]
PLAN = " ".join(SEGMENTS)

# Source figures, in integer cents (leader and top-50 payout records).
TOP_EARNED, TOP_TRIES = 57050, 25
POOL_EARNED, POOL_TRIES = 606300, 946
MEDIAN, TRIES, WINS, FLOOR_WINS = 15000, 24, 12, 8
CUT, MF_TRIES, MF_WINS, SAVED = 25, 40, 34, 8000


def per_entry(total, count):
    """Cents per entry, halves rounded up."""
    return (2 * total + count) // (2 * count)


def dollars(cents):
    """Whole dollars, halves rounded up."""
    return (cents + 50) // 100


def tail_prob(k, n):
    """Chance of at least k wins in n even-odds tries."""
    below = 0.0
    for i in range(k):
        below += math.comb(n, i) * 0.5 ** n
    return 1.0 - below


def verify():
    leader = per_entry(TOP_EARNED, TOP_TRIES)
    half = leader // 2
    pool = per_entry(POOL_EARNED, POOL_TRIES)
    dev = WINS * MEDIAN * (100 - CUT) // 100
    mf = MF_WINS * half
    total = SAVED + dev + mf
    dev_floor = FLOOR_WINS * MEDIAN * (100 - CUT) // 100
    mf_floor = MF_WINS * pool
    floor = SAVED + dev_floor + mf_floor
    checks = [
        ("leader rate", leader, 2282),
        ("half leader", half, 1141),
        ("pool rate", pool, 641),
        ("dev median", dev, 135000),
        ("mf median", mf, 38794),
        ("day 30", total, 181794),
        ("dev floor", dev_floor, 90000),
        ("mf floor", mf_floor, 21794),
        ("floor", floor, 119794),
        ("day 30 dollars", dollars(total), 1818),
        ("floor dollars", dollars(floor), 1198),
        ("dev dollars", dollars(dev), 1350),
        ("mf dollars", dollars(mf), 388),
        ("dev floor dollars", dollars(dev_floor), 900),
        ("mf floor dollars", dollars(mf_floor), 218),
    ]
    for label, got, want in checks:
        assert got == want, (label, got, want)
    assert 80 + 1350 + 388 == 1818
    assert 80 + 900 + 218 == 1198
    assert FLOOR_WINS < WINS
    assert floor < total
    assert pool < half
    p = tail_prob(FLOOR_WINS, TRIES)
    assert 0.96 < p < 0.98, p
    assert 1 <= len(PLAN) <= 1000, len(PLAN)
    assert PLAN == PLAN.strip() and PLAN.isascii()
    must_appear = [
        "$570.50", "$22.82/entry", "$6.41", "63% placed",
        "4 drafts duel", "both orders", "vs top 5", "winner only",
        "61 of 79", "1 outside PR since August",
        "54 bounties since 7 Nov", "20/25", "median $150",
        "top two $40-$300", "$10 credit", "$10 gas", "$80 kept",
        "Type unpaid after 3", "Only pots settling by day 30",
        "failing test first", "PR in 24h", "max 2 open", "stalled 5d",
        "24 claims", "12 merge at median $150", "$1,800", "$1,350",
        "40 entries", "34 settle at $11.41", "$388",
        "$80 + $1,350 + $388", "$1,818",
        "8 merge (97% binomial)", "$1,200", "$900",
        "34 at $6.41", "$218", "$1,198",
    ]
    for figure in must_appear:
        assert figure in PLAN, figure


def main():
    verify()
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(PLAN + "\n")
    print(PLAN)
    print("chars:", len(PLAN))
    print("day30: $1818 (exact $1817.94)")
    print("floor: $1198 (exact $1197.94)")
    print("wrote:", out_path)


if __name__ == "__main__":
    main()
