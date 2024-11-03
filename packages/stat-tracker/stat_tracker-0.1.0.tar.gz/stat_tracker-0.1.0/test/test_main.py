from stat_tracker import StatTracker
from time import sleep


def test_time():
    stats = StatTracker()

    with stats.time1:
        with stats.time2:
            sleep(0.05)
        sleep(0.05)

    assert repr(stats.time1) == '0.10'
    assert repr(stats.time2) == '0.05'


def test_value():
    stats = StatTracker()

    for _ in range(5):
        stats.value1 += 1

    assert stats.value1 == 5
    assert repr(stats.value1) == '5'


def test_count():
    stats = StatTracker()

    for i in stats.loop1.count(range(10)):
        pass

    assert stats.loop1 == 10
    assert repr(stats.loop1) == '10'

    for i in stats('loop2').count(range(20)):
        pass

    assert stats.loop2 == 20
    assert repr(stats.loop2) == '20'


def test_list():
    stats = StatTracker()

    stats.tags.append('a')
    stats.tags.extend(['b', 'c'])

    assert 'a' in stats.tags
    assert 'b' in stats.tags
    assert 'c' in stats.tags
    assert repr(stats.tags) == "['a', 'b', 'c']"
