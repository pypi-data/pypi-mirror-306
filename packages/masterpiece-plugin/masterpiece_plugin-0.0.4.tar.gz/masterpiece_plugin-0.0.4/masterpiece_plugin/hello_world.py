from masterpiece import Plugin
from masterpiece import Composite


class HelloWorld(Plugin):
    """An object with a description."""

    def __init__(self, name: str = "noname", description: str = "hello") -> None:
        """Create hello world object."""
        super().__init__(name)
        self.description = description

    # @override
    def install(self, app: Composite) -> None:
        obj = HelloWorld("Hello World - A Plugin")
        app.add(obj)

    # @override
    def to_dict(self):
        """Convert instance attributes to a dictionary."""
        return {
            "_class": self.get_class_id(),  # the real class
            "_version:": 0,
            "_hello_world": {
                "description": self.description,
            },
        }

    # @override
    def from_dict(self, data):
        """Update instance attributes from a dictionary."""
        for key, value in data["_hello_world"].items():
            setattr(self, key, value)
