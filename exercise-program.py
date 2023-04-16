import csv
import argparse
import os
import time
import fileinput
from pyttsx3 import speak

class Step: pass

class WaitStep(Step):
    def __init__(self, duration):
        self.duration = int(duration)
    def evaluate(self):
       time.sleep(self.duration)
    def __repr__(self):
        return '<WaitStep length={}>'.format(self.duration)
    def __str__(self):
        return 'wait for {}s'.format(self.duration)

class AnnounceStep(Step):
    def __init__(self, announcement):
        self.announcement = announcement
    def evaluate(self):
        speak(self.announcement)
    def __repr__(self):
        return '<AnnounceStep announcement={}>'.format(self.announcement)
    def __str__(self):
        return 'announce "{}"'.format(self.announcement)

class ConfirmStep(Step):
    def __init__(self):
        self.duration = 120
    def evaluate(self):
        os.system('sleep {}'.format(self.duration))
    def __repr__(self):
        return '<ConfirmStep duration={}>'.format(self.duration)
    def __str__(self):
        return 'Wait for user confirmation to continue'



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
        steps += [AnnounceStep('{}, {}'.format(self.name, self.position))]
        steps += [AnnounceStep('press control C to continue')]
        steps += [ConfirmStep()]
        if self.comment: steps += [AnnounceStep(self.comment)]
        for set in range(self.sets):
            for rep in range(self.reps):
                steps += [AnnounceStep('begin')]
                steps += [WaitStep(self.seconds)]
            steps += [AnnounceStep('end of set')]
            steps += [WaitStep(3)]
        if self.sets > 0: steps.pop(); steps.pop() # remove trailing "next set"
        steps += [AnnounceStep('end of exercise')]

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
