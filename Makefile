##
# spaCy Service
#
# @file
# @version 0.1


help:  ## show Makefile help
	@grep ":.*##" $(MAKEFILE_LIST) | grep -v MAKEFILE_LIST | sed "s/:.*##/\t/" | column -t -s"	"

CLEAN :=
venv := venv
python := $(venv)/bin/python
pip := $(python) -m pip

notebook: .dev  ## launch Jupyter Lab
	$(python) -m jupyterlab

CLEAN := $(venv) $(CLEAN)
$(python):
  # Special case, directory isn't a good make target
	python -m venv $(venv)
	$(pip) install -U pip pip-tools~=6.0

requirement%.txt: requirement%.in $(python)
	$(venv)/bin/pip-compile $<

CLEAN := .dev $(CLEAN)
.dev: requirements.txt
	$(pip) install -r $<
	touch $@

dev: .dev  ## run dev server
	$(python) -m uvicorn main:app --reload

clean:  ## clean all intermediate targets
	rm -rf $(CLEAN)


# end
