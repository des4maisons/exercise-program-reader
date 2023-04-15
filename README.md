# Exercise program reader

This script reads an exercise program described in a .csv file and uses voice
prompts to guide the user through the steps they must take.

It requires pyttsx3 to interact with your operating system's voice.

I have only tested it on macos.

## Usage

```
pip3 install pyttsx3
python3 exercise-program.py <csv-file> [ --dry-run ]
```

See `--help` for all options.

## CSV format

The program expects a CSV file with the headers as in the example CSV provided.

## Quirks

- before the exercise starts, the program prompts you to hit Ctrl C when ready
  to continue. you have to wait a second or two after that voice prompt before
  the ctrl C will behave correctly (and not kill the whole program).
