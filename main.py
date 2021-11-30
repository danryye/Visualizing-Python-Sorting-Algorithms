import time
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Used to record the state of the array every time an element is accessed
# The information is stored in their respective arrays
class TrackedArray():

    def __init__(self, arr):
        self.arr = np.copy(arr)
        self.reset()

    def reset(self):
        self.indices = []  # index being accessed
        self.values = []  # value being accessed
        self.access_type = []  # read(get)/write(set) operation
        self.full_copies = []  # a copy of the array with every action

    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))

    def GetActivity(self, index=None):
        if isinstance(index, type(None)):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[index], self.access_type[index])

    # Overrides getitem magic method to count when its accessed
    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)

    # Overrides getitem magic method to count when its accessed
    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")

    def __len__(self):
        return self.arr.__len__()

######## Program Settings ########
plt.rcParams["figure.figsize"] = (8,6) # width in inches X height in inches
plt.rcParams["font.size"] = 14
FPS = 60
N = 30 # population size - amount of indices

######## Populating the Array ########
# Fills an array of numbers from 0 to 1000 at even intervals, with the size of N
arr = np.round(np.linspace(0, 1000, N), 0)
np.random.shuffle(arr) # Randomizes the element inde
arr = TrackedArray(arr)

##################################################
############ Sort 1 - Insertion Sort #############
##################################################
# sorter_name = "Insertion"
# timer_start = time.perf_counter()
#
# for index in range(1, len(arr)):
#     current_value = arr[index]
#     current_position = index
#
#     while current_position > 0 and arr[current_position - 1] > current_value:
#         arr[current_position] = arr[current_position - 1]
#         current_position = current_position - 1
#     arr[current_position] = current_value
# timer_delta = time.perf_counter() - timer_start
# print(arr)

##################################################
############# Sort 2 - Quick Sort ################
##################################################
sorter_name = "Quick"
time_start = time.perf_counter()

def partition(arr, start_index:int, end_index:int):
    position = start_index

    for index in range(start_index, end_index):
        if arr[index] < arr[end_index]:
            arr[index], arr[position] = arr[position], arr[index]
            position += 1
    arr[position], arr[end_index] = arr[end_index], arr[position]
    return position

def quick_sort(arr, start_index:int, end_index:int):
    if start_index >= end_index:
        return
    position = partition(arr, start_index, end_index)
    quick_sort(arr, start_index, position - 1)
    quick_sort(arr, position + 1, end_index)

quick_sort(arr, 0, len(arr) - 1)

time_delta = time.perf_counter() - time_start

##################################################
############# Printing the Results ###############
##################################################

print(f"-------- {sorter_name} Sort --------")
print(f"Array Sorted in {time_delta*1E3:.1f} ms") # converts nanoseconds to milliseconds

fig, ax = plt.subplots() # Retrieves the figure and axes to edit
# bar(array_indexes_X, array_values_Y, aligns left edge of bars to x positions, width of bars - default=0.8)
bar_container = ax.bar(np.arange(0, len(arr), 1), arr, align="edge", width=0.8)
ax.set_xlim(0, N) # Removes the extra spacing at the edges of x-axis
ax.set(xlabel="Indexes", ylabel="Values", title=f"{sorter_name} Sort") # Set labels
text = ax.text(0, 1000, "")

# Function that goes through the full_copies array which stores the history
# of all operations and accesses. On each iteration, it will update the graph
# by changing the heights of accessed rectangles
# @param frame - index of full_copies being updated
def update(frame):
    text.set_text(f" Accesses = {frame}")
    for (rectangle, height) in zip(bar_container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color("blue")

    # Sets the color of the rectangle depending on the operation being performed
    # red   = get operations
    # green = set operations
    index, operation = arr.GetActivity(frame)
    if operation == "get":
        bar_container.patches[index].set_color("red")
    elif operation == "set":
        bar_container.patches[index].set_color("green")

    # Saves an image of the current frame in frames/ folder
    # This will be done to every frame until the sort complete
    fig.savefig(f"frames/{sorter_name}_{frame:06.0f}.png") # ex. Quick_000001.png

    return (*bar_container, text) # Returns values to be visually updated

ani = FuncAnimation(fig=fig, func=update, frames=range(len(arr.full_copies))
                    , interval=1000/FPS, blit=True, repeat=False)

plt.show()