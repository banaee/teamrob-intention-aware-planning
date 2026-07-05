import yaml
with open("costs.yaml") as f:
    cfg = yaml.safe_load(f)
print(cfg["robot"]["speed_ms"])
