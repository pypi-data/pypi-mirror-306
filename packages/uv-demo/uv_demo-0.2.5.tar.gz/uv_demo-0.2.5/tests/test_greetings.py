"""Tests the greetings module."""

from loguru import logger as log

from uv_demo.greetings import say_goodbye, say_hello


def test_hello_greeting(capsys) -> None:
    """Expects a hello message."""

    say_hello()
    captured = capsys.readouterr()
    log.info(f"Test captured: {captured.out}")
    assert "hello" in captured.out.lower()


def test_goodbye_greeting(capsys) -> None:
    """Expects a goodbye message."""

    say_goodbye()
    captured = capsys.readouterr()
    log.info(f"Test captured: {captured.out}")
    assert "goodbye" in captured.out.lower()
