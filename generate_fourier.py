"""
generate_fourier.py

Calls the Gemini API (google-generativeai) to generate a Manim scene that
demonstrates Fourier series decomposition of a square wave, and saves the
model's raw code output to fourier_series.py.

Setup:
    pip install google-generativeai
    export GEMINI_API_KEY="your-api-key-here"

Run:
    python generate_fourier.py
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

Write a COMPLETE, runnable Manim scene (Python) called `FourierSeries`
that demonstrates how a square wave is approximated by a sum of sine
harmonics (a Fourier series). Requirements:

1. Draw a coordinate system (Axes) with clearly labeled, numerically
   scaled x and y axes.
2. Plot the TARGET square wave (the function being approximated) once,
   in a neutral color, as a visual reference.
3. Plot at least the first 5 odd harmonics of the Fourier sine series for
   a square wave: f(x) ~ (4/pi) * sum sin(n*x)/n for n = 1, 3, 5, 7, 9.
   Each harmonic must be drawn in its own distinct, clearly distinguishable color,
   and labeled (e.g. "n=1", "n=3", etc.) with a small legend so the
   viewer can match color to harmonic.
4. Show the CUMULATIVE partial sum updating step by step as each new
   harmonic is added (i.e. after adding n=1, show the partial sum curve;
   then transform/update it as n=3, n=5, n=7, n=9 are added one at a
   time), using a visually distinct color for the cumulative sum curve
   that is different from all the individual harmonic colors, with a
   legend label identifying it (e.g. "partial sum").
5. Use sensible animation pacing with self.wait() calls so the build-up
   is easy to follow, and make sure text labels do not overlap each
   other or run off the visible frame.
6. Include a title at the top of the scene.

Return ONLY the Python code for the full scene (including the necessary
imports, including numpy if needed, and the `from manim import *` line)
and nothing else -- no explanation, no markdown code fences.
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

    out_path = os.path.join(os.path.dirname(__file__), "fourier_series.py")
    with open(out_path, "w") as f:
        f.write(code)

    print(f"Saved generated Manim scene to: {out_path}")
    print("\n--- Render it with ---")
    print("manim -ql fourier_series.py FourierSeries")


if __name__ == "__main__":
    main()
