#!/usr/bin/env python3

import code
import readline
import rlcompleter
import os
import sys

class RedirectStdStreams(object):
    """
    Class used to redirect output.
    Used so we can determine whether the user got the challenge correct.
    
    """
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
    """
        OurOut - stores response from the P in REPL (Read Eval Print Loop) 
    
    """
    def __init__(self):
        self.line = ""

    def write(self, line):
        self.line += line

    def errors(self, line):
        pass

    def flush(self):
        pass

class NotAKoansole(code.InteractiveConsole):
    """
        NotAKoansole - main class for interaction

    """
    score = 0
    challenges = [
        { "message" : "You can make the intepreter talk using 'print(\"hello world\")'\n"
        "Try running this now!",
          "expected" : "hello world"
        },
        { "message" : "You can add ints with +, such as  '1 + 1'\n"
        "Try running this now!",
          "expected" : "2"
        }
    ]

    def raw_input(self, prompt=''):
        print (self.challenges[self.score]["message"])
        return input(prompt).strip()

    def banner(self):
        return ""

    def push(self, line):
        print("You tried "+line)
        out = OurOut()
        with RedirectStdStreams(stdout=out, stderr=out):
            self.runsource(line)
        print(out.line.strip())
        if self.challenges[self.score]["expected"] == out.line.strip():
            print("That's correct!")
            self.score += 1
        else:
            print("That's wrong")

readline.parse_and_bind("tab: complete")
NotAKoansole().interact(banner=
    "Welcome to NotAKoansole\n"
    "Here you will learn to be clever\n\n"
)
