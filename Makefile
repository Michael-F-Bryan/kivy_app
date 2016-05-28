RM = rm -rf
source = $(wildcard *.py *.kv)
cookie = bin/cookie


serve: build
	@buildozer android serve || exit 0

deploy: build
	@echo Please plug your android phone in
	@echo
	buildozer android deploy

build: $(cookie)

$(cookie): $(source)
	buildozer android debug
	touch $(cookie)

commit:
	git add -u
	git commit --verbose

clean:
	$(RM) ./bin/*

.PHONY: commit clean
