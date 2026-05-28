# agentlang-index-data

Open dataset of AgentLang Index benchmark runs. Append-only. JSON
exports per dated run.

Reproduce a row: every record carries `harnessSha` resolvable against
[truffle-dev/agentlang-index](https://github.com/truffle-dev/agentlang-index).
License is CC-BY-4.0 — attribute as `AgentLang Index by Truffle,
github.com/truffle-dev/agentlang-index-data`.

## Layout

```
exports/<YYYY-MM-DD>/manifest.json   harness SHA, Zero version, models, totals
exports/<YYYY-MM-DD>/dashboard.json  per-model/per-language summary
exports/<YYYY-MM-DD>/runs.json       flat array, one record per attempt
exports/<YYYY-MM-DD>/attempts/...    raw response.md / system.md / user.md / result.json
NOTICE                               attribution + harness/Zero version pin
```

A Parquet mirror under `parquet/<YYYY-MM>/runs.parquet` is planned for
later releases; v1.0 ships JSON only.

## First export

[`exports/2026-05-19/`](exports/2026-05-19/) — 300 attempts across 3
OpenAI models and 20 tasks.

- 3 OpenAI models in one-shot mode: gpt-5, gpt-4o, gpt-4o-mini.
- 20 tasks x 5 languages (zero, ts, rust, go, python) = 100 attempts
  per model.
- gpt-5 reached 79% overall and 0% on Zero. Per-model and per-language
  breakdown on the leaderboard:
  https://truffleagent.com/agentlang/leaderboard/

## License

CC-BY-4.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
