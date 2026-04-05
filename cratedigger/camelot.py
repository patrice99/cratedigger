"""
Camelot Wheel — key compatibility scoring for DJ transitions.

The Camelot wheel is the circle of fifths repackaged for DJs.
Each key gets a number (1-12) and a letter (A=minor, B=major).
Compatible keys are adjacent on the wheel.

Spotify represents keys as:
  key  : int 0-11 (chromatic pitch class: 0=C, 1=C#, 2=D ... 11=B)
  mode : int 0=minor, 1=major
"""

from dataclasses import dataclass


# Full mapping: (spotify_key, spotify_mode) → (camelot_number, camelot_letter, key_name)
_SPOTIFY_TO_CAMELOT = {
    # Minor keys (A)
    (0,  0): (5,  "A", "C minor"),
    (1,  0): (12, "A", "C# minor"),
    (2,  0): (7,  "A", "D minor"),
    (3,  0): (2,  "A", "Eb minor"),
    (4,  0): (9,  "A", "E minor"),
    (5,  0): (4,  "A", "F minor"),
    (6,  0): (11, "A", "F# minor"),
    (7,  0): (6,  "A", "G minor"),
    (8,  0): (1,  "A", "Ab minor"),
    (9,  0): (8,  "A", "A minor"),
    (10, 0): (3,  "A", "Bb minor"),
    (11, 0): (10, "A", "B minor"),
    # Major keys (B)
    (0,  1): (8,  "B", "C major"),
    (1,  1): (3,  "B", "Db major"),
    (2,  1): (10, "B", "D major"),
    (3,  1): (5,  "B", "Eb major"),
    (4,  1): (12, "B", "E major"),
    (5,  1): (7,  "B", "F major"),
    (6,  1): (2,  "B", "F# major"),
    (7,  1): (9,  "B", "G major"),
    (8,  1): (4,  "B", "Ab major"),
    (9,  1): (11, "B", "A major"),
    (10, 1): (6,  "B", "Bb major"),
    (11, 1): (1,  "B", "B major"),
}


@dataclass
class CamelotKey:
    number: int        # 1-12
    letter: str        # "A" or "B"
    key_name: str      # e.g. "C major"

    def __str__(self):
        return f"{self.number}{self.letter}"


def from_spotify(key: int, mode: int) -> CamelotKey:
    """
    Convert Spotify key/mode integers to a CamelotKey.

    Args:
        key:  Spotify pitch class (0=C, 1=C#, ... 11=B)
        mode: 0=minor, 1=major

    Returns:
        CamelotKey with number, letter, and key name

    Example:
        from_spotify(0, 1)  →  CamelotKey(8, "B", "C major")
    """
    if (key, mode) not in _SPOTIFY_TO_CAMELOT:
        raise ValueError(f"Invalid Spotify key/mode: key={key}, mode={mode}")

    number, letter, key_name = _SPOTIFY_TO_CAMELOT[(key, mode)]
    return CamelotKey(number=number, letter=letter, key_name=key_name)


def wheel_distance(a: CamelotKey, b: CamelotKey) -> int:
    """
    Shortest distance between two keys on the Camelot wheel (1-12, circular).
    Ignores A/B — only measures the numeric distance around the clock.

    Example:
        distance between 11 and 1 = 2 (not 10)
    """
    diff = abs(a.number - b.number)
    return min(diff, 12 - diff)   # circular — wheel wraps around


def key_compatibility(a: CamelotKey, b: CamelotKey) -> float:
    """
    Score the harmonic compatibility of two keys (0.0 - 1.0).

    Scoring rules:
        Same number + same letter  → 1.0   perfect match
        Same number + diff letter  → 0.85  relative major/minor (share all notes)
        Distance of 1              → 0.75  adjacent key (dominant/subdominant)
        Distance of 2              → 0.4   possible but requires skill
        Distance of 3              → 0.25  energy shift technique
        Distance > 3               → 0.1   avoid

    Args:
        a: CamelotKey for track A
        b: CamelotKey for track B

    Returns:
        float compatibility score between 0.0 and 1.0
    """
    distance = wheel_distance(a, b)
    same_letter = a.letter == b.letter

    if distance == 0 and same_letter:
        return 1.0   # perfect — same key

    if distance == 0 and not same_letter:
        return 0.85  # relative major/minor — same 7 notes, different feel
                     # e.g. C major ↔ A minor

    if distance == 1:
        return 0.75  # adjacent on wheel — dominant or subdominant
                     # e.g. C major → G major (V) or F major (IV)

    if distance == 2:
        return 0.4   # two steps — works but needs careful mixing

    if distance == 3:
        return 0.25  # classic "energy shift" — dramatic but usable

    return 0.1       # too far apart — harmonic clash


def compatible_keys(key: CamelotKey) -> list[CamelotKey]:
    """
    Return all keys that are compatible with the given key (score >= 0.75).
    Useful for suggesting what keys to look for next.

    Returns keys in descending compatibility order.
    """
    results = []

    for (spotify_key, spotify_mode), (number, letter, key_name) in _SPOTIFY_TO_CAMELOT.items():
        candidate = CamelotKey(number=number, letter=letter, key_name=key_name)
        score = key_compatibility(key, candidate)
        if score >= 0.75 and str(candidate) != str(key):
            results.append((candidate, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return [(k, s) for k, s in results]
