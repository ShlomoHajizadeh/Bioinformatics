"""
Day/night cycle helper functions.
"""


def cycle_length(day_length, night_length):
    return day_length + night_length


def time_in_cycle(step, day_length, night_length):
    return step % cycle_length(day_length, night_length)


def phase_of_day(step, day_length, night_length):
    t = time_in_cycle(step, day_length, night_length)
    if t < day_length:
        return "day"
    return "night"


def is_day(step, day_length, night_length):
    return phase_of_day(step, day_length, night_length) == "day"


def is_night(step, day_length, night_length):
    return phase_of_day(step, day_length, night_length) == "night"