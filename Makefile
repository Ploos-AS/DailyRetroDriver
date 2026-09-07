PYTHON ?= python3
ANSIBLE_PLAYBOOK ?= ansible-playbook
ANSIBLE_CONFIG := $(CURDIR)/ansible/ansible.cfg
ANSIBLE_LOCAL_TEMP ?= /tmp/retro-daily-driver-ansible
INVENTORY := ansible/inventory/hosts.example.yml
PLAYBOOK := ansible/playbooks/provision.yml
QUALIFICATION_OUTPUT ?= /srv/retro-daily-driver/reports/m1.1-pi400.json

.PHONY: check lint syntax test doctor qualify-pi400

check: lint syntax test
	$(PYTHON) -m compileall -q scripts tests
	@git diff --check

lint:
	$(PYTHON) scripts/validate-config
	$(PYTHON) scripts/check-repository

syntax:
	ANSIBLE_CONFIG=$(ANSIBLE_CONFIG) ANSIBLE_LOCAL_TEMP=$(ANSIBLE_LOCAL_TEMP) \
		$(ANSIBLE_PLAYBOOK) --syntax-check -i $(INVENTORY) $(PLAYBOOK)

test:
	$(PYTHON) -m unittest discover -s tests -v

doctor:
	./scripts/retro-doctor --repo-root .

qualify-pi400:
	$(PYTHON) scripts/retro-qualify-host --output $(QUALIFICATION_OUTPUT)
