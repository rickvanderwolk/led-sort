import time
import random
import board
import neopixel
from flask import Flask, render_template_string
from dotenv import load_dotenv
import os

load_dotenv()

BRIGHTNESS = float(os.getenv('BRIGHTNESS', 0.5))
LED_DATA_PIN = getattr(board, os.getenv('LED_DATA_PIN', 'D18'))
NUMBER_OF_LEDS = int(os.getenv('NUMBER_OF_LEDS', 60))
SLEEP_BETWEEN_CHANGES = float(os.getenv('SLEEP_BETWEEN_CHANGES', 0.5))
SLEEP_BETWEEN_ALGORITHMS = int(os.getenv('SLEEP_BETWEEN_ALGORITHMS', 5))
EXCLUDE_ALGORITHMS = os.getenv('EXCLUDE_ALGORITHMS', '').split(',')

strip = neopixel.NeoPixel(LED_DATA_PIN, NUMBER_OF_LEDS, brightness=BRIGHTNESS, auto_write=False)
current_algorithm_index = 0
current_algorithm = ""
iteration_count = 0
app = Flask(__name__)

def get_unsorted_array():
    array = list(range(NUMBER_OF_LEDS))
    random.shuffle(array)
    for i in range(NUMBER_OF_LEDS):
        if array[i] == i:
            swap_with = (i + 1) % NUMBER_OF_LEDS
            array[i], array[swap_with] = array[swap_with], array[i]
    return array

def show_change(array, changed_indices=None):
    global current_values
    if changed_indices:
        for i in changed_indices:
            strip[i] = (128, 0, 128)
        strip.show()
        time.sleep(SLEEP_BETWEEN_CHANGES)
    show_current_sort(array)
    current_values = array.copy()

def show_current_sort(array):
    for i in range(NUMBER_OF_LEDS):
        if array[i] == i:
            strip[i] = (0, 255, 0)
        else:
            strip[i] = (255, 0, 0)
    strip.show()

def bubble_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Bubble Sort"
    for i in range(NUMBER_OF_LEDS):
        changed_indices = []
        for j in range(0, NUMBER_OF_LEDS-i-1):
            if values[j] > values[j+1]:
                values[j], values[j+1] = values[j+1], values[j]
                changed_indices.extend([j, j+1])
        iteration_count += 1
        show_change(values, changed_indices=changed_indices)

def insertion_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Insertion Sort"
    for i in range(1, len(values)):
        key = values[i]
        j = i-1
        changed_indices = []
        while j >= 0 and key < values[j]:
            values[j + 1] = values[j]
            changed_indices.extend([j, j+1])
            j -= 1
        values[j + 1] = key
        iteration_count += 1
        show_change(values, changed_indices=changed_indices)

def selection_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Selection Sort"
    for i in range(len(values)):
        min_idx = i
        changed_indices = []
        for j in range(i+1, len(values)):
            if values[min_idx] > values[j]:
                min_idx = j
        values[i], values[min_idx] = values[min_idx], values[i]
        changed_indices.extend([i, min_idx])
        iteration_count += 1
        show_change(values, changed_indices=changed_indices)

def quick_sort(values, start, end):
    global current_algorithm, iteration_count
    current_algorithm = "Quick Sort"
    if start < end:
        pivot_index = partition(values, start, end)
        iteration_count += 1
        show_change(values, changed_indices=list(range(start, end + 1)))
        quick_sort(values, start, pivot_index - 1)
        quick_sort(values, pivot_index + 1, end)

def partition(values, start, end):
    pivot = values[end]
    i = start - 1
    changed_indices = []
    for j in range(start, end):
        if values[j] < pivot:
            i += 1
            if i != j:
                values[i], values[j] = values[j], values[i]
                changed_indices.extend([i, j])
    if i + 1 != end:
        values[i + 1], values[end] = values[end], values[i + 1]
        changed_indices.extend([i + 1, end])
    return i + 1

def shell_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Shell Sort"
    gap = NUMBER_OF_LEDS // 2
    while gap > 0:
        changed_indices = []
        for i in range(gap, NUMBER_OF_LEDS):
            temp = values[i]
            j = i
            while j >= gap and values[j - gap] > temp:
                values[j] = values[j - gap]
                changed_indices.extend([j, j-gap])
                j -= gap
            values[j] = temp
        iteration_count += 1
        show_change(values, changed_indices=changed_indices)
        gap //= 2

def heap_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Heap Sort"
    n = len(values)

    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        changed_indices = []
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            changed_indices.extend([i, largest])
            heapify(arr, n, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(values, n, i)
    for i in range(n-1, 0, -1):
        values[i], values[0] = values[0], values[i]
        iteration_count += 1
        show_change(values, changed_indices=[i, 0])
        heapify(values, i, 0)

def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    changed_indices = []

    for i in range(n):
        index = (arr[i] // exp)
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = (arr[i] // exp)
        output[count[index % 10] - 1] = arr[i]
        changed_indices.append(count[index % 10] - 1)
        count[index % 10] -= 1
        i -= 1

    for i in range(len(arr)):
        arr[i] = output[i]

    return changed_indices

def radix_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Radix Sort"
    max1 = max(values)
    exp = 1
    while max1 // exp > 0:
        changed_indices = counting_sort_for_radix(values, exp)
        iteration_count += 1
        show_change(values, changed_indices=changed_indices)
        exp *= 10

def gnome_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Gnome Sort"
    index = 0
    while index < len(values):
        if index == 0 or values[index] >= values[index - 1]:
            index += 1
        else:
            values[index], values[index - 1] = values[index - 1], values[index]
            show_change(values, changed_indices=[index, index - 1])
            index -= 1
        iteration_count += 1

def cocktail_shaker_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Cocktail Shaker Sort"
    n = len(values)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                swapped = True
                show_change(values, changed_indices=[i, i + 1])
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                swapped = True
                show_change(values, changed_indices=[i, i + 1])
        start += 1
        iteration_count += 1

def comb_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Comb Sort"
    gap = len(values)
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap // shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < len(values):
            if values[i] > values[i + gap]:
                values[i], values[i + gap] = values[i + gap], values[i]
                show_change(values, changed_indices=[i, i + gap])
                sorted = False
            i += 1
        iteration_count += 1

def pancake_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Pancake Sort"

    def flip(end):
        start = 0
        while start < end:
            values[start], values[end] = values[end], values[start]
            show_change(values, changed_indices=[start, end])
            start += 1
            end -= 1

    for size in range(len(values), 1, -1):
        max_index = values.index(max(values[:size]))
        if max_index + 1 != size:
            if max_index != 0:
                flip(max_index)
            flip(size - 1)
        iteration_count += 1

def bogosort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Bogosort"

    def is_sorted(arr):
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                return False
        return True

    while not is_sorted(values):
        old_values = values.copy()

        random.shuffle(values)

        changed_indices = [i for i in range(len(values)) if values[i] != old_values[i]]

        show_change(values, changed_indices=changed_indices)

        iteration_count += 1
        time.sleep(SLEEP_BETWEEN_CHANGES)

def stooge_sort(values, i, j):
    global current_algorithm, iteration_count
    current_algorithm = "Stooge Sort"

    if values[j] < values[i]:
        values[i], values[j] = values[j], values[i]
        show_change(values, changed_indices=[i, j])
        iteration_count += 1

    if j - i > 1:
        t = (j - i + 1) // 3
        stooge_sort(values, i, j - t)
        stooge_sort(values, i + t, j)
        stooge_sort(values, i, j - t)

def slow_sort(values, i, j):
    global current_algorithm, iteration_count
    current_algorithm = "Slow Sort"

    if i >= j:
        return

    m = (i + j) // 2

    slow_sort(values, i, m)
    slow_sort(values, m + 1, j)

    if values[m] > values[j]:
        values[m], values[j] = values[j], values[m]
        show_change(values, changed_indices=[m, j])
        iteration_count += 1

    slow_sort(values, i, j - 1)

def cycle_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Cycle Sort"

    n = len(values)

    for cycle_start in range(0, n - 1):
        item = values[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, n):
            if values[i] < item:
                pos += 1

        if pos == cycle_start:
            continue

        while item == values[pos]:
            pos += 1

        values[pos], item = item, values[pos]
        show_change(values, changed_indices=[cycle_start, pos])
        iteration_count += 1

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if values[i] < item:
                    pos += 1

            while item == values[pos]:
                pos += 1

            values[pos], item = item, values[pos]
            show_change(values, changed_indices=[cycle_start, pos])
            iteration_count += 1

def odd_even_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Odd-Even Sort"

    n = len(values)
    sorted = False

    while not sorted:
        sorted = True

        for i in range(1, n - 1, 2):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                show_change(values, changed_indices=[i, i + 1])
                iteration_count += 1
                sorted = False

        for i in range(0, n - 1, 2):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                show_change(values, changed_indices=[i, i + 1])
                iteration_count += 1
                sorted = False

        show_current_sort(values)
        time.sleep(SLEEP_BETWEEN_CHANGES)

def flash_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Flash Sort"

    n = len(values)
    m = int(0.43 * n)
    min_value = min(values)
    max_value = max(values)

    if min_value == max_value:
        show_current_sort(values)
        return

    L = [0] * m
    for value in values:
        index = min(m - 1, (value - min_value) * (m - 1) // (max_value - min_value))
        L[index] += 1

    for i in range(1, m):
        L[i] += L[i - 1]

    flash_value = values[0]
    move = 0
    j = 0
    k = m - 1

    while move < n:
        while j > L[k] - 1:
            j += 1
            k = min(m - 1, (values[j] - min_value) * (m - 1) // (max_value - min_value))

        flash_value = values[j]
        while j != L[k]:
            k = min(m - 1, (flash_value - min_value) * (m - 1) // (max_value - min_value))
            hold = values[L[k] - 1]
            values[L[k] - 1] = flash_value
            flash_value = hold
            L[k] -= 1
            show_change(values, changed_indices=[j, L[k]])
            iteration_count += 1
            move += 1

    for i in range(1, n):
        key = values[i]
        j = i - 1
        while j >= 0 and values[j] > key:
            values[j + 1] = values[j]
            j -= 1
        values[j + 1] = key
        show_change(values, changed_indices=[i, j + 1])
        iteration_count += 1

    show_current_sort(values)

def odd_even_transposition_sort(values):
    global current_algorithm, iteration_count
    current_algorithm = "Odd-Even Transposition Sort"

    n = len(values)
    sorted = False

    while not sorted:
        sorted = True

        for i in range(1, n - 1, 2):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                show_change(values, changed_indices=[i, i + 1])
                iteration_count += 1
                sorted = False

        for i in range(0, n - 1, 2):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                show_change(values, changed_indices=[i, i + 1])
                iteration_count += 1
                sorted = False

    show_current_sort(values)

algorithms = [
    bogosort,
    insertion_sort,
    quick_sort,
    pancake_sort,
    selection_sort,
    cocktail_shaker_sort,
    shell_sort,
    cycle_sort,
    bubble_sort,
    comb_sort,
    odd_even_sort,
    heap_sort,
    stooge_sort,
    radix_sort,
    gnome_sort,
    flash_sort,
    odd_even_transposition_sort,
    slow_sort
]
algorithms_to_run = [alg for alg in algorithms if alg.__name__ not in EXCLUDE_ALGORITHMS]

def calculate_progress(values):
    correct_count = sum(1 for i in range(len(values)) if values[i] == i)
    progress = (correct_count / len(values)) * 100
    return progress

def run_all_sorts_forever():
    global algorithms_to_run, iteration_count, current_algorithm, current_values, current_algorithm_index

    while True:
        for current_algorithm_index, algorithm in enumerate(algorithms_to_run):
            iteration_count = 0
            current_algorithm = algorithm.__name__.replace("_", " ").title()
            values = get_unsorted_array()
            current_values = values.copy()
            show_current_sort(values)
            time.sleep(SLEEP_BETWEEN_CHANGES)

            if algorithm in [quick_sort, stooge_sort, slow_sort]:
                algorithm(values, 0, len(values) - 1)
            else:
                algorithm(values)

            current_values = values.copy()
            show_current_sort(values)
            time.sleep(SLEEP_BETWEEN_ALGORITHMS)

@app.route('/')
def index():
    global algorithms_to_run, current_values, current_algorithm_index
    progress = calculate_progress(current_values)
    algorithm_position = current_algorithm_index + 1

    return render_template_string("""
        <html>
            <head>
                <meta http-equiv="refresh" content="1">
                <title>LED sort</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 0; }
                    .container { max-width: 600px; margin: auto; padding: 20px; }
                    h1 { font-size: 6em; margin-bottom: 0.5em; }
                    p { font-size: 4em; margin-top: 0.5em; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Algorithm: {{ current_algorithm }}</h1>
                    <p>Iterations: {{ iteration_count }}</p>
                    <p>Progress: {{ progress }}%</p>
                    <p>Algorithm {{ algorithm_position }} of {{ algorithms_to_run | length }}</p>
                </div>
            </body>
        </html>
    """, current_algorithm=current_algorithm, iteration_count=iteration_count, progress=round(progress, 2), algorithm_position=algorithm_position, algorithms_to_run=algorithms_to_run)

from threading import Thread
sort_thread = Thread(target=run_all_sorts_forever)
sort_thread.start()

app.run(host='0.0.0.0', port=5000)
