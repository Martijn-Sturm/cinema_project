from collections import deque


class OfflineGroups:
    def __init__(self, groups_list):
        self.freq_dict = self._init_groups_freq_dict(groups_list)

    def _init_groups_freq_dict(self, groups_list):
        """Generates the self.freq_dict in which for each group size the frequency is stored

        Args:
            groups_list (list(int)): A list with the index of the item representing the group_size, and the item representing the frequency of this group_size

        Returns:
            dict: dictionary with {group_size: frequency}
        """
        freq_dict = {}
        for size, freq in enumerate(groups_list):
            freq_dict[size + 1] = freq
        return freq_dict

    def remove_group(self, size):
        """Lowers the group_size count/frequency of the inputted group_size

        Args:
            size (int): group_size to be decremented

        Raises:
            Exception: Is raised if no groups of this size are remaining
        """
        if self.freq_dict[size] > 0:
            self.freq_dict[size] -= 1
        else:
            raise Exception(
                "No groups of size", size, "are available to be seated (anymore)"
            )

    def get_largest_group_size(self):
        """Returns largest group size

        Returns:
            int: largest group size
        """
        return max(self.freq_dict.keys())


class OnlineGroups:
    def __init__(self, groups_list: list) -> None:
        self._groups_deque = deque(groups_list)

    def get_next_group(self):
        return self._groups_deque.popleft()
