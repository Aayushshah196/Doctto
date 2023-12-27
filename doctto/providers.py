from faker import Faker
from faker.providers import BaseProvider
from providers import HexadecimalProvider

_fake_gen = Faker()


def get_callable_names_for_providers(faker):
    callable_names = []

    for provider_cls in faker.get_providers():
        # Get the callable names for fake methods
        provider_methods = [
            method
            for method in dir(provider_cls)
            if callable(getattr(provider_cls, method)) and not method.startswith("_")
        ]

        # Append provider name as a prefix to the callable names
        callable_names.extend([method for method in provider_methods])

    return set(callable_names)


# Add any new providers in this file in the form
_fake_gen.add_provider(HexadecimalProvider)

SYNTHETIC_GENERATOR = {
    generator_name: getattr(_fake_gen, generator_name, _fake_gen.text)
    for generator_name in get_callable_names_for_providers(_fake_gen)
}


if __name__ == "__main__":
    print("Random Hex string: ", SYNTHETIC_GENERATOR["hexadecimal_string"]())
