PYTHON = python3

run:
	$(PYTHON) main.py

commit:
	git add -u
	git commit --verbose

.PHONY: run commit
