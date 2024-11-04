
import random

def mental_exercise(break_type):
    """
    Provides a quick mental exercise to reset the mind based on the specified break type.

    Parameters:
    - break_type (str): The type of mental break needed. Options are 'focus', 'creativity', and 'mindfulness'.

    Returns:
    - str: A suggestion for a mental exercise.
    """
    focus_exercises = [
        "Close your eyes and take five deep breaths, focusing on the inhale and exhale.",
        "Practice the 4-7-8 breathing technique: inhale for 4 seconds, hold for 7, exhale for 8.",
        "Try a quick counting meditation: count down from 100 by 3s to refocus your mind.",
        "Visualize a peaceful place and imagine yourself there for one minute, focusing on each detail.",
        "Trace the shape of an object on your desk with your eyes, noticing its edges and curves.",
        "Recite a positive affirmation slowly, like 'I am focused and relaxed,' three times.",
        "Look at a nearby plant or picture and observe it closely for 60 seconds.",
        "Mentally list three things you're grateful for today and focus on each one for a moment.",
        "Imagine yourself completing your next task successfully and feel the sense of accomplishment.",
        "Spend a minute focusing on the sensations in your body, starting from head to toe.",
        "Do a 30-second eye massage with gentle pressure, focusing on relaxing your eyes."
    ]
    
    creativity_exercises = [
        "Write down three new ideas you would like to explore in your next project.",
        "Draw a quick doodle of something you find inspiring.",
        "Think of a new feature you'd add to your favorite app and jot down a few details.",
        "Create a quick list of five alternative uses for a common object near you.",
        "Sketch a quick design for a completely fictional product.",
        "Write down a random word, and think of five ways it relates to your current project.",
        "Challenge yourself to come up with a different way to solve a common daily problem.",
        "Write a short two-sentence story with a plot twist at the end.",
        "Invent a new flavor combination for a dessert or snack.",
        "List as many creative uses for a paperclip as you can think of in one minute.",
        "Imagine an alternate universe where your project is used in an unexpected way."
    ]
    
    mindfulness_exercises = [
        "Sit back, close your eyes, and focus on your body, noting any areas of tension.",
        "Take 10 slow, mindful breaths, paying attention to each breath as it enters and leaves.",
        "Look out the window and take a minute to observe the details of your surroundings.",
        "Listen to the sounds around you for one minute, noting each sound without judgment.",
        "Focus on feeling the temperature of the air and textures of objects around you.",
        "Trace small circles with your fingers and focus on the motion and sensation.",
        "Name three things you can see, three things you can hear, and three things you can feel.",
        "Hold a small object and examine it closely, noticing texture, color, and shape.",
        "Practice progressive muscle relaxation, tensing and then relaxing each muscle group.",
        "Take a few seconds to just breathe and focus on being present in the moment.",
        "Visualize yourself in a favorite calm place and picture every detail around you."
    ]
    
    exercises = {
        'focus': focus_exercises,
        'creativity': creativity_exercises,
        'mindfulness': mindfulness_exercises
    }
    
    # convert to lower 
    break_type = break_type.lower()
 
    if break_type in exercises:
        return random.choice(exercises[break_type])
    else:
        return "Please choose a valid break type: 'focus', 'creativity', or 'mindfulness'."