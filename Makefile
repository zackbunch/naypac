
define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help:
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)


lint:  ## Lint and static-check
	black nay
	flake8 nay


push:  ## Push code with tags
	git push && git push --tags

test:  ## Run tests
	pytest -ra