"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document

# The line every reply in advice_threads starts with, e.g.
#   --- reply 3 (11 votes) ---
REPLY_HEADER = re.compile(r"^--- reply \d+ \(\d+ votes\) ---$", re.MULTILINE)


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in week 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_on_replies(text: str, chunk_size: int) -> list[str] | None:
    """
    Cut a long thread between replies, repeating the title on every piece.

    Returns None if this doesn't look like a thread, so the caller can fall
    back to fixed-size windows rather than hand back one oversized chunk.
    """
    starts = [m.start() for m in REPLY_HEADER.finditer(text)]
    if not starts:
        return None

    title = text[: starts[0]].strip()
    replies = [
        text[a:b].strip() for a, b in zip(starts, starts[1:] + [len(text)])
    ]

    pieces, current = [], []
    for reply in replies:
        if current and len("\n\n".join([title, *current, reply])) > chunk_size:
            pieces.append("\n\n".join([title, *current]))
            current = [reply]
        else:
            current.append(reply)
    if current:
        pieces.append("\n\n".join([title, *current]))
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    One whole thread per chunk.

    My corpus is `advice_threads`: 23 threads running 317 to 793 characters,
    so not one of them reaches the 1,000-character ceiling and every document
    comes out as a single chunk. That is the point — the starter's fixed-size
    windows split three of them, and every split was a duplicate tail of a
    document the first window already held whole, one of them two characters
    long.

    `chunk_size` is a ceiling rather than a target here. If a thread ever
    exceeds it, the split falls on a reply boundary and the `THREAD:` title
    goes on both halves, because the title is the only place the topic is
    stated — a chunk reading "16GB of RAM is the one number worth paying for"
    has lost that the question was about laptops.

    A document with no reply headers in it — another corpus, or a thread in a
    format this doesn't recognise — falls through to `fallback_split` so this
    never returns a chunk larger than the ceiling without saying so.
    """
    chunk_size = config.CHUNK_SIZE
    chunks: list[Chunk] = []

    for doc in documents:
        text = doc.text.strip()

        if len(text) <= chunk_size:
            pieces = [text]
        else:
            pieces = _split_on_replies(text, chunk_size)
            if pieces is None:
                # Overlap comes from config, which this strategy sets to 0.
                pieces = [c.text for c in fallback_split([doc], chunk_size)]

        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
