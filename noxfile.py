"""
Contains nox sessions.
"""

import nox

@nox.session
def tests(session):
    """
    Run tests.
    """
    session.run("poetry", "install", "-E", "pandas", external=True)
    session.run("pytest")

@nox.session
def lint(session):
    """
    Run linter.
    """
    session.run("poetry", "install", "-E", "pandas", external=True)
    session.run("pylint", "qvd4nifi", "tests")

@nox.session
def build(session):
    """
    Build package.
    """
    session.run("poetry", "build", external=True)

@nox.session
def nar(session):
    """
    Build NAR package.
    """
    session.run("python", "scripts/build_nar.py", external=True)
