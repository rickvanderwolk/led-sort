import time
import random
import board
import neopixel
from flask import Flask, render_template_string

BRIGHTNESS = 0.5 # between 0.0 and 1.0
LED_STRIP_DATA_PIN = board.D18 # gpio 18
NUMBER_OF_LEDS = 60
SLEEP_BETWEEN_CHANGES = 0.5
SLEEP_BETWEEN_ALGORITHMS = 5

strip = neopixel.NeoPixel(LED_STRIP_DATA_PIN, NUMBER_OF_LEDS, brightness=BRIGHTNESS, auto_write=False)
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
    if changed_indices:
        for i in changed_indices:
            strip[i] = (128, 0, 128)
        strip.show()
        time.sleep(SLEEP_BETWEEN_CHANGES)
    show_current_sort(array)

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

def run_all_sorts_forever():
    algorithms = [
        #bogosort,
        insertion_sort,
        selection_sort,
        quick_sort,
        bubble_sort,
        shell_sort,
        heap_sort,
        gnome_sort,
        cocktail_shaker_sort,
        comb_sort,
        radix_sort,
        pancake_sort
    ]

    while True:
        for algorithm in algorithms:
            global iteration_count
            iteration_count = 0
            values = get_unsorted_array()
            show_current_sort(values)
            time.sleep(SLEEP_BETWEEN_CHANGES)

            if algorithm in [quick_sort]:
                algorithm(values, 0, len(values) - 1)
            else:
                algorithm(values)

            show_current_sort(values)
            time.sleep(SLEEP_BETWEEN_ALGORITHMS)

@app.route('/')
def index():
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
                    <h1>Algoritme: {{ current_algorithm }}</h1>
                    <p>Iteraties: {{ iteration_count }}</p>
                </div>
            </body>
        </html>
    """, current_algorithm=current_algorithm, iteration_count=iteration_count)

from threading import Thread
sort_thread = Thread(target=run_all_sorts_forever)
sort_thread.start()

app.run(host='0.0.0.0', port=5000)
