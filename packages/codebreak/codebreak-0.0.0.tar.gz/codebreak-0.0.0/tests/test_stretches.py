import pytest
from codebreak.stretches import stretch_exercise

def test_stretch_exercise_1_to_5():
    result = stretch_exercise(3)  # Testing with a value within 1-5 minutes
    assert result in [
        "Neck Stretch: Slowly tilt your head from side to side.",
        "Shoulder Shrug: Raise your shoulders up to your ears and release.",
        "Wrist Stretch: Extend your arm and gently pull your fingers back.",
        "Ankle Circles: Rotate your ankles clockwise and counterclockwise.",
        "Arm Circles: Extend your arms and make small circles.",
        "Chest Stretch: Place your hands behind your back and squeeze shoulder blades together.",
        "Seated Forward Bend: Reach towards your toes while seated.",
        "Finger Stretch: Spread your fingers wide, then squeeze into a fist.",
        "Shoulder Rolls: Roll your shoulders forward and backward.",
        "Seated Cat-Cow: Arch and round your back while sitting up straight."
    ]

def test_stretch_exercise_6_to_10():
    result = stretch_exercise(8)  # Testing with a value within 6-10 minutes
    assert result in [
        "Standing Forward Bend: Bend forward and reach for your toes.",
        "Chest Opener: Clasp hands behind your back and stretch.",
        "Seated Twist: Sit up straight, and twist gently to each side.",
        "Side Stretch: Reach one arm overhead and lean to the side.",
        "Figure Four Stretch: Cross one ankle over the opposite knee and lean forward.",
        "Tricep Stretch: Raise one arm and bend it behind your head, gently pulling with the other hand.",
        "Hip Flexor Stretch: Step one foot forward into a lunge and stretch the hip.",
        "Quad Stretch: Stand and pull one foot towards your buttock.",
        "Calf Stretch: Place hands on a wall and stretch your calf by pushing your heel back.",
        "Seated Hamstring Stretch: Extend one leg forward and reach towards your toes."
    ]

def test_stretch_exercise_11_to_15():
    result = stretch_exercise(12)  # Testing with a value within 11-15 minutes
    assert result in [
        "Downward Dog: Get on all fours and raise your hips into the air.",
        "Child's Pose: Sit back on your heels and stretch your arms forward.",
        "Pigeon Pose: Bring one knee forward and extend the other leg back.",
        "Reclining Twist: Lie on your back, bring one knee across your body, and turn your head in the opposite direction.",
        "Cobra Pose: Lie on your stomach and push up with your hands.",
        "Butterfly Stretch: Sit with the soles of your feet together and gently press your knees down.",
        "Happy Baby Pose: Lie on your back and grab your feet, pulling your knees towards the ground.",
        "Lying Quad Stretch: Lie on your side and pull one foot towards your buttock.",
        "Supine Hamstring Stretch: Lie on your back and lift one leg, holding it with your hands.",
        "Cat-Cow: Get on all fours, arch your back, then round it."
    ]

def test_invalid_time_limit():
    result = stretch_exercise(20)  # Testing with a value outside the valid range
    assert result == "Invalid time range. Please choose a time between 1 and 15 minutes."



