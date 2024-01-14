from sprites import add_epsilon_to_every_avg, compute_probabilities

def test_add_epsilon():
    assert add_epsilon_to_every_avg([2, 3]) == [2.1, 3.1]


def test_compute_probs():
    assert compute_probabilities([2, 3]) == [2.1 / 5.2, 3.1 / 5.2]

def test_sum_of_ps():
    assert sum(compute_probabilities([2, 3])) == 1.0