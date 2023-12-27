from faker.providers import BaseProvider


class HexadecimalProvider(BaseProvider):
    def hexadecimal_string(self, length=8):
        """Generate a random hexadecimal string."""
        return self.random_hex(length)

    def random_hex(self, length):
        """Generate a random hexadecimal string of the specified length."""
        return "".join(self.random_element("0123456789abcdef") for _ in range(length))
