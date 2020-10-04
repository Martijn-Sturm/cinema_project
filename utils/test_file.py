from random import choices


def generate_group_sequence(
    n: int,
    seq_range: range = range(1, 9),
    probability: list = [0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05],
):
    if len(seq_range) != len(probability):
        raise ValueError(
            "number of items in range and probability list does not match.",
            f"\nRange: {len(seq_range)}\n Prob: {len(probability)}",
        )
    sizes = list(seq_range)
    return choices(sizes, probability, k=n)


def write_test_file(filename, contents):
    with open(f"input/{filename}.txt", mode="w") as file:
        file.writelines([str(group) + "\n" for group in contents])


# write_test_file("new_test1", generate_group_sequence(100))

