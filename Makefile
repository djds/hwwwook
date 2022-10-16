DOCKER ?= podman
IMAGE  ?= localhost:5000/hwwwook

# reproductible builds: https://reproducible-builds.org/docs/source-date-epoch/
build: clean
	SOURCE_DATE_EPOCH=$(shell git log -1 --pretty=%ct) python3 -m build

install:
	pip install dist/hwwwook-*-py3-none-any.whl

clean:
	rm -rf dist/
	find . -type d -name '*\.egg-info' -exec rm -rf "{}" +

image:
	$(DOCKER) build --tag $(IMAGE) --file Containerfile .
