gunilla_exec = gnl
install_dir = /usr/local/bin
gunilla_dist = dist/gunilla-0.1.0.dev1.tar.gz

all : $(gunilla_exec) $(gunilla_dist)

$(gunilla_dist) :
	cd src; python setup.py sdist --dist-dir=../dist

install : $(gunilla_exec) $(gunilla_dist)
	cp $(gunilla_exec) $(install_dir)/
	chmod a+rx $(install_dir)/$(gunilla_exec)
	cd src; python setup.py install
	cd src; rm -rf build/ dist/ *.egg-info

uninstall :
	rm $(install_dir)/$(gunilla_exec)

clean :
	rm -rf dist
