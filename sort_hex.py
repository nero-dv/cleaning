from typing import Any, Tuple, List


class HexadecimalSorter:
    """
    Class to handle sorting of hexadecimal string entries.
    """

    @staticmethod
    def sort_hexadecimal_strings(unsorted_hex_values: Tuple[str, ...]) -> Tuple[str, ...]:
        """
        Sorts a tuple of hexadecimal string entries.

        Args:
            unsorted_hex_values: A tuple containing unsorted hexadecimal string entries.

        Returns:
            Tuple[str, ...]: Sorted tuple of hexadecimal string entries.
        """
        hex_ints = HexadecimalSorter._convert_hex_strings_to_ints(unsorted_hex_values)
        sorted_hex_ints = sorted(hex_ints)
        sorted_hex_strings = HexadecimalSorter._convert_ints_to_hex_strings(sorted_hex_ints)
        return sorted_hex_strings

    @staticmethod
    def _convert_hex_strings_to_ints(hex_strings: Tuple[str, ...]) -> List[int]:
        """
        Convert hexadecimal strings to integers.

        Args:
            hex_strings: A tuple of hexadecimal string entries.

        Returns:
            List[int]: A list of integers converted from hexadecimal strings.
        """
        return [int(x, 16) for x in hex_strings]

    @staticmethod
    def _convert_ints_to_hex_strings(ints: List[int]) -> Tuple[str, ...]:
        """
        Convert integers back to hexadecimal strings.

        Args:
            ints: A list of integers.

        Returns:
            Tuple[str, ...]: A tuple of hexadecimal string entries.
        """
        return tuple(hex(f)[2:] for f in ints)


if __name__ == "__main__":
    # Example usage
    hex_values = ("c8", "ca", "cb", "c9")
    sorted_hex_values = HexadecimalSorter.sort_hexadecimal_strings(hex_values)
    print(f"Sorted hexadecimal values: {sorted_hex_values}")
    print("Object type:", type(sorted_hex_values))
    print("Expected output: ('c8', 'c9', 'ca', 'cb')")
