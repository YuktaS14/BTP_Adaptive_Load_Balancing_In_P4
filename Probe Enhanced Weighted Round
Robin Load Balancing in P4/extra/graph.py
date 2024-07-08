import matplotlib.pyplot as plt

data = {
    100: [22, 28, 27, 23],
    200: [51, 50, 50, 49],
    300: [73, 72, 76, 79],
    400: [100, 101, 98, 101],
    500: [127, 126, 125, 122]
}

categories = list(data.keys())
values = list(data.values())

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting bars
bar_width = 0.2
num_categories = len(categories)
index = list(range(num_categories))
colors = ['b', 'g', 'r', 'c']  # You can customize colors as needed

for i in range(len(values[0])):
    plt.bar([x + i * bar_width for x in index], [values[j][i] for j in range(num_categories)], bar_width, label=f'VM {i+1}', color=colors[i])

plt.xlabel('Number of clients')
plt.ylabel('Number of connections')
plt.title('Connections Destribution vs Number Of Users')
plt.xticks([i + (bar_width * (len(values[0]) - 1)) / 2 for i in index], categories)
plt.legend()
# plt.grid(True)
plt.tight_layout()
plt.show()
