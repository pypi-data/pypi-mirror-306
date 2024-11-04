import time
import schedule 
import random as r 

class Exercise:
    def __init__(self, name: str, low_intensity_duration: str, medium_intensity_duration: str, high_intensity_duration: str, exercise_type: str):
        self.name = name
        self.low_intensity_duration = low_intensity_duration
        self.medium_intensity_duration = medium_intensity_duration
        self.high_intensity_duration = high_intensity_duration
        self.exercise_type = exercise_type

    def get_name(self): 
        return self.name

    def get_low_intensity_duration(self): 
        return self.low_intensity_duration

    def get_medium_intensity_duration(self): 
        return self.medium_intensity_duration
        
    def get_high_intensity_duration(self): 
        return self.high_intensity_duration
    
    def get_type(self): 
        return self.exercise_type
    
    def output(self,intensity):
        print("STOP YOUR WORK...time for an exercise break\n")

        if (self.exercise_type.strip().lower()=="cardio"):
            if (intensity.strip().lower()=="high"):
                print(f"Your exercise is: {self.get_name().capitalize()} for {self.get_high_intensity_duration()}") 
            elif (intensity.strip().lower()=="low"):
                print(f"Your exercise is: {self.get_name().capitalize()} for {self.get_low_intensity_duration()}")
            else: 
                print(f"Your exercise is: {self.get_name().capitalize()} for {self.get_medium_intensity_duration()}")
        elif (self.exercise_type.strip().lower()=="stretching"):
            if (intensity.strip().lower()=="high"):
                print(f"Your exercise is: {self.get_name().capitalize()} for {self.get_high_intensity_duration()}") 
            elif (intensity.strip().lower()=="low"):
                print(f"Your exercise is: {self.get_name().capitalize()} for {self.get_low_intensity_duration()}")
            else: 
                print(f"Your exercise is: {self.get_name().capitalize()} for {self.get_medium_intensity_duration()}")
        else:
            if (intensity.strip().lower()=="high"):
                print(f"Your exercise is: {self.get_high_intensity_duration()} {self.get_name().capitalize()}") 
            elif (intensity.strip().lower()=="low"):
                print(f"Your exercise is: {self.get_low_intensity_duration()} {self.get_name().capitalize()}")
            else: 
                print(f"Your exercise is: {self.get_medium_intensity_duration()} {self.get_name().capitalize()}")
        







def activate_exercises(current_exercises,intensity, ask_quit):
    done = False
    ask_quit[0] = True
    run_exercise(current_exercises,intensity)
    while not (done): 
        done_response = input("type 'done' when you've finished your exercise: ")
        if (done_response.strip().lower()=="done"): 
            done = True
 


def run_exercise(current_exercises,intensity):
    if intensity == "mix": 
        current_intensity = r.randint(0,2)
        if current_intensity==0:
            excercise_ind = r.randint(0,len(current_exercises)-1)
            current_exercises[excercise_ind].output("low")

        elif current_intensity==1:
            excercise_ind = r.randint(0,len(current_exercises)-1)
            current_exercises[excercise_ind].output("medium") 

        elif current_intensity==2:
            excercise_ind = r.randint(0,len(current_exercises)-1)
            current_exercises[excercise_ind].output("high") 

    else: 
        excercise_ind = r.randint(0,len(current_exercises)-1)
        current_exercises[excercise_ind].output(intensity)
    

def run():
    exercises = []
    ask_quit = [False]
    walking = Exercise("Walking", "8 minutes", "14 minutes", "20 minutes", "Cardio")
    exercises.append(walking)
    running = Exercise("Jogging/Running", "5 minutes", "10 minutes", "15 minutes", "Cardio")
    exercises.append(running)
    squats = Exercise("Squats", "15", "30", "45", "Strength")
    exercises.append(squats)
    push_ups = Exercise("Push Ups", "10", "15", "20", "Strength")
    exercises.append(push_ups)
    burpees = Exercise("Burpees", "3", "5", "7", "Strength")
    exercises.append(burpees)
    toe_touches = Exercise("Toe Touches", "30 seconds", "1 minute", "2 minutes", "Stretching")
    exercises.append(toe_touches)
    runners_stretch = Exercise("Runner's Stretch", "1-2 minutes", "3-5 minutes", "5 minutes", "Stretching")
    exercises.append(runners_stretch)
    side_reach = Exercise("Side Reaches", "1-2 minutes", "3-5 minutes", "5 minutes", "Stretching")
    exercises.append(side_reach)

    active_exercises = []
    active_intensity = None 
    acceptable_input_et = False 
    acceptable_input_i = False 
    acceptable_input_t = False 
    first_run_i = True 
    first_run_et = True
    first_run_t = True
    

    while not (acceptable_input_et): 
        if (first_run_et):
            response = input("What type of exercise are you in the mood for today?\n- Cardio\n- Strength\n- Stretching\n- Mix\ntype any of the above resonses (input 'q' to quit): ")
            first_run_et = False
            if (response.strip().lower()=="cardio"):
                acceptable_input_et = True 
                for ex in exercises: 
                    if (ex.get_type()=="cardio"): 
                        active_exercises.append(ex)
            elif (response.strip().lower()=="strength"):
                acceptable_input_et = True 
                for ex in exercises: 
                    if (ex.get_type()=="strength"): 
                        active_exercises.append(ex)
            elif (response.strip().lower()=="stretching"):
                acceptable_input_et = True 
                for ex in exercises: 
                    if (ex.get_type()=="stretching"): 
                        active_exercises.append(ex)
            elif (response.strip().lower()=="mix"):
                acceptable_input_et = True 
                active_exercises = exercises
            elif (response.strip().lower()=="q"):
                acceptable_input_et = True 
                return 0
        else: 
            response = input("Invalid input please try again\n- Cardio\n- Strength\n- Stretching\n- Mix\ntype any of the above resonses: ")

    

    while not (acceptable_input_i):
        if (first_run_i):
            response = input("What is your preferred intensity?\n- Low\n- Medium\n- High\n- Mix\ntype any of the above resonses: ")
            first_run_i = False
            if (response.strip().lower()=="low" or response.strip().lower()=="high"or response.strip().lower()=="medium" or response.strip().lower()=="mix"): 
                active_intensity = response.strip().lower() 
                acceptable_input_i = True

        else: 
            response = input("Invalide input please try again\n- Low\n- Medium\n- High\n- Mix\ntype any of the above resonses: ")

    preffered_time = 0 
    if (first_run_t):
        response = input("Enter your preffered time between exercises in WHOLE MINUTES: ")            
        first_run_t = False
    else:
        response = input("Invalid input please try again: ")     
    while not (acceptable_input_t):
        try: 
            preffered_time = int(response)
            acceptable_input_t = True 
        except ValueError:
            acceptable_input_t = False
            response = input("Invalid input please try again: ")
        
    ask_quit[0] = False
    program_running = True; 
    schedule.every(preffered_time).minutes.do(activate_exercises,active_exercises,exercises,active_intensity,ask_quit)
    while (program_running): 
        schedule.run_pending()
        if (ask_quit):
            acceptable_input_c = False
            while not acceptable_input_t: 
                response=input("Would you like to continue your exercises? (input y for yes and n for no): ")
                if (response.strip().lower()=="y"): 
                    acceptable_input_c = True 
                    schedule.clear()
                elif response.strip().lower()=="n":
                    acceptable_input_c = True 
            ask_quit[0]=False
        time.sleep(1)
        
if __name__ == "__main__":
    run()

