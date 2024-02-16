PLATFORM=
TENANT=
DOCKER_REPO_URL=registry.cp.kpn-dsh.com/$(TENANT)
VERSION=
tagname=pylog-generator
tenantuserid=
image=$(DOCKER_REPO_URL)/$(tagname):$(VERSION)
PORT_INTERNAL=3000
PORT_EXTERNAL=3000

help:
	@echo "login   - login to the relevant repository"
	@echo "fix     - run dos2unix on every file"
	@echo "build   - build the image"
	@echo "rebuild - build the image with the --no-cache flag"
	@echo "itgo    - shorthand for fix, build, push, show"
	@echo "run     - run the image in local docker"
	@echo "push    - push the  image to jfrog"
	@echo "show    - show the current make variables"
login:
	docker login $(DOCKER_REPO_URL)
fix:
	find . -type f -print0 | xargs -0 dos2unix
build:
	docker build --platform linux/amd64 -t $(tagname) -f Dockerfile --build-arg tenantuserid=$(tenantuserid) .
	docker tag  $(tagname) $(image)
rebuild:
	docker build --platform linux/amd64 --no-cache -t $(tagname) -f Dockerfile --build-arg tenantuserid=$(tenantuserid) .
	docker tag  $(tagname) $(image)
all:
	make build
	make push
	make show
run:
	docker run --platform linux/amd64 -u $(tenantuserid):$(tenantuserid) -it --entrypoint "/bin/sh" $(image)
fun:
	curl -H "Accept: application/json" https://icanhazdadjoke.com/
push:
	docker push $(image)
show:
	@echo "#make file configuration"
	@echo "#URL          :" $(DOCKER_REPO_URL)
	@echo "#PLATFORM     :" $(PLATFORM)
	@echo "#TENANT       :" $(TENANT)
	@echo "#tenantuserid :" $(tenantuserid)
	@echo "#tagname      :" $(tagname)
	@echo "#version      :" $(VERSION)
	@echo "#image        :" $(image)
