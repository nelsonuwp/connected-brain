from abc import ABC, abstractmethod


class Pattern(ABC):
    slug: str
    display_name: str
    description: str

    @abstractmethod
    def matches(self, ticket: dict) -> bool:
        """Whether this pattern applies to the given ticket."""

    @abstractmethod
    async def fetch_examples(self, conn, ticket: dict) -> list[dict]:
        """Retrieve few-shot examples for this ticket from the database.
        Typically pulls the assigned engineer's past public comments on tickets
        matching this same pattern."""

    @abstractmethod
    def build_prompt(self, ticket: dict, examples: list[dict]) -> tuple[str, str]:
        """Return (system_prompt, user_prompt) for the LLM call."""
