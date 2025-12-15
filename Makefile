.DEFAULT_GOAL := help
.PHONY: help build-sources build-static build dev run clean

help:
	@echo 'Available targets:'
	@echo '  build-sources - Build the sources from the raw .md files. See ./main.py for more details'
	@echo '  build-static  - Build static files using Vitepress'
	@echo '  build         - Build sources and static files'
	@echo '  dev           - Build sources and run the development server'
	@echo '  run           - Run the development server'
	@echo '  clean         - Clean the built files'

build-sources:
	@python main.py \
            --ignored-dirs '.obsidian,.git' \
            --verbose \
            --base-dir . \
            --source-dir sources \
            --target-dir build \
            --template-dir templates
	@mv build/links.json .vitepress/links.json

build-static:
	@npm run docs:build

build: build-sources build-static

dev: build-sources
	@npm run docs:dev

run:
	@npm run docs:dev

clean:
	@rm -rf build
	@rm -rf .vitepress/dist
	@rm -rf .vitepress/links.json
