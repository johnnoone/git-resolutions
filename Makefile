
build:
	python -m zipapp src -p "/usr/bin/env python" -m "git_resolutions:main" -o git-resolutions
	chmod +x git-resolutions

install: build
	./git-resolutions --install

publish: install
	./git-resolutions --publish
