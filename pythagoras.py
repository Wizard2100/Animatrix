"""
pythagoras.py

Manim Community Edition scene that visually proves the Pythagorean Theorem
using a 3-4-5 right triangle: squares are built on each side, shaded, and
the algebraic identity a^2 + b^2 = c^2 is shown with the matching numbers.

Render with:
    manim -ql pythagoras.py PythagoreanTheorem      (fast draft, 480p)
    manim -qh pythagoras.py PythagoreanTheorem      (high quality, 1080p)
"""

from manim import *


class PythagoreanTheorem(Scene):
    def construct(self):
        # ---- hardcoded side lengths (3-4-5 triangle) ----
        a = 3
        b = 4
        c = 5

        title = Text("The Pythagorean Theorem", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # ---- build the right triangle ----
        A = ORIGIN
        B = ORIGIN + RIGHT * b
        C = ORIGIN + UP * a

        triangle = Polygon(A, B, C, color=WHITE, stroke_width=4)
        triangle.move_to(ORIGIN + DOWN * 0.5)

        self.play(Create(triangle))
        self.wait(0.5)

        # ---- labels for the sides ----
        label_a = Text("a", font_size=30).next_to(triangle, LEFT, buff=0.3)
        label_b = Text("b", font_size=30).next_to(triangle, DOWN, buff=0.3)
        label_c = Text("c", font_size=30)
        label_c.move_to(triangle.get_center() + UP * 0.3 + RIGHT * 0.6)

        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait(1)

        # ---- square on side a (left, vertical side) ----
        square_a = Square(side_length=a)
        square_a.set_fill(BLUE, opacity=0.5)
        square_a.set_stroke(BLUE, width=2)
        square_a.move_to(triangle.get_vertices()[0] + LEFT * (a / 2))
        square_a.align_to(triangle, DOWN)

        # ---- square on side b (bottom, horizontal side) ----
        square_b = Square(side_length=b)
        square_b.set_fill(GREEN, opacity=0.5)
        square_b.set_stroke(GREEN, width=2)
        square_b.move_to(triangle.get_vertices()[0] + DOWN * (b / 2))
        square_b.align_to(triangle, LEFT)

        # ---- square on side c (hypotenuse) ----
        square_c = Square(side_length=c)
        square_c.set_fill(RED, opacity=0.5)
        square_c.set_stroke(RED, width=2)
        square_c.move_to(triangle.get_vertices()[2] + RIGHT * 2.5 + UP * 1.5)

        self.play(FadeIn(square_a), FadeIn(square_b), FadeIn(square_c))
        self.wait(1)

        area_a = Text("a²", font_size=28).move_to(square_a.get_center())
        area_b = Text("b²", font_size=28).move_to(square_b.get_center())
        area_c = Text("c²", font_size=28).move_to(square_c.get_center())

        self.play(Write(area_a), Write(area_b), Write(area_c))
        self.wait(1)

        # ---- algebraic identity ----
        equation = Text("a² + b² = c²", font_size=40)
        equation.to_edge(DOWN)
        self.play(Write(equation))
        self.wait(1)

        numeric = Text(f"{a}² + {b}² = {c}²   →   {a*a} + {b*b} = {c*c}", font_size=36)
        numeric.next_to(equation, UP)
        self.play(Transform(equation.copy(), numeric), Write(numeric))
        self.wait(2)
