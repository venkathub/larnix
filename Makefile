NODE ?= node

.PHONY: build check serve
build:
	python3 scripts/build_site.py

check:
	python3 scripts/curriculum.py check
	$(NODE) --test tests/platform.test.cjs samples/vector-similarity/tests/vector-math.test.cjs samples/rag-grounding/tests/rag-engine.test.cjs samples/agent-recovery/tests/recovery-engine.test.cjs
	$(NODE) --check web/app.js
	$(NODE) --check web/lesson-shell.js
	$(NODE) --check samples/shared/lesson-ui.js
	$(NODE) --check samples/shared/notebook.js
	$(NODE) --check samples/vector-similarity/lesson.js
	$(NODE) --check samples/rag-grounding/lesson.js
	$(NODE) --check samples/agent-recovery/lesson.js
	python3 -m unittest discover -s tests -p 'test_*.py'

serve: build
	python3 -m http.server 8775 --bind 127.0.0.1 --directory dist
