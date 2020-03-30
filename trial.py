import subprocess
def isWord(word):
    t = subprocess.check_output(['swift','trial.swift',word]).decode("utf-8")
    if t[-2]=='0':
        return False
    return True