#!/usr/bin/env python3

import code
import readline
import rlcompleter
import os
import sys

class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


class OurOut:
    def __init__(self):
        self.line = ""

    def write(self, line):
        self.line += line

    def flush(self):
        pass

class NotAKoansole(code.InteractiveConsole):
    score = 0
    challenges = [
        { "message" : "You can make the intepreter talk using 'print(\"hello world\")'\n"
        "Try running this now!",
          "expected" : "Hello World"
        },
        { "message" : "You can add ints with +, such as  '1 + 1'"
        "Try running this now!",
          "expected" : "2"
        }
    ]

    def raw_input(self, prompt=''):
        print (self.challenges[self.score]["message"])
        return input(prompt).strip()

    def push(self, line):
        print("You tried "+line)
        out = OurOut()
        with RedirectStdStreams(stdout=out):
            self.runsource(line)
        print(out.line.strip())
        if self.challenges[self.score]["expected"] == out.line.strip():
            print("That's correct!")
            self.score += 1
        else:
            print("That's wrong")

readline.parse_and_bind("tab: complete")
NotAKoansole().interact()
