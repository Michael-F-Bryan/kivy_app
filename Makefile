PYTHON = python3

commit:
	git add -u
	git commit --verbose

.PHONY: run commit
