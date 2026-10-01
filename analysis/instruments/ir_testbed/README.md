# The IR test-bed's instrument (shared code)

The code of the IR test-bed (design_decisions.md, "The IR test-bed"; glossary §8, TB), shared by the domains since the
sort (1 October 2026). What it runs, what it derives from which record, and how it compares are stated in kitting's
record, `analysis/kitting/ir_testbed/README.md` (the pipeline, the columns, rules 1 to 23 with their sources, the
readings R1 to R4); a domain's set, its expectations and its report live in `analysis/<domain>/ir_testbed/`, its run
files in `configs/<domain>/ir_testbed/`.

```bash
analysis/instruments/ir_testbed/run.sh <domain>                         # every configs/<domain>/ir_testbed/*.yaml
analysis/instruments/ir_testbed/run.sh <domain> [-o <out root>] [run files]
```

Outputs per scenario in `<out root>/<scenario>/` (default `analysis/<domain>/ir_testbed/`), the run's log and `.rec` in
`<out root>/runs/` (git-ignored). Run from the repo root; PYTHONHASHSEED=0 is set by the script.
