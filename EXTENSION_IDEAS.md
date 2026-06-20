# Recommended Extensions — Ideas for Extra Time

Grounded in what actually broke in `pythagoras.py` / `fourier_series.py` and
how the fixing process went, here are the extensions I'd prioritize, roughly
in order of value-per-effort.

## 1. Turn the critique into automated tests, not just eyeballed screenshots
Right now, finding bugs meant rendering a video and manually looking at
frames. That doesn't scale and won't catch regressions. Add a small
assertion layer that runs against any constructed scene *before* rendering:
- assert every mobject's bounding box is within `config.frame_width/height`
  (catches the overflow bug)
- assert no two "important" mobjects' bounding boxes overlap beyond a
  tolerance (catches the label-collision bug)
- for geometry scenes, assert measured side lengths match the intended
  `a, b, c` within floating-point tolerance (catches the
  not-actually-attached-squares bug)

This is the single highest-leverage addition: it converts "critical
analysis" from a one-time manual write-up into a regression suite the team
can run on every new LLM-generated scene going forward.

## 2. Multi-model comparison harness
Run the *same* prompt through Gemini, Claude, and GPT-4o/5, save each
model's raw code + rendered output side by side, and score them against the
same rubric (geometric correctness, layout, color contrast, pacing, code
cleanliness). This is a natural extension of "critically evaluate the
quality of generated code" — instead of one data point, you get a real
comparison, which is much more interesting and defensible as a finding.

## 3. Self-correcting feedback loop
Feed the rendered screenshot back into a vision-capable Gemini call along
with the specific bugs found (e.g. "the c² square overlaps the title — fix
it"), and let the model attempt its own repair. Track how many iterations
it takes to converge to a bug-free render. This turns the one-shot
"generate once" pipeline into an agentic generate → render → critique →
repair loop, which is both a more realistic workflow and a more interesting
thing to measure ("how many rounds does each model need?").

## 4. Generalize the scenes instead of hardcoding examples
Make `pythagoras_corrected.py` accept any `a, b, c` (already mostly true
after the fix) and `fourier_series.py` accept an arbitrary harmonic count
and waveform type (square, sawtooth, triangle) via CLI args or a small
config dict. Useful both as a stronger demo and as a better regression-test
target for #1 — a single hardcoded example can hide bugs that only show up
at other parameter values.

## 5. CI pipeline that renders on every push
A GitHub Actions workflow that installs Manim + ffmpeg, renders every scene
in the repo on each push/PR, and uploads the resulting `.mp4`/`.png` as a
build artifact (or posts a thumbnail as a PR comment). Catches "looks right
in the code, breaks on render" regressions automatically — exactly the
category of bug that motivated this whole assignment.

## 6. Narration / voiceover
Use `manim-voiceover` (or simple TTS + `add_sound`) to narrate each
construction step ("Here we shade the square built on side a..."). Turns
the animations into something actually usable in a classroom rather than a
silent code-quality demo.

## 7. A small "LLM + Manim pitfalls" cheat sheet
Both bugs in this assignment trace back to a handful of recurring root
causes: hand-tuned magic-number offsets instead of vector-derived
positions, `Transform` calls applied to throwaway copies instead of the
on-screen mobject, and missing `add_coordinates()`/scale-to-fit calls.
Writing these up as a short internal reference (not a generic Manim
tutorial, but specifically "patterns we've seen LLMs get wrong") would save
the team time on every future prompt-and-fix cycle, since the same handful
of bug classes are likely to recur.

## If only doing one thing
**#1 (automated layout/geometry assertions)** — it's the cheapest of these
to build, and it directly upgrades the deliverable the assignment already
asks for (a critical analysis) from a one-time manual write-up into
something reusable for every future scene the team generates.
