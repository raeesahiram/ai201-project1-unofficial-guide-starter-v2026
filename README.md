# The Unofficial Guide

Raeesah Iram — corpus: `advice_threads`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none, because the grader can't
> read it.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Week 1

## What This Does

This answers questions about university life from `advice_threads` — 23
question-and-answer threads where students reply to each other about parking
permits, laundry timing, pass/fail deadlines, laptop specs and the rest of the
things nobody writes down officially. You ask a question, it finds the thread
that answers it, and it returns two or three sentences naming the file it used.

It's built for questions with one right answer — "how late can you declare
pass/fail?", "how many pages does the printing quota cover?" — not for open
questions like "what's the best dorm". If nothing in the 23 threads is close
enough to the question, it says it doesn't have enough information instead of
guessing, and it does that in two places: a distance cutoff before the model is
called, and an instruction in the prompt for the cases that get past it.

## Chunking Strategy

**Chunk size:** 1,000 characters — a ceiling, not a target
**Overlap:** 0

My 23 threads run 317 to 793 characters, so none of them reaches even the
starter's 800-character cutoff. The right number of chunks here is 23, one per
thread, and any splitting is damage rather than division. 1,000 is headroom
above the longest thread; if one ever exceeds it I'll split on reply boundaries
and repeat the `THREAD:` line, since the title is the only place the topic is
stated.

Overlap is 0 because the starter's 120 is what produced the junk. Its stride is
`800 - 120` = 680, so the three threads longer than that got a second window
duplicating a tail already indexed — one of them the two-character chunk `t.`.
Overlap exists to save a sentence cut in half; if I never cut mid-sentence,
there's nothing to save.

I considered one chunk per reply, since replies are 68–195 characters and
disagree with each other inside a thread. At 600/0 the corpus fragments to 40
chunks including a 32-character piece, and a reply cut from its title loses its
topic. That disagreement is real, but it belongs to retrieval and prompting,
not to the chunker.

<!-- Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

Printed with `python app.py chunks -n 5`. All five are whole threads — 23 chunks
from 23 documents, shortest 317 characters and longest 793.

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.
```

**Chunk 2** — source: `thread_first_gen.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.

--- reply 2 (41 votes) ---
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

--- reply 3 (16 votes) ---
Emergency fund for textbooks and travel exists and is not means-tested beyond a short form.
```

**Chunk 3** — source: `thread_laptop_specs.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: How much laptop do I actually need for CS courses?

--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.

--- reply 3 (12 votes) ---
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```

**Chunk 4** — source: `thread_office_hours_etiquette.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is it weird to go to office hours with no specific question?

--- reply 1 (44 votes) ---
No, and this is the single most common thing first years get wrong. 'I'm following the lectures but I don't feel like I understand the shape of it' is a completely normal thing to say.

--- reply 2 (29 votes) ---
They're usually empty. You are doing the instructor a favour by turning up.

--- reply 3 (18 votes) ---
If it helps, treat it as a standing appointment. Go every week for a month and it stops feeling like a thing.
```

**Chunk 5** — source: `thread_professor_email.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Do professors actually answer email?

--- reply 1 (21 votes) ---
Varies enormously. General rule I've found: if the syllabus states a response window, it's honoured. If it doesn't, assume 48 hours and don't panic before then.

--- reply 2 (33 votes) ---
Office hours are dramatically more effective than email for anything that takes more than two sentences to answer. They're also usually empty.

--- reply 3 (15 votes) ---
Empty office hours is the biggest unused resource here and I say that having wasted a year not going.
```

**Reading them:** all five stand alone — each opens with its `THREAD:` title, so the
topic is always stated, and none is a fragment. The weakness is chunks 4 and 5:
both answer "are office hours worth it?", and a query for that returns them
0.019 apart (0.539 and 0.558), so neither is clearly the answer. Chunk 1 is the
widest — four separate facts — and "How do I keep my bike from being stolen?"
retrieves it at 0.637, above the 0.6 cutoff, even though reply 4 answers it.

## Relevance Cutoff

**THRESHOLD: 0.6** — the number the starter ships, kept on purpose after measuring.

My five test questions and the five in `OUT_OF_SCOPE`, best distance each, at
`TOP_K = 3`:

| In corpus | | Out of corpus | |
|---|---|---|---|
| laptop RAM | 0.190 | ibuprofen dosage | 0.828 |
| parking lots | 0.293 | Rust for loop | 0.871 |
| pass/fail | 0.314 | diesel oil change | 0.930 |
| printing quota | 0.405 | capital of Mongolia | 0.948 |
| laundry timing | 0.446 | 1994 World Cup | 0.952 |

**0.190–0.446 against 0.828–0.952**: a gap of 0.382 with nothing in it, midpoint
0.637. Any cutoff between 0.45 and 0.82 scores 5 of 5 both ways, so these ten
questions don't actually choose the number for me.

So I tested eleven more. Six my documents *do* cover, phrased the way a student
would rather than in corpus vocabulary, and five that sound like student
questions but aren't in my documents at all:

| Covered, natural phrasing | | Not covered, plausible | |
|---|---|---|---|
| summer internships | 0.301 | parking ticket cost | 0.535 |
| roommate guests | 0.401 | gym closing time | 0.638 |
| winter coat | 0.470 | appealing a grade | 0.657 |
| older textbook edition | 0.604 | student ID pickup | 0.726 |
| bike theft | 0.637 | airport shuttle | 0.767 |
| essay extension | 0.788 | | |

**These two groups overlap, 0.535 to 0.788.** There is no cutoff that separates
real questions from unanswerable ones — only cutoffs that trade one error for
the other:

| Cutoff | My 5 pass | OUT_OF_SCOPE refused | Covered pass | Uncovered refused |
|---|---|---|---|---|
| 0.55 | 5/5 | 5/5 | 3/6 | 4/5 |
| **0.60** | **5/5** | **5/5** | **3/6** | **4/5** |
| 0.65 | 5/5 | 5/5 | 5/6 | 3/5 |
| 0.70 | 5/5 | 5/5 | 5/6 | 2/5 |

I picked 0.6 over 0.65 because of *which* questions each one gets wrong, not how
many. Of the three covered questions 0.6 refuses, two — the essay extension at
0.788 and the older textbook at 0.604 — retrieved the wrong thread anyway
(`first_gen` and `printing`, when the answers live in `late_work` and
`textbook_editions`). Refusing those is the right outcome, not a loss. Only bike
theft at 0.637 is a genuine false refusal. Moving to 0.65 would rescue it, but
would also admit the wrong-thread textbook question and the gym closing time —
trading one honest refusal for two chances to invent an answer.

The cost I'm accepting: "How much is a parking ticket?" lands at 0.535 and
passes. My parking thread never mentions tickets, so the model gets a relevant-
looking document and no answer in it. That's the failure mode I'd watch first in
week 2.

## Sample Answer

```
$ python app.py ask "How much RAM do students recommend for a laptop for CS courses?"

  (best distance 0.190, cutoff 0.6)

Students recommend 16GB of RAM for a laptop for CS courses.

Source: thread_laptop_specs.txt

Sources retrieved: thread_first_gen.txt, thread_laptop_specs.txt, thread_printing.txt

1 model calls this session, 650 tokens (624 in, 26 out)
```

Two lines are worth separating. `Source:` is the model's own citation, and it
names the one thread it used. `Sources retrieved:` is `app.py` printing all
`TOP_K = 3` chunks that came back, including `first_gen` at 0.711 and `printing`
at 0.717, which contributed nothing. Criterion 2 is satisfied by the second
line; the first is the one that's actually correct.

The answer is also the test of criterion 5 for this question. `thread_laptop_specs.txt`
contains a reply saying "I did two years on an 8GB machine and it was fine," and
the answer still comes back 16GB.

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

**1.** I asked Claude to rewrite the chunker after reading what the starter
actually produced. It found that the 2-character chunk came from the overlap,
not the chunk size — the stride is `800 - 120 = 680`, so the three threads
longer than that got a duplicate tail — and rewrote `split_documents` around
thread boundaries. It also dropped `TOP_K` from 5 to 3 without being asked, so I
checked ranks 4 and 5 against my own five questions before I kept that.

**2.** I asked it to draft acceptance criteria 4 and 5. Criterion 4 came back as
three checks in one sentence, pinned to "all 26 chunks", which stops meaning
anything as soon as the chunker changes, so I replaced it with one property: 23
chunks, each 300 to 800 characters. Its written reasons also ran three or four
paragraphs per section and I cut them all to two sentences.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Week 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     week 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. One chunk per thread, no fragments | 23 of 23 | 23/23 | 23/23 | 23/23 | MET |
| 5. The answer states the right fact | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

**Evidence for criteria 1, 2, and 5** — from
`results/run_2026-09-20_2321_before.md`, produced by
`run_eval.py::main` and `generate.py::answer_from_chunks`:

```text
You can declare a course pass/fail as late as week eight.

Sources: *thread_pass_fail.txt* and *thread_first_year_regret.txt*

The printing quota of $30 covers about 600 pages of black and white printing.

Source: thread_printing.txt

Students state that laundry is free (least busy) on Tuesday and Wednesday mornings in every building.

Source: thread_laundry_timing.txt

Students recommend 16GB of RAM for a laptop for CS courses.

Source: thread_laptop_specs.txt

The west parking lots sell out in about three days in August.

Source: thread_parking.txt
```

All five retrieved result sets included the corresponding answer thread, all
five answers contained the expected fact, and all five named a source.

**Evidence for criterion 3** — from
`results/run_2026-09-20_2321_before.md`, produced by
`run_eval.py::check_out_of_scope`:

```text
Produced by `run_eval.py::check_out_of_scope`, cutoff 0.6. Refused 5 of 5.

| What is the capital of Mongolia? | 0.948 | refused |
| How do I change the oil in a diesel engine? | 0.930 | refused |
| Who won the 1994 World Cup? | 0.952 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.828 | refused |
| How do I write a for loop in Rust? | 0.871 | refused |
```

**Evidence for criterion 4** — from `chunker.py::split_documents`, checked by
the `python app.py chunks -n 5` output already pasted above:

```text
All five are whole threads — 23 chunks from 23 documents, shortest 317 characters and longest 793.
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     week — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | All three runs retrieved a chunk from the thread containing the expected answer for all 5 questions, exceeding the target of 4 of 5. |
| 2 | Every answer names a source | MET | All 15 generated answers named at least one source, meeting the target of 5 of 5 in every run. |
| 3 | Gate stops out-of-corpus questions | MET | The deterministic gate refused all 5 out-of-scope questions in each reported run, exceeding the target of 4 of 5. |
| 4 | One chunk per thread, no fragments | MET | The chunker produced 23 whole-thread chunks, all between 300 and 800 characters, meeting the target exactly. |
| 5 | The answer states the right fact | MET | Every one of the 15 generated answers contained its question's expected string, exceeding the target of 4 of 5 in every run. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

I missed nothing: all five criteria met their original targets in all three
runs. The targets were somewhat safe, especially criterion 3: the five
out-of-scope questions were clearly unrelated to the corpus, and the gate
refused all five. I would tighten criterion 3 from 4 of 5 to 5 of 5, then use
plausible student questions that sound closer to the corpus as the test set.

## The Improvement

**What I changed:** I added an opt-in hybrid retrieval mode in
`store.py::search`. It combines the semantic ranking with BM25 keyword
ranking using reciprocal-rank fusion. The existing semantic index remains the
`default` variant; I built the same 23 chunks as the `hybrid` variant and ran
the evaluation with `--variant hybrid`. The run is recorded in
`results/run_2026-09-20_2332_after.md`.

**Why I picked it:** The diagnosis identified exact terms and numbers as the
most likely retrieval weakness, and this corpus contains terms such as `16GB`,
`600`, and `week eight` that keyword search can preserve when semantic search
smooths them into a broader meaning.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. One chunk per thread, no fragments | 23 of 23 | 23/23 | 23/23 | 23/23 | MET |
| 5. The answer states the right fact | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Real output from `results/run_2026-09-20_2332_after.md`:**

```text
How late in the term can you declare a course pass/fail?
     run 1: —  (best distance 0.314)
     run 2: —  (best distance 0.314)
     run 3: —  (best distance 0.314)

How much RAM do students recommend for a laptop for CS courses?
     run 1: —  (best distance 0.190)
     run 2: —  (best distance 0.190)
     run 3: —  (best distance 0.190)

Out-of-scope questions (the gate should refuse these):
     refused  (best distance 0.948)  What is the capital of Mongolia?
     refused  (best distance 0.918)  How do I write a for loop in Rust?
     -> gate refused 5 of 5
```

The dashes are because `scorer.py` does not exist yet; I judged the answers
against the `expects` strings in `questions.py`.

**Did it help?**

It did not change the criterion totals: both variants retrieved the answer
thread for all five test questions, all generated answers stated the expected
fact and named a source, and both refused all five obvious out-of-scope
questions. Hybrid did change some lower-ranked sources, but it did not fix the
known plausible question "How much is a parking ticket?": the parking thread
still ranked first at distance `0.535` and passed the `0.6` gate.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

The same parking-ticket false positive is still broken. I would add plausible
student questions like that one to the out-of-scope set and tune or redesign
the gate around them; I stopped here because hybrid search changed rankings
without changing the measured outcomes, so lowering the cutoff without new
evidence would risk refusing genuine questions.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
