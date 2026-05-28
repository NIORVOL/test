"""Example module demonstrating code standards."""


def greet(name: str, greeting: str | None = None) -> str:
    """Generate a greeting message.

    Args:
        name: The name to greet.
        greeting: Optional custom greeting. Defaults to "Hello".

    Returns:
        The formatted greeting string.
    """
    if greeting is None:
        greeting = "Hello"

    return f"{greeting}, {name}!"


def calculate_sum(numbers: list[int]) -> int:
    """Calculate the sum of a list of numbers.

    Args:
        numbers: List of integers to sum.

    Returns:
        The total sum.
    """
    total = 0
    for num in numbers:
        total += num
    return total


class DataProcessor:
    """Process data with standard patterns."""

    def __init__(self, name: str):
        """Initialize the processor.

        Args:
            name: Name of this processor.
        """
        self.name = name
        self._data: list[str] = []

    def add(self, item: str) -> None:
        """Add an item to the data list.

        Args:
            item: String item to add.
        """
        self._data.append(item)

    def get_all(self) -> list[str]:
        """Return all stored items."""
        return self._data.copy()
