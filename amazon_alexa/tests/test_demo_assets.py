from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo"

class DemoAssetTests(unittest.TestCase):
    def test_demo_files_exist(self):
        for name in ("index.html", "style.css", "app.js"):
            self.assertTrue((DEMO / name).exists(), name)

    def test_demo_has_required_story_beats(self):
        text = (DEMO / "index.html").read_text(encoding="utf-8") + (DEMO / "app.js").read_text(encoding="utf-8")
        for phrase in ("Lead Rescue Voice","Run morning brief","price match","owner approval","MCP tool trace","Streamable"):
            self.assertIn(phrase.lower(), text.lower())

if __name__ == "__main__":
    unittest.main()
