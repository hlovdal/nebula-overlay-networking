# https://docs.pagure.org/copr.copr/user_documentation.html#make-srpm

# make -f <cloned_repodir>/.copr/Makefile srpm outdir="<outdir>" spec="<spec_path>"

srpm:
	if [ $$(id -u) -eq 0 ]; then dnf install -y rpmdevtools; fi
	./.copr/download_source_files.sh SPECS/nebula-overlay-networking.spec SOURCES
	./.copr/build.sh SPECS/nebula-overlay-networking.spec $(outdir)
