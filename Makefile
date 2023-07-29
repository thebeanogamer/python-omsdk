spec := python-omsdk.spec

srpm:
	cp setup-omsdk.py.patch `rpmbuild --eval "%{_topdir}"`/SOURCES
	@set -e; rpmbuild -bs --define "_disable_source_fetch 0" $(spec)
ifdef outdir
	cp `rpmbuild --eval "%{_topdir}"`/SRPMS/* $(outdir)
endif
