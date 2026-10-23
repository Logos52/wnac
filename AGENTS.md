# WNAC: agent contract

Minimal contract. The ecosystem-level rules in `../AGENTS.md` apply (project disambiguation, writing style).

## Doctrine

Method public, money private. No real balances, transactions, or account details ever leave this repo or appear in screenshots. Public-facing renders use fake data only.

Comments inside an embedded page script are comments. Delete them without changing what the page does. Prove that with a diff of the built page, and cover that behavior with tests.

## Writing style

Decision documents (PRDs, proposals, decision notes, memos) follow High-Signal Decision Writing. The canonical copy is `../llm-knowledge-base/02 - System/Writing Standards.md`. The digest is in `../AGENTS.md`. The standard asks for a verdict first, measured claims, a steelman of the rejected option, a price on your own recommendation, and falsifiable success criteria.

## Reversibility

Confirm before anything destructive or hard to undo. Plan, then approve, then build, then review.

## Feedback protocol (standing rule, canonical in ~/Projects/AGENTS.md)

Deep read before execution, always. Enumerate everything Wedge asked, details included, never the gist. Find the general principle behind the specific complaint. Then execute against both, and record the principle in the appropriate standard. Prose is generated as a continuous explanation to a real person first, then filtered through the writing standards. It is never assembled from rule-compliant fragments.
