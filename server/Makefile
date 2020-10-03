SERVICE := eink-display-server
IMAGE := applepunk/$(SERVICE)

# Registry credentials
export REGISTRY_USER
export REGISTRY_PASSWORD

login:
	@docker login -u="$(REGISTRY_USER)" -p="$(REGISTRY_PASSWORD)"

image:
	@docker build . -t $(IMAGE):latest

push: image login
	@docker push $(IMAGE):latest

local: image
	@docker run --rm \
		-p 5000:5000 \
		--name=$(SERVICE) $(IMAGE) \
		bash -c "flask run -h 0.0.0.0"
