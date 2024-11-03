# stat-tracker

`stat-tracker` is a small utility library for short-term record-keeping, such as gathering local metrics inside a function .

## Installation

`pip install stat-tracker`

## Usage

```py
stats = StatTracker()

with stats.time1:
    sleep(0.05)

for _ in range(5):
    stats.value1 += 1

for i in stats.loop1.count(range(10)):
    pass

for i in stats('loop2').count(range(100)):
    pass

stats.tags.append('a')
stats.tags.extend(['b', 'c'])

print(f'time {stats.time1}')  # time 0.05
print(f'added {stats.value1}')  # added 5
print(f'counted {stats.loop1}')  # counted 10
print(f'counted {stats('loop2')}')  # counted 100
print(f'gathered {stats.tags}')  # gathered ['a', 'b', 'c']
```
