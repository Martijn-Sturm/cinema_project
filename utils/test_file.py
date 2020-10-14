import random


def generate_group_sequence(
    n: int,
    seed,
    seq_range: range = range(1, 9),
    probability: list = [0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05],
):
    if len(seq_range) != len(probability):
        raise ValueError(
            "number of items in range and probability list does not match.",
            f"\nRange: {len(seq_range)}\n Prob: {len(probability)}",
        )
    sizes = list(seq_range)
    random.seed(seed)
    return random.choices(sizes, probability, k=n)


def generate_group_sequences(
    n_groups: int,
    seq_length: int,
    seed,
    seq_range: range = range(1, 9),
    probability: list = [0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05],
):
    random.seed(seed)
    seeds_list = [random.random() for i in range(n_groups)]
    result = []
    for new_seed in seeds_list:
        result.append(generate_group_sequence(seq_length, new_seed))
    return result


def write_test_file(filename, contents):
    with open(f"input/{filename}.txt", mode="w") as file:
        file.writelines([str(group) + "\n" for group in contents])


# result = generate_group_sequences(20, 10, "test")
# print(result[0])
# print(result[1])
# print(result[2])

# result = generate_group_sequences(20, 10, "test")
# print(result[0])
# print(result[1])
# print(result[2])
