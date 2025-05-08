default_testsuite:='tests'

develop:
    uv run maturin develop

install:
    uv sync --group dev

doc:
    uv sync --group dev --group docs
    cd docs && uv run make html
    xdg-open docs/build/html/index.html

cleandoc:
    rm -rf docs/build
    rm -rf docs/source/develop

test testsuite=default_testsuite: develop
    uv run pytest -sxv {{testsuite}}

lf:
    uv run pytest --lf -vvv

fmt:
    uv run ruff check --fix .
    uv run ruff format src tests

release major_minor_patch: && changelog
    #!/bin/bash
    cargo release {{major_minor_patch}} --no-confirm --no-tag --no-push --no-publish --execute
    git reset --soft HEAD^
    export VERSION=$(head -n 10 Cargo.toml | grep version | sed 's/.*"\([^"]*\)".*/\1/')
    sed -i "s/version = \"\(.*\)\"/version = \"${VERSION}\"/" pyproject.toml
    uv sync

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(uv run scripts/get_version.py)"
    git push
    git tag "v$(uv run scripts/get_version.py)"
    git push origin "v$(uv run scripts/get_version.py)"
