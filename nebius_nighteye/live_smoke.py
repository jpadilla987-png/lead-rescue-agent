from __future__ import annotations

from .demo import DEMO
from .nebius_client import analyze


def main() -> None:
    result = analyze(DEMO)
    analysis = result["analysis"]
    assert analysis["observations"]
    assert len(analysis["explanations"]) >= 2
    print("Nebius/NVIDIA live smoke passed")
    print("Model:", result["model"])
    print("Material change:", analysis["material_change"])


if __name__ == "__main__":
    main()
