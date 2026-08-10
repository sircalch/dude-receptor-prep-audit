# SoftwareX: assessment and submission-readiness record

**Status:** pre-submission assessment only. This file is not a submission and
does not imply acceptance, payment, or a decision by SoftwareX.

## Why SoftwareX is a plausible candidate

SoftwareX describes its scope as research software across disciplines and asks
for a concise descriptive paper supported by publicly available, reusable
software. This repository supplies a public MIT-licensed implementation, a
versioned Zenodo archive, reproducible protocols, versioned inputs summaries,
and deterministic result figures. The proposed paper is a description of the
software and its documented evidence workflow; it is not a biological or
clinical study.

The proposed contribution is narrow and should be represented that way. The
software records strict receptor-preparation attempts, evidence tables, and
reference-pose recovery under frozen inputs. The DUD-E audit and the BRAF and
KIF11 runs are reference implementations and reproducibility examples. They
are not evidence of broad adoption, benchmarking superiority, binding affinity,
or biological activity.

## Public materials already available

- Source repository: https://github.com/sircalch/dude-receptor-prep-audit
- Frozen software-and-evidence release: https://doi.org/10.5281/zenodo.21866318
- License: MIT.
- User-facing baseline command and strict policy: `README.md` and
  `protocol/AUDIT-PROTOCOL.md`.
- Reproducible summaries: `results/`, `reports/`, and deterministic SVG
  figures under `reports/figures/`.
- Versioned authorship and citation metadata: `CITATION.cff`.

## Requirement-to-evidence mapping

| SoftwareX expectation | Evidence or action |
| --- | --- |
| Research software with a concise descriptive article | Use the journal-neutral manuscript as a scientific base, then transfer it to the current official SoftwareX template. |
| Open, inspectable software and supporting material | Public GitHub repository and Zenodo v0.2.0 archive. Verify that the exact release and repository links remain accessible on the day of submission. |
| Clear operation and reuse conditions | README gives a baseline invocation; strict scope and input/output boundaries are documented in the protocol. The manuscript must state the required local source files and external tools. |
| Evidence of the described behavior | Versioned CSV tables, protocol records, command configurations, and deterministic figures. |
| Transparent generative-AI disclosure | Include a journal-compliant declaration naming OpenAI Codex (GPT-5), its assistance roles, and the authors' responsibility for verification and final content. Do not conceal use or attempt to evade detection. |
| Authorship, conflicts, funding, and availability statements | The current draft contains provisional CRediT roles, no competing interests, no external funding, and code/data availability text. Every author must check and approve these before submission. |

## Claims that must remain excluded

The manuscript and cover letter must not claim any of the following:

- validation of docking scores, affinity, enrichment, biological activity,
  efficacy, safety, or therapeutic effect;
- a general solution for receptor preparation outside the declared toolchain
  and strict protocol;
- external uptake, community impact, or performance superiority not supported
  by evidence;
- experimental confirmation of the BRAF or KIF11 calculations.

The two frozen docking runs are retained only as computational reference-pose
recovery examples, with all poses and methodological limitations reported.

## Remaining author decisions before a submission can be prepared

1. Confirm that each author accepts the final author order, affiliations,
   CRediT statement, and corresponding-author role.
2. Decide whether to pursue SoftwareX after reviewing its article-processing
   charge and any applicable waiver route. No fee should be incurred without
   explicit author approval.
3. Download the current official SoftwareX article template immediately before
   formatting, because journal templates and submission instructions can
   change.
4. Conduct a human, line-by-line review of the final manuscript, figures,
   captions, references, code availability, and AI disclosure.
5. Submit only the final author-approved files through the journal portal.

## Pre-submission checklist

- [x] Public repository and permanent versioned archive available.
- [x] DOI, author identifiers, license, and availability links recorded.
- [x] Evidence boundaries and computational limitations stated.
- [x] Bibliographic sources verified against primary or official sources.
- [x] Provisional transparent AI-assistance declaration drafted.
- [ ] All authors confirm final text and contribution roles.
- [ ] Current journal template and instructions applied.
- [ ] APC/waiver decision documented by the authors.
- [ ] Final package independently proofread by the authors.

## Sources consulted for this assessment

- SoftwareX, *Guide for authors*:
  https://www.sciencedirect.com/journal/softwarex/publish/guide-for-authors
- Elsevier, *Generative AI policies for journals*:
  https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
- Elsevier, *Pricing and funding options*:
  https://www.elsevier.com/about/policies-and-standards/pricing

