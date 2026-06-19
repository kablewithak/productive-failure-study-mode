# Research Mapping: Attempt First Mode

## Purpose

This document maps the research and BAG Learning context into product behaviour for **Productive Failure Study Mode**.

The core translation is simple:

```text
Research idea: problem solving before instruction
Product behaviour: attempt before explanation
Engineering behaviour: enforce the attempt gate in API and UI
```

## BAG Learning fit

BAG Learning is positioned around South African university study support: AI-supported notes, quizzes, tutoring, simplification, translation, and structured learning support. The platform context also emphasizes active retrieval practice, cognitive-load optimization, and grounded educational support.

Attempt First Mode fits that direction because it does not merely summarize notes. It forces the student to produce evidence of understanding before the AI explains.

The product extension is:

```text
Instead of Zazi explaining first, the system asks the student to attempt first.
```

## Student problem

Many students study by rereading, highlighting, asking AI for summaries, or asking for direct explanations. These behaviours can feel productive while hiding weak recall and shallow understanding.

The prototype targets that failure mode by requiring:

1. concept selection
2. pre-instruction challenge
3. student attempt
4. structured failure analysis
5. targeted consolidation
6. retrieval quiz
7. dashboard event

## Productive Failure basis

The Productive Failure paper describes a sequence where learners initially tackle problems targeting concepts they have not yet fully learned, followed by consolidation instruction. In the referenced Python-list study, the immediate learning outcome difference between Direct Instruction and Productive Failure was not the main win. The stronger product insight is that delayed retention and cognitive-load movement looked more promising for the Productive Failure condition.

Important translation constraint:

```text
The paper studies Python lists.
The product concept is not a Python tutor.
```

Python lists are a paper-aligned demonstration concept. The product mechanism is discipline-agnostic.

## Why multiple disciplines matter

The seeded concepts deliberately include:

- Law: offer and acceptance
- Commerce: break-even analysis
- Engineering: moments
- Programming: Python lists

This proves the interface is not tied to one subject. The shared abstraction is not the discipline; it is the learning event.

## Product behaviour mapping

| Research / product idea | Prototype behaviour |
|---|---|
| Problem solving before instruction | UI shows challenge before explanation |
| Visible attempt | Student submits free-text attempt and confidence |
| Failure as diagnostic signal | Backend assigns a failure label |
| Consolidation after struggle | Targeted explanation is returned after attempt |
| Retrieval practice | Quiz generated after consolidation |
| Learning-event evidence | Session persists and appears in dashboard |
| Safe learning support | Mock engine avoids assignment-completion framing |
| Scalable evaluation | Eval harness checks fixed diagnostic cases |

## What the prototype deliberately avoids

The prototype does not implement real cognitive-load measurement, wearable sensors, EEG/HRV collection, or real student outcome measurement.

It also does not claim that Productive Failure improves BAG Learning outcomes. That would require a controlled study, real users, real course contexts, and outcome metrics.

## Correct claim

This project demonstrates a production-shaped way to operationalize Productive Failure inside a BAG Learning-style study companion.

It proves the behaviour can be implemented with:

- typed backend contracts
- deterministic mock AI mode
- learning event persistence
- dashboard metrics
- eval harness checks
- browser-based learning flow

It does not prove real learning efficacy.
