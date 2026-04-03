# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import typing


class LlmHelloWorld(gl.Contract):
    """
    The simplest possible LLM-powered contract.
    Demonstrates exec_prompt and strict_eq for basic AI consensus.
    """

    message: str

    def __init__(self):
        self.message = ""

    @gl.public.write
    def set_message(self) -> typing.Any:
        def get_message() -> str:
            task = "There is no context, I just want you to answer with a string equal to 'yes'"
            result = gl.nondet.exec_prompt(task)
            print(result)
            return result

        self.message = gl.eq_principle.strict_eq(get_message)

    @gl.public.view
    def get_message(self) -> str:
        return self.message
