name=gunilla
version=0.2.0.dev1
dist_file = dist/$(name)-$(version).tar.gz

all : $(dist_file)

build : $(dist_file)

$(dist_file) :
	cd src; python setup.py sdist --dist-dir=../dist

install : $(dist_file)
	pip install $(dist_file) --upgrade

clean :
	rm -rf dist

uninstall :
	pip uninstall $(name)
