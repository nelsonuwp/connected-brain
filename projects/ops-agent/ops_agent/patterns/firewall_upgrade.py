from ..db import get_engineer_past_comments
from .base import Pattern


class FirewallUpgradePattern(Pattern):
    slug = "firewall_upgrade"
    display_name = "Firewall Upgrade Close-out"
    description = "Drafts the customer-facing close-out comment after a firewall upgrade or cutover."

    def matches(self, ticket: dict) -> bool:
        summary = (ticket.get("summary") or "").lower()
        return "firewall" in summary and any(
            kw in summary for kw in ("upgrade", "cutover", "firmware")
        )

    async def fetch_examples(self, conn, ticket: dict) -> list[dict]:
        assignee = ticket.get("assignee_account_id")
        if not assignee:
            return []
        return await get_engineer_past_comments(
            conn,
            account_id=assignee,
            summary_pattern="Firewall%",
            limit=5,
        )

    def build_prompt(self, ticket: dict, examples: list[dict]) -> tuple[str, str]:
        org_name = ticket.get("jira_org_name") or "the customer"
        assignee_name = ticket.get("assignee_display_name") or "the engineer"

        if examples:
            example_text = "\n\n---\n\n".join(
                f"Past close-out #{i + 1}:\n{ex['body']}"
                for i, ex in enumerate(examples)
            )
        else:
            example_text = "(no past examples available)"

        system_prompt = (
            f"You are {assignee_name}, an Aptum network engineer. "
            f"You have just finished a firewall upgrade or cutover for {org_name}. "
            f"Write the customer-facing close-out comment for the Jira ticket.\n\n"
            f"Match the voice, length, and formality of your past close-out comments exactly. "
            f"Be concise. Do not invent technical details not present in the examples or summary. "
            f"Do not add greetings or sign-offs unless your examples include them.\n\n"
            f"Here are your {len(examples)} most recent close-outs on similar tickets:\n\n"
            f"{example_text}"
        )

        user_prompt = (
            f"The ticket is:\n"
            f"Summary: {ticket['summary']}\n"
            f"Organization: {org_name}\n\n"
            f"Write the close-out comment. Output only the comment text, no preamble."
        )

        return system_prompt, user_prompt
