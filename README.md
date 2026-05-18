# agentlang-index-data

Open dataset of AgentLang Index benchmark runs. Append-only. JSON
exports per dated run, Parquet files for bulk run records.

Reproduce a row: every record carries `harness_version_id` resolvable
against [truffle-dev/agentlang-index](https://github.com/truffle-dev/agentlang-index)
tags. License is CC-BY-4.0 — attribute as `AgentLang Index by Truffle,
github.com/truffle-dev/agentlang-index-data`.

## Layout

```
exports/<YYYY-MM-DD>/runs.json   JSON snapshot of one benchmark run
parquet/<YYYY-MM>/runs.parquet   Bulk run records, content-addressed
NOTICE                           Attribution + harness/Zero version pin
```

Each dated export includes a `manifest.json` next to `runs.json`
pinning the harness git SHA and Zero version the run corresponded to.

## License

CC-BY-4.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
