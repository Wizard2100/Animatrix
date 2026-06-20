# Critical Analysis — `pythagoras.py` (Pythagorean Theorem Scene)

The scene was generated, run with `manim -ql pythagoras.py PythagoreanTheorem`, and
inspected frame-by-frame. Below are five concrete shortcomings found in the
actual rendered output (see `pythagoras_frame_overlap.png` and
`pythagoras_frame_final.png`), not hypothetical ones.

## 1. Geometrically incorrect square placement
**Issue:** The three squares are positioned with ad-hoc `move_to()` / `align_to()`
calls rather than being derived from the triangle's actual edge vectors. The
square meant to sit on the hypotenuse is not rotated to lie flush against the
hypotenuse line at all — it just floats above and to the right of the triangle.
**Why it matters:** The entire pedagogical point of this animation is showing
that the *areas built on the sides* relate to each other. If the squares
aren't actually attached to their corresponding edges, the "proof" is visually
meaningless — a viewer can't see that the square's side **is** the triangle's
side.
**Fix:** Compute each square's position and rotation directly from the
triangle's vertices, e.g. take the edge vector, rotate the square by the
edge's angle, and anchor one of the square's sides exactly onto that edge
(`Square().rotate(angle).move_to(edge_midpoint + outward_normal * side/2)`),
rather than using hand-placed offsets.

## 2. Off-screen overflow
**Issue:** The square on side `b` (green, area `b²`) extends past the bottom
edge of the frame — its `b²` label is only half-visible in the final frame.
**Why it matters:** A label the viewer can't fully read defeats the purpose of
labeling it. This is a basic layout bug that's easy to miss when only reading
the code, but obvious the moment you render it.
**Fix:** After building the full diagram (triangle + 3 squares + labels),
call `VGroup(*everything).move_to(ORIGIN)` and scale-to-fit with
`.scale_to_fit_height(config.frame_height - 1)` before playing any
animations, so the whole composition is guaranteed to fit inside the frame.

## 3. Overlapping, simultaneously-illegible text
**Issue:** In the final frame, the equation `a² + b² = c²` and the numeric
version `3² + 4² = 5² → 9 + 16 = 25` are stacked so closely that they overlap
the green square *and* each other, and partially overlap the leftover `b`
side-label.
**Why it matters:** Two pieces of text occupying the same pixels means the
viewer can read neither one cleanly — exactly the moment that should be the
animation's "payoff" (the identity confirmed with real numbers) is the least
legible part of the video.
**Fix:** Use `.arrange(DOWN, buff=0.4)` to stack the symbolic and numeric
equations with guaranteed spacing, and `FadeOut` the side-label `b` (or move
it out of the way) before writing the final equation in that same region.

## 4. Hardcoded values that only work for this one triangle
**Issue:** Square placement uses literal hand-tuned numeric offsets such as
`LEFT * (a/2)`, `RIGHT * 2.5 + UP * 1.5`, mixed with the variables `a`, `b`,
`c`. The `2.5` and `1.5` constants are "magic numbers" tuned by eye for the
3-4-5 case and aren't derived from `a`, `b`, or `c` at all.
**Why it matters:** Change `a`, `b`, `c` to a different right triangle (e.g.
5-12-13) and the layout breaks, because the constants don't scale with the
triangle. Code that looks parameterized (it uses variables `a`/`b`/`c`) but
silently depends on un-derived constants is a common, easy-to-miss flaw in
LLM-generated geometry code.
**Fix:** Replace every magic-number offset with an expression computed from
the triangle's vertices/edge vectors and side lengths so the scene is
correct for *any* valid `a`, `b`, `c`.

## 5. A Transform animation that doesn't do what it appears to
**Issue:** The closing animation is:
```python
self.play(Transform(equation.copy(), numeric), Write(numeric))
```
This transforms a *throwaway, never-added-to-scene* copy of `equation` into
`numeric`, while simultaneously `Write`-ing `numeric` directly. The
`Transform` call has no visible effect (its target was never added to the
scene), and the original `equation` mobject is left untouched on screen.
**Why it matters:** The code runs without error and *looks* like it morphs
the symbolic equation into the numeric one — but it doesn't. This is exactly
the kind of subtly-wrong animation logic that passes a quick code read but
fails on actual viewing, and it's a common failure mode of LLM-written Manim
code: APIs are used correctly in isolation but the overall animation intent
isn't achieved.
**Fix:** `self.play(Transform(equation, numeric))` — transform the actual
on-screen mobject, and drop the redundant `Write(numeric)` call.

## Other minor notes
- `Polygon` is imported via the `from manim import *` wildcard import along
  with everything else in the library, even though only a handful of classes
  are used — harmless here, but worth narrowing in production code for
  readability.
- There is no final `self.wait()` long enough for a viewer to actually read
  the numeric identity before the scene presumably ends/loops in a larger
  video — 2 seconds is a minimum, not a comfortable reading pace for new
  viewers.
