import json
import os
from datetime import datetime

class CloudMemory:
    def __init__(self, memory_file="memory/hermes_state.json"):
        self.memory_file = memory_file
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        self.data = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"decisions_log": [], "published_pins": [], "performance_stats": {}}

    def save_decision(self, product_id, product_title, decision_result):
        record = {
            "timestamp": datetime.now().isoformat(),
            "product_id": product_id,
            "title": product_title,
            "status": decision_result.get("status"),
            "score": decision_result.get("score"),
            "reason": decision_result.get("reason")
        }
        self.data["decisions_log"].append(record)
        self._sync_to_disk()

    def _sync_to_disk(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    mem = CloudMemory()
    mem.save_decision("p101", "سماعات لاسلكية", {"status": "APPROVE", "score": 85, "reason": "منتج ممتاز"})
    print("🧠 [Hermes Memory System]: Cloud Memory synchronized locally and ready for GitHub push.")
