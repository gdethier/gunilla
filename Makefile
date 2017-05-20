wplab_exec = wplab
install_dir = /usr/local/bin
theme_builder_dist = dist/wplab-theme-builder-0.1.0.dev1.tar.gz

all : $(wplab_exec) $(theme_builder_dist)

$(theme_builder_dist) :
	cd src; python setup.py sdist --dist-dir=../dist

install : $(wplab_exec) $(theme_builder_dist)
	cp $(wplab_exec) $(install_dir)/
	chmod a+rx $(install_dir)/$(wplab_exec)
	cd src; python setup.py install
	cd src; rm -rf build/ dist/ *.egg-info

uninstall :
	rm $(install_dir)/$(wplab_exec)

clean :
	rm -rf dist
