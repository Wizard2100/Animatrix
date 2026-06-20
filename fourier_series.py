"""
fourier_series.py

Manim Community Edition scene that demonstrates how a square wave is built
up by summing sine harmonics (Fourier series). Shows the first 5 odd
harmonics (n = 1, 3, 5, 7, 9), each in a different colour, and the
cumulative partial sum updating term by term.

    f(x) ~ (4/pi) * sum_{n=1,3,5,7,9} sin(n x) / n

Render with:
    manim -ql fourier_series.py FourierSeries      (fast draft, 480p)
    manim -qh fourier_series.py FourierSeries      (high quality, 1080p)
"""

from manim import *
import numpy as np


class FourierSeries(Scene):
    def construct(self):
        title = Text("Fourier Series: Building a Square Wave", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            axis_config={"include_tip": False},
        )
        axes.move_to(ORIGIN)

        self.play(Create(axes))
        self.wait(0.5)

        # ---- target square wave (period 2*pi, amplitude 1) ----
        def square_wave(x):
            return 1 if np.sin(x) >= 0 else -1

        square_graph = axes.plot(square_wave, x_range=[0, 4 * PI, 0.01], color=WHITE)
        square_label = Text("target square wave", font_size=24, color=WHITE)
        square_label.next_to(axes, DOWN)

        self.play(Create(square_graph), Write(square_label))
        self.wait(1)

        # ---- harmonics ----
        harmonics = [1, 3, 5, 7, 9]
        colors = [BLUE, GREEN, YELLOW, ORANGE, PURPLE]

        def term(n):
            return lambda x: (4 / PI) * np.sin(n * x) / n

        partial_sum_funcs = []
        running_terms = []

        for n in harmonics:
            running_terms.append(term(n))

        partial_graph = None

        for i, n in enumerate(harmonics):
            harmonic_graph = axes.plot(term(n), color=colors[i], x_range=[0, 4 * PI])
            harmonic_label = Text(f"n={n}", font_size=20, color=colors[i])
            harmonic_label.next_to(axes, UP).shift(RIGHT * i * 1.2)

            self.play(Create(harmonic_graph), Write(harmonic_label), run_time=1)

            def partial_sum(x, terms=running_terms[: i + 1]):
                return sum(f(x) for f in terms)

            new_partial_graph = axes.plot(partial_sum, color=RED, x_range=[0, 4 * PI])

            if partial_graph is None:
                partial_graph = new_partial_graph
                self.play(Create(partial_graph))
            else:
                self.play(Transform(partial_graph, new_partial_graph))

            self.wait(0.5)

        final_label = Text("Sum of 5 harmonics approximates the square wave", font_size=24)
        final_label.next_to(axes, DOWN)
        self.play(Write(final_label))
        self.wait(2)
