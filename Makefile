
build:
	python -m zipapp src -p "/usr/bin/env python" -m "git_conflict:main" -o git-conflict
	chmod +x git-conflict

install: build
	./git-conflict --install

publish: install
	./git-conflict --publish
