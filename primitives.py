from functools import partial


def seq(*args):
    for arg in args:
        arg()

def seq2(step1, step2):
    return partial(seq, step1, step2)

def seq3(step1, step2, step3):
    return partial(seq, step1, step2, step3)

def if_then_else(condition, out1, out2):
    out1() if condition() else out2()

def switch4(condition, out1, out2, out3, out4):
    value = condition()
    if value == 0:
        out1()
    elif value == 1:
        out2()
    elif value == 2:
        out3()
    else:
        out4()
