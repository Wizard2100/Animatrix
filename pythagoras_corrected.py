"""
pythagoras_corrected.py

A corrected version of the LLM-generated pythagoras.py scene. This file
fixes the 5 issues documented in critical_analysis.md:

  1. Squares are now built geometrically from the triangle's actual edge
     vectors (rotated to lie flush against each edge) instead of
     hand-placed offsets -> works for ANY right triangle, not just 3-4-5.
  2. The whole diagram is scaled/positioned to guarantee it fits inside
     the visible frame -> no more off-screen overflow.
  3. The equation block is built as a properly arranged VGroup with
     buffered spacing and placed in a dedicated region below the
     diagram -> no more overlapping text.
  4. No hardcoded "magic number" offsets (e.g. RIGHT * 2.5 + UP * 1.5) -
     every position is derived from `a`, `b`, `c`.
  5. The broken Transform(equation.copy(), numeric) call is replaced with
     a correct Transform(equation, numeric) that actually animates the
     symbolic equation turning into the numeric one.

Render with:
    manim -ql pythagoras_corrected.py PythagoreanTheoremCorrected
    manim -qh pythagoras_corrected.py PythagoreanTheoremCorrected
"""

from manim import *
import numpy as np


def square_on_edge(p1: np.ndarray, p2: np.ndarray, away_from: np.ndarray) -> Polygon:
    """
    Build a Polygon square whose first side is the segment p1->p2, extruded
    outward (away from `away_from`, typically the triangle's centroid) by
    a distance equal to |p1 - p2|.

    This makes the square geometrically attached to the edge for ANY
    triangle -- no hardcoded offsets needed.
    """
    edge_vec = p2 - p1
    side_length = np.linalg.norm(edge_vec)
    edge_dir = edge_vec / side_length

    # 90-degree rotation of the edge direction (in the XY plane) gives a
    # vector perpendicular to the edge.
    normal = np.array([-edge_dir[1], edge_dir[0], 0])

    # Make sure `normal` points AWAY from `away_from` (e.g. the triangle's
    # interior), not into it.
    midpoint = (p1 + p2) / 2
    if np.dot(normal, midpoint - away_from) < 0:
        normal = -normal

    p3 = p2 + normal * side_length
    p4 = p1 + normal * side_length

    return Polygon(p1, p2, p3, p4)


class PythagoreanTheoremCorrected(Scene):
    def construct(self):
        # ---- side lengths (still a 3-4-5 triangle, but every position
        #      below is derived from a/b/c, so changing these three
        #      numbers to any other valid right triangle just works) ----
        a = 3
        b = 4
        c = 5

        title = Text("The Pythagorean Theorem", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)

        # ---- the right triangle, right angle at A ----
        A = np.array([0.0, 0.0, 0.0])
        B = np.array([b, 0.0, 0.0])
        C = np.array([0.0, a, 0.0])
        centroid = (A + B + C) / 3

        triangle = Polygon(A, B, C, color=WHITE, stroke_width=4)

        # ---- squares, built exactly on each edge, outward from the
        #      triangle's centroid (this is the core geometry fix) ----
        square_a = square_on_edge(A, C, centroid)  # on leg a
        square_a.set_fill(BLUE, opacity=0.6).set_stroke(BLUE, width=2)

        square_b = square_on_edge(B, A, centroid)  # on leg b
        square_b.set_fill(GREEN, opacity=0.6).set_stroke(GREEN, width=2)

        square_c = square_on_edge(C, B, centroid)  # on hypotenuse c
        square_c.set_fill(RED, opacity=0.6).set_stroke(RED, width=2)

        # ---- side labels, positioned from the actual edge midpoints
        #      (not hardcoded pixel offsets) ----
        out_a = (square_a.get_center() - triangle.get_center())
        out_a = out_a / np.linalg.norm(out_a)
        label_a = Text("a", font_size=30, color=BLUE).move_to(
            (A + C) / 2 + out_a * 0.4
        )

        out_b = (square_b.get_center() - triangle.get_center())
        out_b = out_b / np.linalg.norm(out_b)
        label_b = Text("b", font_size=30, color=GREEN).move_to(
            (A + B) / 2 + out_b * 0.4
        )

        out_c = (square_c.get_center() - triangle.get_center())
        out_c = out_c / np.linalg.norm(out_c)
        label_c = Text("c", font_size=30, color=RED).move_to(
            (B + C) / 2 + out_c * 0.4
        )

        area_a = Text("a²", font_size=28).move_to(square_a.get_center())
        area_b = Text("b²", font_size=28).move_to(square_b.get_center())
        area_c = Text("c²", font_size=28).move_to(square_c.get_center())

        # ---- group everything, then scale + position to GUARANTEE it
        #      fits inside the visible frame, leaving room below for the
        #      equation block (fixes the overflow bug) ----
        diagram = VGroup(
            triangle, square_a, square_b, square_c,
            label_a, label_b, label_c, area_a, area_b, area_c,
        )
        diagram.scale_to_fit_height(4.2)
        diagram.next_to(title, DOWN, buff=0.6)

        self.play(Create(triangle))
        self.wait(0.5)
        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait(1)
        self.play(FadeIn(square_a), FadeIn(square_b), FadeIn(square_c))
        self.wait(1)
        self.play(Write(area_a), Write(area_b), Write(area_c))
        self.wait(1)

        # ---- algebraic identity, arranged as a clean stacked block
        #      below the diagram with guaranteed spacing (fixes the
        #      overlapping-text bug) ----
        equation = Text("a² + b² = c²", font_size=40)
        numeric = Text(
            f"{a}² + {b}² = {c}²   →   {a*a} + {b*b} = {c*c}", font_size=36
        )

        equation.next_to(diagram, DOWN, buff=0.5)
        self.play(Write(equation))
        self.wait(1)

        numeric.move_to(equation)  # numeric will occupy the same slot
        self.play(Transform(equation, numeric))  # correct, visible transform
        self.wait(2)
