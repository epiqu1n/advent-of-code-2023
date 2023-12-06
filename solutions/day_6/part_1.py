from math import floor
from operator import itemgetter

races = [
    { "time": 56, "distance": 499 },
    { "time": 97, "distance": 2210 },
    { "time": 77, "distance": 1097 },
    { "time": 93, "distance": 1440 },
]

def calculate_distance(race_time: int, button_hold_time: int) -> int:
    velocity = button_hold_time
    remaining_time = race_time - button_hold_time
    distance = velocity * remaining_time
    return distance

def calculate_button_hold_times(race_time: int, best_distance: int) -> range:
    """Returns a tuple representing a range of times (low, high) where the button can be held
    and beat the given record with the remaining race time"""

    # Use a sort of binary search to find upper and lower bounds of valid times range
    low_bound = floor(race_time / 2)
    high_bound = floor(race_time / 2)
    new_low = -1
    new_high = -1
    iteration = 1

    def calc_new_time(prev_time: int, iteration: int, direction: 'low' or 'high') -> int:
        adjustment = prev_time / (2 ** iteration)
        return floor(prev_time + adjustment if direction == 'high' else prev_time - adjustment)

    while True:
        new_low = calc_new_time(low_bound, iteration, 'low')
        new_high = calc_new_time(high_bound, iteration, 'high')
        distance_low = calculate_distance(race_time, new_low)
        distance_high = calculate_distance(race_time, new_high)

        if new_low == low_bound and new_high == high_bound:
            break

        if distance_low > best_distance:
            low_bound = new_low
        if distance_high > best_distance:
            high_bound = new_high

        iteration += 1

    return range(low_bound, high_bound)


def main():
    race_times_product = 1

    for race in races:
        time, distance = itemgetter('time', 'distance')(race)
        time_range = calculate_button_hold_times(time, distance)
        time_range_count = time_range.stop - time_range.start + 1
        print(time_range)
        race_times_product *= time_range_count

    print(race_times_product)

if __name__ == '__main__':
    main()
