import pytest
from unittest.mock import Mock, call
import random as r 

from codebreak.physical_exercise import Exercise, activate_exercises

class TestExercise: 

    def test_get_exercise_attributes(self): 
        exercise = Exercise("Seated Spinal Twist", "30 seconds", "1 minute", "2 minutes", "Stretching")
        assert exercise.get_name() == "Seated Spinal Twist"
        assert exercise.get_low_intensity_duration() == "30 seconds"
        assert exercise.get_medium_intensity_duration() == "1 minute"
        assert exercise.get_high_intensity_duration() == "2 minutes"
        assert exercise.get_type() == "Stretching"
    
    def test_get_exercise_output_low(self,capsys):
        exercise1 = Exercise("Walking", "5 minutes", "10 minutes", "15 minutes", "Cardio")
        exercise1.output("low")
        low_output = capsys.readouterr()
        assert "STOP YOUR WORK...time for an exercise break\n\nYour exercise is: Walking for 5 minutes\n" in low_output.out

    def test_get_exercise_output_med(self,capsys):
        exercise2 = Exercise("Walking", "5 minutes", "10 minutes", "15 minutes", "Cardio")
        exercise2.output("med")
        med_output = capsys.readouterr()
        assert "STOP YOUR WORK...time for an exercise break\n\nYour exercise is: Walking for 10 minutes\n" in med_output.out 

    def test_get_exercise_output_high(self,capsys):  
        exercise3 = Exercise("Walking", "5 minutes", "10 minutes", "15 minutes", "Cardio")
        exercise3.output("high")
        high_output = capsys.readouterr()
        assert "STOP YOUR WORK...time for an exercise break\n\nYour exercise is: Walking for 15 minutes\n" in high_output.out

    def test_activate_exercises_ask_quit(self,monkeypatch): 
        current_exercises = [Exercise("Walking", "8 minutes", "14 minutes", "20 minutes", "Cardio"),Exercise("Jogging", "5 minutes", "12 minutes", "18 minutes", "Cardio"),Exercise("Seated Spinal Twist", "30 seconds", "1 minute", "2 minutes", "Stretching")]
        ask_quit = [False]

        user_input = iter(["done"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_input))

        activate_exercises(current_exercises, "low", ask_quit)
        assert ask_quit[0] == True
        

    """WIP: def test_run_exercise_test_high(monkeypatch): 
        current_exercises = [Exercise("Walking", "8 minutes", "14 minutes", "20 minutes", "Cardio"),Exercise("Jogging", "5 minutes", "12 minutes", "18 minutes", "Cardio"),Exercise("Seated Spinal Twist", "30 seconds", "1 minute", "2 minutes", "Stretching")]
        
        monkeypatch.setattr(r, "randint", lambda a, b: 0)  # Always pick "low" intensity and first exercise

    
        run_exercise(current_exercises, "mix")
        assert current_exercises[0].output_called_with == "low"""
        

        



