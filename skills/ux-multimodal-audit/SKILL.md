# UX and multimodal audit

## Procedure

1. Inventory the supplied image, screen capture, audio, or video: filename,
   format, visible duration/pages, resolution or recording context when known,
   and gaps. Verify authorization and remove personal data before analysis.
2. Confirm that available IDE/model tools can actually inspect the format. If
   video, audio, or image content is inaccessible, do not claim to have
   inspected it; ask for an accessible export or report the limitation.
3. Analyze only observable content. For each finding cite the exact screen,
   visible component, image region, timestamp/time range, or audible segment.
   Keep observed behavior separate from interpretation and recommendation.
4. Audit the relevant journey: user goal/context, entry point, information
   hierarchy, comprehension, interaction affordances, errors, accessibility
   signals, trust/privacy cues, pricing/eligibility disclosures, and
   hand-off/completion. Include what cannot be inferred from a static image or
   recording, such as backend behavior, unobserved states, or user intent.
5. Record each reusable observation in `state/evidence_graph.json` as a
   sourced fact only when the material directly shows it, with the exact
   locator and confidence. Interpretations belong in hypotheses; do not claim
   usability or prevalence from screenshots alone.
6. Check communication promises against the exact product UI and authoritative
   product evidence. Note mismatches or missing disclosures without assuming
   that the screen is representative of every user.

## Stop for the user

Pause if content contains personal data or restricted material, if the
required modality cannot be inspected, or if the sample/context is too limited
to support a decision-changing conclusion.

## Output

Create a concise audit with an evidence locator per finding, observation,
interpretation, severity/impact rationale, uncertainty, and suggested test.
Report explicitly what the supplied material does not show.
