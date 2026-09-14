# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in week 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next week costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, one of the retrieved chunks contains that
question's `expects` string from `questions.py`, matched as a case-insensitive
substring.

**Why this target:**

I picked 4 of 5 because of the laptop question: it's the only one of my five
whose answer is argued across replies rather than stated once — reply 1 says
16GB, reply 3 spends most of its length on an 8GB machine that was fine before
conceding "16 is the answer" — so it's the one where a chunk boundary could
return the anecdote without the conclusion. I match the `expects` string rather
than judging "contains the answer" because I couldn't score that wording the
same way twice on that same question.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

I picked every answer rather than 4 of 5 because this one is either working or
it isn't: `ask_pipeline` builds the source list from the retrieved chunks and
every chunk carries its filename, so a missing source would mean an answer
produced from zero chunks, which the gate refuses before it can happen. What it
doesn't check is whether the source named is the one the answer came from —
with `TOP_K = 5` over 26 chunks, a fifth of my corpus is listed under every
answer, and that's what I'd revise this into in week 2.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**

My five test questions measured 0.190 to 0.446 and the five `OUT_OF_SCOPE` ones
0.787 to 0.930, so the 0.6 cutoff sits in a 0.34-wide gap with nothing in it.
I kept 4 of 5 rather than raising it to 5 of 5 because those five are
unrealistically clean — "What is the capital of Mongolia?" shares no vocabulary
with a corpus about parking permits, and the questions that will really test
this gate are ones that sound like student questions but aren't in my documents,
like "how much is a parking ticket".

---

## 4. One chunk per thread, no fragments

Every chunk is one whole thread: 23 chunks from 23 documents, each between 300
and 800 characters.

**Why this target:**

I picked 300 and 800 because they're my corpus's actual floor and ceiling — the
shortest thread is 317 characters and the longest 793 — so anything outside that
range isn't a whole thread. I picked 23 rather than accepting today's 26 because
the three extra chunks are duplicate tails the 680-character stride cut off
documents already indexed whole, and one of them is 2 characters long.

---

## 5. The answer states the right fact

For at least 4 of my 5 test questions, the answer the system returns contains
that question's `expects` string from `questions.py`, matched as a
case-insensitive substring.

**Why this target:**

Nothing else in these five checks whether the answer is *right* — the system
could pass 1, 2 and 3 and still tell a student the printing quota is 300 pages
with a correct source printed underneath. I picked 4 of 5 because the laptop
question is the one place in my corpus where the right answer means taking a
side in an argument: the model has to read "I did two years on an 8GB machine
and it was fine" and still say 16GB.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     WEEK 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in week 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
