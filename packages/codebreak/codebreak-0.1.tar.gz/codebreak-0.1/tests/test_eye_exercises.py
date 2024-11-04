import pytest
from codebreak.eye_exercises import eye_exercise

def test_low_intensity():
    result = eye_exercise(10)
    assert result in [
        "Blink rapidly for 10 seconds to relax your eyes.",
        "Close your eyes for 10 seconds, then open them wide.",
        "Gently massage your temples with your fingers for 10 seconds to ease eye strain.",
        "Roll your eyes in a circular motion for 10 seconds to relax eye muscles.",
        "Shift your focus quickly between near and far objects for 10 seconds."
        "Look up, down, left, and right for 10 seconds to stretch your eye muscles.",
        "Squeeze your eyes shut tightly for 10 seconds, then relax to relieve tension."
    ]

def test_med_intensity():
    result = eye_exercise(20)
    assert result in [
        "Focus on an object 20 feet away for 20 seconds, following the 20-20-20 rule.",
        "Look out of a window at the farthest point you can see for 20 seconds.",
        "Cover your eyes with warm palms for 20 seconds to relax your eyes.",
        "Draw a figure eight with your eyes for 20 seconds to improve focus and flexibility.",
        "Trace the outline of a large object in the room with your eyes for 20 seconds to improve focus control.",
        "Softly press and release the area around your eyes with your fingertips for 20 seconds to relieve tension.",
        "Look around and slowly focus on distant points for 20 seconds."
    ]

def test_high_intensity():
    result = eye_exercise(60)
    assert result in [
        "Spend 1 minutes looking at distant objects outside to reduce eye strain.",
        "Focus on blinking slowly and deliberately for 1 minute to reduce dryness.",
        "Sit comfortably, close your eyes, and let them rest for 1 minute.",
        "Readjust your posture, stand up, and gaze at the horizon for 1 minutes.",
        "Practice deep breathing with closed eyes for 1 minute for a calming effect on your vision.",
        "Look at a calming image or color for 1 minute to give your eyes a break from screens.",
        "Slowly roll your eyes in a circular motion for 1 minute to reduce strain."
    ]

def test_invalid_intensity():
    with pytest.raises(ValueError):
        eye_exercise(0)