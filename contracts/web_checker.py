# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class WebChecker(gl.Contract):
    """Demonstrates non-deterministic web access with strict equivalence."""

    has_content: bool

    def __init__(self):
        example_url = "https://example.org"

        def check_page():
            web_data = gl.nondet.web.render(example_url, mode="html")
            return "iana" in web_data.lower()

        self.has_content = gl.eq_principle.strict_eq(check_page)

    @gl.public.view
    def get_result(self) -> bool:
        return self.has_content
