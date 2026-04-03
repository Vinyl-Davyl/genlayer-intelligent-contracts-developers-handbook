# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class Hello(gl.Contract):
    """A basic deterministic contract demonstrating GenLayer fundamentals."""

    name: str

    def __init__(self, name: str):
        self.name = name

    @gl.public.view
    def greet(self) -> str:
        return f"Hello, {self.name}!"

    @gl.public.write
    def set_name(self, name: str):
        print(f"debug old name: {self.name}")
        self.name = name
