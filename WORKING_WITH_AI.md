# Working with AI

## Purpose

Use AI to expand skill, judgement, and productive hours—not to replace
critical thinking, ownership, or understanding.

## Working style

- Work in small, understandable steps.
- Explain what each step does and why it matters.
- Use exact file locations and concise examples.
- Agree scope and approach before generating implementation code.
- Prefer plans, checklists, and small diffs over large unreviewed dumps.
- Keep business rules in services; keep API contracts in serializers;
  keep HTTP concerns in views.
- Use tests to prove behaviour, including happy paths and failure cases.
- Treat AI output as a draft: review it, run it, and understand it before
  accepting it.

## Local ownership

- The user retains the final step before any code is pushed.
- Code is primarily created and managed from the user’s local machine.
- Do not push, commit, delete, or modify repository content without explicit
  approval.
- Before pushing, confirm the change is understood, tested, and intentional.

## Review checklist

Before accepting AI-generated work:

- Does it solve the agreed requirement, and nothing else?
- Can every changed file and decision be explained?
- Are rules in the right architectural layer?
- Are tests meaningful and independent?
- Are there security, permission, or data-integrity concerns?
- Has the change been run locally and verified?
- Is the commit message clear and accurate?

## Prompt pattern

For a new feature:

1. State the goal and constraints.
2. Ask for a plan: files, responsibilities, tests, edge cases, assumptions.
3. Approve or correct the plan.
4. Implement one small slice.
5. Run and review locally.
6. Commit and push only when satisfied.
