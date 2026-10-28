from argos import __version__, config
from argos.cli import main


def test_hello_uses_default_settings(capsys, monkeypatch):
    monkeypatch.delenv("ARGOS_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("ARGOS_LLM_MODEL", raising=False)
    monkeypatch.setattr(config, "load_dotenv", lambda: None)
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "Hello, I'm Argos" in out
    assert "groq" in out
    assert "openai/gpt-oss-120b" in out


def test_settings_can_be_overridden(monkeypatch):
    monkeypatch.setattr(config, "load_dotenv", lambda: None)
    monkeypatch.setenv("ARGOS_LLM_MODEL", "openai/gpt-oss-20b")
    assert config.load_settings().llm_model == "openai/gpt-oss-20b"


def test_version_flag(capsys):
    try:
        main(["--version"])
    except SystemExit as exit_:
        assert exit_.code == 0
    assert __version__ in capsys.readouterr().out
