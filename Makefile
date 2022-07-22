.PHONY: all help install venv test run login

## Add some environment variables
REGISTRY ?= us.icr.io
NAMESPACE ?= nyu_devops
IMAGE_NAME ?= shopcarts 
IMAGE_TAG ?= 1.0
IMAGE ?= $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)
# PLATFORM ?= "linux/amd64,linux/arm64"
PLATFORM ?= "linux/amd64"
CLUSTER ?= nyu-devops
RESOURCE_GROUP_ID ?= b6f897e8eb35445596abefc181e16f1a


help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-\\.]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

all: help

venv: ## Create a Python virtual environment
	$(info Creating Python 3 virtual environment...)
	python3 -m venv venv

install: ## Install dependencies
	$(info Installing dependencies...)
	sudo pip install -r requirements.txt

lint: ## Run the linter
	$(info Running linting...)
	flake8 service --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 service --count --max-complexity=10 --max-line-length=127 --statistics
	
test: ## Run the unit tests
	$(info Running tests...)
	flask create-db
	nosetests
	# nosetests --with-spec --spec-color

run: ## Run the service
	$(info Starting service...)
	honcho start

login: ## Login to ibm cloud
	$(info Logging into IBM Cloud cluster $(CLUSTER)...)
	ibmcloud login -a cloud.ibm.com -g $(RESOURCE_GROUP_ID) -r us-south --apikey @~/apikey.json
	ibmcloud cr login
	ibmcloud ks cluster config --cluster $(CLUSTER)
	kubectl cluster-info
