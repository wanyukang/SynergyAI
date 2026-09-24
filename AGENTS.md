# Repository Guidelines

## Project Structure & Module Organization

This repository is a small Python prototype for multi-agent PRD review. The executable entry point is `SynergyAI_demo.py`; `llm_client.py` contains provider configuration and API calls, while `utils.py` contains shared helpers. `sample_document.md` is the example input document. Images such as `logo.jpg` and `Anthropic-projects.png` support the README and demo presentation. There is currently no dedicated `tests/` directory or package layout.

## Build, Test, and Development Commands

Install the runtime dependency with:

```bash
pip install openai
```

Run the demonstration locally with:

```bash
python3 SynergyAI_demo.py
```

The demo reads the sample document and calls the configured LLM provider. Set the matching credential before running, for example `SILICONFLOW_TOKEN`, `GITHUB_TOKEN`, or `DEEPSEEK_TOKEN`. Check Python syntax without making API calls with:

```bash
python3 -m py_compile SynergyAI_demo.py llm_client.py utils.py
```

## Coding Style & Naming Conventions

Use Python 3.8+ syntax, four-space indentation, descriptive `snake_case` names for functions and variables, and `PascalCase` for classes. Keep provider settings and retry behavior centralized in `llm_client.py`. Preserve the existing straightforward style; no formatter or linter is configured, so run the syntax check after edits.

## Testing Guidelines

No automated test framework is configured. For code changes, run the compile check and, when credentials are available, execute the demo against `sample_document.md`. Avoid committing secrets, generated outputs, or local tooling metadata.

## Commit & Pull Request Guidelines

Existing history uses short, generic messages such as `update`. Prefer clearer imperative messages that identify the change, such as `Improve retry handling` or `Document provider setup`. Pull requests should explain the behavior changed, list validation commands, note any required environment variables, and include sample output or screenshots when the user-visible demo changes.

## Security & Configuration Tips

Keep API tokens in environment variables and out of source files, commits, and screenshots. Review endpoint and model changes in `llm_client.py` before running the demo against a production credential.
