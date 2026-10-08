---
type: rule
tags: [workflow, tooling]
repo: none
created: 2026-10-07
---
# Skills Are Tools

A rule is a standard, and a skill is a tool. A skill must not collide with a rule. Install only the skill text that changes what an agent does. Own each copy.

## The Rules

- **Install by copy.** Copy only the skill folders that the work needs into `~/.agents/skills/`. Link each one into `~/.claude/skills/` with a relative link, for example `../../.agents/skills/<name>`. Do not install a plugin or a whole bundle for one skill. A plugin also adds hooks, commands, and other skills.
- **Trim before first use.** Keep only the text that changes what the agent does: the method, the guardrails, and the trigger description. Cut persona text, marketing, and benchmark claims. Also cut commands for programs that you do not use and sections for work that you do not do.
- **Check for collisions before first use.** Compare the trimmed skill with each rule in `brain/rules/`. When the skill collides with a rule, change the skill or do not install it. Do not change the rule to fit the skill. Do not add a clause that ranks the rule above the skill.
- **Own the copy.** An update through `npx skills update` or a plugin update replaces a managed copy and brings the fluff back. An owned copy changes only when the user decides. For an upgrade, compare the new upstream version with the owned copy. Take only the changes that matter.
- **Use `find-skills` to find, not to install.** `find-skills` installs with `npx skills add ... -g -y`, which skips the trim and the collision check. Install the result by copy.
- **Keep a team skill linked.** A skill from a repo that the user's team owns stays connected to that repo, through a link or a plugin. The trim step does not apply to it. When a team skill collides with a rule, fix the skill in its team repo, not in a local copy. Change a team repo only when the user tells you to.
- **Apply at each new install and each upgrade.** An existing install that does not follow this rule stays as it is until its next upgrade. Do not upgrade it with `npx skills update` or `git pull`. Replace it with an owned copy of the new version. Use the upgrade steps in [How to Apply](#how-to-apply).
- **The user decides each exception.** The user can keep a skill that collides with a rule, for example a plugin that the user values. Record the decision and the known collisions in the queue task.

## How to Apply

To install a skill, do these steps:

1. Create a queue task for the skill.
2. Copy the original upstream files to `~/.cache/<task-id>/`. A later upgrade compares against them.
3. Trim the copy in `~/.agents/skills/`.
4. Check the copy against the rules.
5. Link the copy into `~/.claude/skills/`.
6. Record the upstream source and version in the task.

To upgrade an install that does not follow this rule, do these steps:

1. Create a queue task for the upgrade.
2. Back up the old install.
3. Remove the old install. For a skill that the skills CLI manages, run `npx skills rm -g <name>`, which also removes its lock entry.
4. Install the new version with install steps 2 to 6.
5. Keep each setting that names the skill, for example a key in `skillOverrides`.

To remove a skill, do these steps:

1. Back up its folder.
2. Remove its folder from `~/.agents/skills/`. For a skill that the skills CLI manages, run `npx skills rm -g <name>`.
3. Remove its link from `~/.claude/skills/`.
4. Remove each setting that names it, for example a key in `skillOverrides`.

## Why

The user wanted this rule because installed skills brought fluff and collided with the brain rules, on 2026-10-07. A rule is a standard, and a skill is a tool, so there should be no collision between them.

## Related

[ponytail-baseline](ponytail-baseline.md) · [vault-is-not-a-repo](vault-is-not-a-repo.md) · [work-tracking](work-tracking.md) · [keep-it-simple-stupid](keep-it-simple-stupid.md)
