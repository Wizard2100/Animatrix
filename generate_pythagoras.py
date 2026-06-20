"""
generate_pythagoras.py

Calls the Gemini API (google-generativeai) to generate a Manim scene that
visually proves the Pythagorean Theorem, and saves the model's raw code
output to pythagoras.py.

Setup:
    pip install google-generativeai
    export GEMINI_API_KEY="your-api-key-here"

Run:
    python generate_pythagoras.py
"""

import os
import re
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "Set the GEMINI_API_KEY environment variable before running this script."
    )

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-pro"  # swap for "gemini-2.0-flash" / latest available model if needed

PROMPT = """
You are an expert Manim (Community Edition) developer and math educator.

Write a COMPLETE, runnable Manim scene (Python) called `PythagoreanTheorem`
that visually proves the Pythagorean Theorem (a^2 + b^2 = c^2) for a
right triangle. Requirements:

1. Draw a right triangle and clearly label its two legs "a", "b" and its
   hypotenuse "c".
2. Construct a square on each of the three sides, geometrically correct
   (i.e. each square's side length matches the corresponding triangle
   side, and the squares should not awkwardly overlap the triangle or
   each other).
3. Shade/fill the three squares with three distinct, visually
   distinguishable colors.
4. Label each square with its algebraic area (a^2, b^2, c^2).
5. Display the algebraic identity "a^2 + b^2 = c^2" on screen, and then
   show it evaluated with actual numbers for a concrete triangle (e.g.
   a 3-4-5 triangle).
6. Use sensible animation pacing (Create/Write/FadeIn calls separated by
   self.wait() calls) so a human viewer can follow each step.
7. Make sure everything fits within the visible frame at every point in
   the animation (no overlapping labels, no elements running off-screen).

Return ONLY the Python code for the full scene (including the necessary
imports and the `from manim import *` line) and nothing else -- no
explanation, no markdown code fences.
"""


def extract_code(raw_text: str) -> str:
    """Strip markdown code fences if the model includes them anyway."""
    match = re.search(r"```(?:python)?\s*(.*?)```", raw_text, re.DOTALL)
    return match.group(1).strip() if match else raw_text.strip()


def main():
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(PROMPT)

    raw_output = response.text
    code = extract_code(raw_output)

    out_path = os.path.join(os.path.dirname(__file__), "pythagoras.py")
    with open(out_path, "w") as f:
        f.write(code)

    print(f"Saved generated Manim scene to: {out_path}")
    print("\n--- Render it with ---")
    print("manim -ql pythagoras.py PythagoreanTheorem")


if __name__ == "__main__":
    main()
