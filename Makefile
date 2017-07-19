name=gunilla
version=0.1.0.dev1
dist_file = dist/$(name)-$(version).tar.gz

all : $(dist_file)

build :
	cd src; python setup.py sdist --dist-dir=../dist

install : build
	pip install $(dist_file) --upgrade
	rm -rf src/build/ src/dist/ src/*.egg-info

clean :
	rm -rf dist

uninstall :
	pip uninstall $(name)
