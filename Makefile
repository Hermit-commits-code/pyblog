NEWPOST_TITLE ?= "New Post"

.PHONY: new-post
new-post:
	python scripts/new_post.py $(title)
