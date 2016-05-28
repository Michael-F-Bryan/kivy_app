PYTHON = python3


serve: build
	buildozer android-new serve

deploy: build
	buildozer android-new deploy

build:
	buildozer android-new debug

commit:
	git add -u
	git commit --verbose

.PHONY: deploy commit
