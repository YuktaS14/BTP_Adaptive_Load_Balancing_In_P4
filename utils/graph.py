import matplotlib.pyplot as plt
import numpy as np

# Define the data
x_axis = [100, 80, 60, 40, 20, 10, 4, 1]
y_axis = [
    [28, 28, 23, 21],
    [21, 19, 21, 19],
    [14, 17, 15, 14],
    [7, 7, 13, 13],
    [7, 7, 4, 2],
    [0, 0, 3, 7],
    [4, 0, 0, 0],
    [1, 0, 0, 0]
]

# Plotting
fig, ax = plt.subplots()
index = np.arange(len(x_axis))
bar_width = 0.15
num_bars = len(y_axis[0])
cmap = plt.get_cmap('tab10')  # Using a color map for different colors

for i, data in enumerate(y_axis):
    for j, value in enumerate(data):
        ax.bar(index[i] + j * bar_width, value, bar_width, color=cmap(j))

ax.set_xlabel('no of users')
ax.set_ylabel('no of connections')
ax.set_xticks(index + bar_width * (num_bars - 1) / 2)
ax.set_xticklabels([str(x) for x in x_axis])
ax.legend()
plt.tight_layout()
plt.show()
