import csv
import argparse
import os
import time
import fileinput
from pyttsx3 import speak

class Step:
    def __init__(self,
        content,
   ):
        self.content = content

    def evaluate(self):
        eval(self.content)

    def __repr__(self):
        return "<Step content='{}'>".format(self.content)


class Exercise:
    def __init__(self,
        name,
        position,
        seconds,
        reps,
        sets,
        comment,
    ):
        self.name = name
        self.position = position
        self.seconds = seconds
        self.reps = reps
        self.sets = sets
        self.comment = comment

    def make_from_csv_dict(csv_dict):
        return Exercise(
            name=csv_dict['name'],
            position=csv_dict['position'],
            seconds=int(csv_dict['seconds']),
            reps=int(csv_dict['reps']),
            sets=int(csv_dict['sets']),
            comment=csv_dict['comment'],
        )

    def steps(self):
        steps = []
        steps += [Step('speak("{}, {}")'.format(self.name, self.position))]
        steps += [Step('speak("press control C to continue")')]
        steps += [Step('os.system("sleep 120")')]
        if self.comment: steps += [Step('speak("{}")'.format(self.comment))]
        for set in range(self.sets):
            for rep in range(self.reps):
                steps += [Step('speak("begin")')]
                steps += [Step('time.sleep({})'.format(self.seconds))]
            steps += [Step('speak("end of set")')]
            steps += [Step('time.sleep(3)')]
        if self.sets > 0: steps.pop(); steps.pop() # remove trailing "next set"
        steps += [Step('speak("end of exercise")')]

        return steps

    def evaluate_steps(self):
        for step in self.steps():
            step.evaluate()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='csv of exercises. Can be - for stdin.')
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()

def parse_data(filename):
    with fileinput.input(filename) as csvfile: # open(filename, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def generate_full_routine(routine_spec):
    return map(Exercise.make_from_csv_dict, routine_spec)

def run_routine(routine):
    for exercise in routine:
        exercise.evaluate_steps()

def print_routine(routine):
    for exercise in routine:
        for step in exercise.steps():
            print(step)

if __name__ == '__main__':
    args = parse_args()
    routine = generate_full_routine(parse_data(args.filename))
    if args.dry_run:
        print_routine(routine)
    else:
        run_routine(routine)
