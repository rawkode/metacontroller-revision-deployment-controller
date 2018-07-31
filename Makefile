.PHONY: test
USER_ID  = $(shell id -u)

init:
	# Deploy MetaController to cluster
	@git clone https://github.com/GoogleCloudPlatform/metacontroller.git ./opt/metacontroller
	@kubectl apply -f ./opt/metacontroller/manifests/

clean:
	@pipenv --rm

deps:
	@pipenv install --dev

test:
	@pytest

dev:
	@skaffold dev

dshell:
	@docker-compose run --rm --user ${USER_ID} --entrypoint=bash python --norc --noprofile

dclean:
	@docker-compose run --rm --entrypoint=pipenv python --rm
