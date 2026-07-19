#!/usr/bin/env python3
"""Vendor a curated GloVe 50-d subset for in-browser semantic search (P2-D2 / R11).

Source: Stanford NLP's pre-trained GloVe vectors ("Pre-trained word vectors are
made available under the Public Domain Dedication and License" —
github.com/stanfordnlp/GloVe, re-verified 2026-07-19). The 6B set (Wikipedia
2014 + Gigaword 5, uncased) is distributed only as an ~822 MB zip, so this
script fetches **just the `glove.6B.50d.txt` member** with HTTP range requests
(stdlib only) from the official mirrors, streams it, and stops as soon as the
curated vocabulary below is found (~10–20 MB transferred, not 822 MB).

The vocabulary is curated for M6 Ch13's teaching demos: analogy families
(king−man+woman), country↔capital pairs, and everyday semantic clusters —
sized so the CSV respects the ≤~50 KB vendoring rule (P1-D8) at 3-decimal
precision (plenty for cosine-similarity teaching).

Determinism: output rows follow VOCAB order, values formatted `%.3f`.
Re-running must reproduce the committed CSV byte-for-byte.

Run from the repo root:
    python infra/datasets/make_glove_sample.py
"""
from __future__ import annotations

import io
import urllib.request
import zipfile
from pathlib import Path

MEMBER = "glove.6B.50d.txt"
URLS = [
    # Official HF mirror first (better range/CDN support), Stanford second.
    "https://huggingface.co/stanfordnlp/glove/resolve/main/glove.6B.zip",
    "https://nlp.stanford.edu/data/wordvecs/glove.6B.zip",
]
OUT = Path("modules/06-vision-sequences/data/glove-50d-sample.csv")
DIMS = 50

# fmt: off
VOCAB = [
    # analogy families (gender / family)
    "king", "queen", "man", "woman", "prince", "princess", "boy", "girl",
    "father", "mother", "brother", "sister", "uncle", "aunt", "husband", "wife",
    # country <-> capital pairs
    "france", "paris", "italy", "rome", "spain", "madrid", "germany", "berlin",
    "japan", "tokyo", "england", "london", "russia", "moscow", "india", "delhi",
    "china", "beijing", "egypt", "cairo",
    # animals
    "dog", "cat", "puppy", "kitten", "horse", "cow", "sheep", "lion", "tiger",
    "elephant", "mouse", "fish", "bird", "eagle", "shark", "whale",
    # food & drink
    "apple", "banana", "orange", "grape", "mango", "bread", "cheese", "butter",
    "rice", "pasta", "pizza", "burger", "coffee", "tea", "milk", "juice",
    "sugar", "salt",
    # vehicles
    "car", "truck", "bus", "train", "plane", "ship", "boat", "bicycle",
    "motorcycle",
    # emotions
    "happy", "sad", "angry", "afraid", "love", "hate", "joy", "fear",
    # technology
    "computer", "software", "internet", "phone", "keyboard", "screen",
    "robot", "machine",
    # nature
    "sun", "moon", "star", "sky", "rain", "snow", "wind", "storm", "river",
    "mountain", "ocean", "forest", "tree", "flower",
    # professions
    "doctor", "nurse", "teacher", "student", "engineer", "scientist",
    "lawyer", "judge", "actor", "actress",
    # qualities & verb forms (comparatives, tense analogies)
    "big", "small", "fast", "slow", "hot", "cold", "good", "bad", "strong",
    "weak", "walked", "walking", "swam", "swimming", "ran", "running",
]
# fmt: on


class HTTPRangeFile(io.RawIOBase):
    """Read-only seekable file over HTTP Range requests (for zipfile)."""

    def __init__(self, url: str, chunk: int = 4 * 1024 * 1024):
        self.url = url
        self.chunk = chunk
        self.pos = 0
        self.transferred = 0
        self.size = self._probe_size()
        self._buf = b""
        self._buf_start = 0

    def _request(self, start: int, end: int) -> bytes:
        req = urllib.request.Request(
            self.url, headers={"Range": f"bytes={start}-{end}"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status != 206:
                raise OSError(f"server ignored Range request (HTTP {resp.status})")
            data = resp.read()
        self.transferred += len(data)
        return data

    def _probe_size(self) -> int:
        req = urllib.request.Request(self.url, headers={"Range": "bytes=0-0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status != 206:
                raise OSError(f"no Range support (HTTP {resp.status})")
            content_range = resp.headers.get("Content-Range", "")
            resp.read()
        return int(content_range.rsplit("/", 1)[1])

    # io plumbing -----------------------------------------------------------
    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = 0) -> int:
        self.pos = {0: offset, 1: self.pos + offset, 2: self.size + offset}[whence]
        return self.pos

    def read(self, n: int = -1) -> bytes:
        if n < 0:
            n = self.size - self.pos
        n = min(n, self.size - self.pos)
        if n <= 0:
            return b""
        in_buf = self._buf_start <= self.pos and (
            self.pos + n <= self._buf_start + len(self._buf)
        )
        if not in_buf:
            fetch_len = max(n, self.chunk)
            end = min(self.pos + fetch_len, self.size) - 1
            self._buf = self._request(self.pos, end)
            self._buf_start = self.pos
        off = self.pos - self._buf_start
        out = self._buf[off : off + n]
        self.pos += len(out)
        return out


def fetch_vectors(url: str) -> dict[str, list[float]]:
    wanted = set(VOCAB)
    found: dict[str, list[float]] = {}
    remote = HTTPRangeFile(url)
    with zipfile.ZipFile(remote) as zf, zf.open(MEMBER) as member:
        for line_no, raw in enumerate(io.TextIOWrapper(member, encoding="utf-8"), 1):
            parts = raw.rstrip("\n").split(" ")
            word = parts[0]
            if word in wanted and word not in found:
                vec = [float(x) for x in parts[1:]]
                if len(vec) != DIMS:
                    raise ValueError(f"{word}: expected {DIMS} dims, got {len(vec)}")
                found[word] = vec
                if len(found) == len(wanted):
                    print(
                        f"all {len(found)} words found by line {line_no:,} "
                        f"({remote.transferred / 1e6:.1f} MB transferred)"
                    )
                    return found
    missing = sorted(wanted - set(found))
    raise ValueError(f"words not in {MEMBER}: {missing}")


def main() -> int:
    last_err: Exception | None = None
    vectors = None
    for url in URLS:
        try:
            print(f"fetching from {url.split('/')[2]} …")
            vectors = fetch_vectors(url)
            break
        except Exception as e:  # noqa: BLE001 - try the next mirror
            last_err = e
            print(f"  mirror failed: {e}")
    if vectors is None:
        raise SystemExit(f"all mirrors failed; last error: {last_err}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    header = "word," + ",".join(f"d{i}" for i in range(DIMS))
    lines = [header]
    for word in VOCAB:
        lines.append(word + "," + ",".join(f"{v:.3f}" for v in vectors[word]))
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"WROTE {OUT} ({len(VOCAB)} words x {DIMS}d, {size_kb:.1f} KB)")
    if size_kb > 55:
        print("WARN: sample exceeds the ~50 KB vendoring rule — trim VOCAB")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
