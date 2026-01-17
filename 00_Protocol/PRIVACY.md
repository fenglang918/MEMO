# Privacy Baseline / 隐私基线

## Do not store (ever) / 永远不要存

- Passwords, API keys, private keys, recovery codes
- Government IDs, full addresses, bank details
- Any data that can be directly abused if leaked

## OK to store (recommended) / 推荐可以存

- Templates, structure, and “how I organize” conventions
- Public links, public profiles, non-sensitive notes
- Contact “locator” hints (e.g., “WeChat note name”), not the raw credential itself

## Suggested split / 建议分层

- Public repo: methodology + templates + sanitized examples
- Private repo: real data (people cards, logs, personal profile, screenshots)

If you want one repo:

- Put sensitive content under a folder like `private/`
- Add it to `.gitignore`
- Keep a `private/README.md` with a reminder of what belongs there

