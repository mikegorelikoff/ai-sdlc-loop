# Guide: install Loop

## Goal

Install and verify the exact Loop package without replacing unrelated skills.

## When to use it

Use this guide for a new project or a new supported agent profile.

## Prerequisites

Review [Prerequisites](../prerequisites.md) and choose one profile from [Supported environments](../reference/environments.md).

## Procedure

Use the one-command install from [Start here](../start-here.md). Run its separate verification command. For a local checkout, use `python3 install.py PROFILE`.

## Verify

The verifier reports 19 Loop skills and the selected project root contains the exact inventory from the [skill catalog](../reference/skills.md).

## Troubleshooting

If unmanaged or drifted content is reported, preserve the local files and run [Doctor](doctor.md) before deciding whether to replace anything.

## Next step

Continue with [Deliver a first change](first-change.md).
