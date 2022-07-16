from collections import defaultdict
from datetime import datetime, timedelta


def get_input():
    events = []
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            line = line.replace('[', '')
            time, action = line.split('] ')
            if action.startswith('Guard'):
                action = action.replace('Guard #', '')
                action = action.replace(' begins shift', '')
                action = int(action)
            time_object = time_string_to_time_object(time)
            events.append((time_object, action))
    return events


def time_string_to_time_object(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M')


def get_time_event_dict(events):
    ans = dict()
    for event in events:
        time, happening = event
        ans[time] = happening
    return ans


def get_guard_sleeps(events):
    """Creates a dictionary of [minute]: defaultdict[id]: sleeptime
    and another of [guard_id]: total_sleep"""
    guard_sleeps = defaultdict(lambda: defaultdict(int))
    total_sleep = defaultdict(int)

    # Make a dict of all time events
    time_dict = get_time_event_dict(events)

    # Get the first time block
    current_time = events[0][0]
    current_guard_id = events[0][1]

    # Get the last time block
    last_time = events[-1][0]

    # Set state
    state = 'awake'

    # Iterate through the times MINUTE BY MINUTE
    while current_time != last_time:
        # Advance the current time
        current_time += timedelta(minutes=1)

        # Check for new events
        if current_time in time_dict:
            event = time_dict[current_time]
            if event == 'falls asleep':
                state = 'sleeping'
            elif event == 'wakes up':
                state = 'awake'
            elif type(event) == int:
                current_guard_id = event
                state = 'awake'

        # Record what's happening
        if state == 'sleeping':
            guard_sleeps[current_time.minute][current_guard_id] += 1
            total_sleep[current_guard_id] += 1

    return guard_sleeps, total_sleep






def main():
    # Get all events
    events = get_input()

    # Sort them chronologically
    events.sort(key=lambda x: x[0])



    # Get a dictionary of guard sleeping times
    guard_sleeps, total_sleep = get_guard_sleeps(events)

    sleepiest_guard = max(total_sleep.items(), key=lambda x: x[1])[0]



    # Get sleepiest guard minute
    dreamland = []
    for minute in guard_sleeps:
        if sleepiest_guard in guard_sleeps[minute]:
            dreamland.append((minute, guard_sleeps[minute][sleepiest_guard]))

    most_minutes = max(dreamland, key=lambda x: x[1])[0]

    print(sleepiest_guard * most_minutes) # Part 1 answer


    total_max = None
    guard_id = None
    minute_id = None
    # Get most frequently asleep in a single minute
    for minute, records in guard_sleeps.items():
        g_id, minutes = max(records.items(), key=lambda x: x[1])
        if total_max is None or minutes > total_max:
            total_max = minutes
            guard_id = g_id
            minute_id = minute

    print(guard_id * minute_id)  # Part 2 answer





main()
