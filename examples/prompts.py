"""Print the prompts from drugs.json for one agent, one per line: <task-id>\t<molecule>\t<prompt>."""

import json
import sys
from pathlib import Path

agent = sys.argv[1] if len(sys.argv) > 1 else "chemgraph"
data = json.loads((Path(__file__).parent / "drugs.json").read_text())

for task in data["tasks"][agent]:
    for mol in data["molecules"]:
        print(f"{task['id']}\t{mol['name']}\t{task['prompt'].format(**mol)}")
