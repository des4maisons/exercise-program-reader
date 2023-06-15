#!/bin/bash

exercise_csv="${1:-exercise-program.csv}"

caffeinate -d pyenv/bin/python exercise-program.py "${exercise_csv}"
