init:
	# Deploy MetaController to cluster
	@git clone https://github.com/GoogleCloudPlatform/metacontroller.git ./opt/metacontroller
	@kubectl apply -f ./opt/metacontroller/manifests/

dev:
	@skaffold dev

dshell:
	@docker-compose run --rm --entrypoint=bash python
