"""Modular tutorial question-answering agent."""

__all__ = ["answer_question", "reindex_tutorial"]


def answer_question(*args, **kwargs):  # pragma: no cover - thin wrapper
    from .main import answer_question as _answer
    return _answer(*args, **kwargs)


def reindex_tutorial(*args, **kwargs):  # pragma: no cover - thin wrapper
    from .reindex import reindex_tutorial as _reindex
    return _reindex(*args, **kwargs)
