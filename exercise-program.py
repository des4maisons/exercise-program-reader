import csv
import argparse
import os
import time
import fileinput
from pyttsx3 import speak
import operator
from functools import reduce

class Step: pass

class WaitStep(Step):
    def __init__(self, duration):
        self._duration = int(duration)
    def evaluate(self):
       time.sleep(self._duration)
    def __repr__(self):
        return '<WaitStep length={}>'.format(self._duration)
    def __str__(self):
        return 'wait for {}s'.format(self._duration)
    @property
    def duration(self):
        return self._duration

class AnnounceStep(Step):
    def __init__(self, announcement):
        self._announcement = announcement
    def evaluate(self):
        speak(self._announcement)
    def __repr__(self):
        return '<AnnounceStep announcement={}>'.format(self._announcement)
    def __str__(self):
        return 'announce "{}"'.format(self._announcement)
    @property
    def duration(self):
        return 3  # estimated length of talk time

class ConfirmStep(Step):
    def __init__(self):
        self._wait_for = 120
    def evaluate(self):
        os.system('sleep {}'.format(self._wait_for))
    def __repr__(self):
        return '<ConfirmStep duration={}>'.format(self._wait_for)
    def __str__(self):
        return 'Wait for user confirmation to continue'
    @property
    def duration(self):
        return 0  # even though wait for is 120, we don't expect the user to wait for too long



class Exercise:
    def __init__(self,
        name,
        position,
        seconds,
        reps,
        sets,
        comment,
    ):
        self._name = name
        self._position = position
        self._seconds = seconds
        self._reps = reps
        self._sets = sets
        self._comment = comment

    def make_from_csv_dict(csv_dict):
        return Exercise(
            name=csv_dict['name'],
            position=csv_dict['position'],
            seconds=int(csv_dict['seconds']),
            reps=int(csv_dict['reps']),
            sets=int(csv_dict['sets']),
            comment=csv_dict['comment'],
        )

    @property
    def steps(self):
        steps = []
        steps += [AnnounceStep('{}, {}. '.format(self._name, self._position)
                               + 'Press control C to continue')]
        steps += [ConfirmStep()]
        if self._comment: steps += [AnnounceStep(self._comment)]
        for set in range(self._sets):
            for rep in range(self._reps):
                steps += [AnnounceStep('begin')]
                steps += [WaitStep(self._seconds)]
            steps += [AnnounceStep('end of set')]
            steps += [WaitStep(3)]
        if self._sets > 0: steps.pop(); steps.pop() # remove trailing "next set"
        steps += [AnnounceStep('end of exercise')]

        return steps

    def evaluate(self):
        [step.evaluate() for step in self.steps]

    @property
    def duration(self):
        return reduce(operator.add, [step.duration for step in self.steps])

    def __str__(self):
        return '\n'.join([str(step) for step in self.steps])


class Routine:
    def __init__(self, exercises): # exercises should be an array of exercises
        self._exercises = exercises
    def __str__(self):
        return '\n'.join([str(exercise) for exercise in self._exercises])
    def evaluate(self):
        [exercise.evaluate() for exercise in self._exercises]
    @property
    def duration(self):
        return reduce(operator.add, [exercise.duration for exercise in self._exercises])

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='csv of exercises. Can be - for stdin.')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--print-duration', help='print the estimated duration of the entire routine', action='store_true')
    return parser.parse_args()

def parse_data(filename):
    with fileinput.input(filename) as csvfile: # open(filename, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def generate_full_routine(routine_spec):
    return map(Exercise.make_from_csv_dict, routine_spec)


if __name__ == '__main__':
    args = parse_args()
    routine = Routine(generate_full_routine(parse_data(args.filename)))
    if args.dry_run:
        print(routine)
    elif args.print_duration:
        print(routine.duration)
    else:
        routine.evaluate()
