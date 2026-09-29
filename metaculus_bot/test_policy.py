from pathlib import Path

WORKFLOW = Path(".github/workflows/metaculus-fall-2026.yml")
BOT = Path("metaculus_bot/bot.py")

def main() -> None:
    workflow = WORKFLOW.read_text()
    bot = BOT.read_text()

    assert "schedule:" not in workflow, "automatic schedule must stay disabled"
    assert workflow.count("default: false") >= 2, "both manual safety gates must default false"
    assert "ALLOW_METACULUS_POSTS: ${{ inputs.allow_posts }}" in workflow
    assert "NIGHTEYE_RESEARCH_READY: ${{ inputs.research_ready }}" in workflow
    assert 'os.getenv("ALLOW_METACULUS_POSTS", "").lower() == "true"' in bot
    assert 'os.getenv("NIGHTEYE_RESEARCH_READY", "").lower() == "true"' in bot
    assert "if not research_ready:" in bot
    assert "openrouter/openrouter/free" in bot
    assert "METACULUS_TOKEN" in bot and "OPENROUTER_API_KEY" in bot
    print("Metaculus policy guard: PASS")

if __name__ == "__main__":
    main()
