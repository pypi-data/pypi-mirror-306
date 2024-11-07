#!/usr/bin/make

PACKAGE         := tiramisu
ifeq ($(PACKAGE_DST),)
PACKAGE_DST             := $(PACKAGE)
endif

INSTALL         := install
INSTALL_DATA    := install -m 644
INSTALL_PROGRAM := install -m 755
INSTALL_DIR     := install -m 755 -d

TRADUC_DIR       = tiramisu/locale
TRADUC_DEST	 = $(DESTDIR)/usr/share/locale

PYTHON_OPTS      =
ifneq ($(DESTDIR),)
PYTHON_OPTS     += --root $(DESTDIR)
endif

VERSION			:=	`cat VERSION`

define gettext
    if command -v pygettext >/dev/null 2>&1 ; then \
        P="pygettext" ; \
    else \
	    P="pygettext.py" ; \
    fi ; \
	$$P -p $(TRADUC_DIR)/ -o $(PACKAGE).pot `find $(PACKAGE)/ -name "*.py"`
endef

# Build translation files
define build_translation
    if [ -d ${1} ]; then                                            \
	for f in `find ${1} -name "*.po"`; do                       \
	    msgfmt -o `dirname $$f`/`basename $$f ".po"`.mo $$f || true; \
	done;                                                       \
    fi
endef



# Install Traduction
define install_translation
    if [ -d ${1} ]; then                          \
	for file in `find ${1} -name "*.mo"`; do  \
	   $(INSTALL_DIR) $(TRADUC_DEST)/`echo $$file | cut -d '/' -f 2` || true;                     \
	   $(INSTALL_DIR) $(TRADUC_DEST)/`echo $$file | cut -d '/' -f 2`/LC_MESSAGES || true;         \
	   $(INSTALL_DATA) $$file $(TRADUC_DEST)/`echo $$file | cut -d '/' -f 2`/LC_MESSAGES/$(PACKAGE_DST).mo || true; \
	done;                                     \
    fi
endef

all: build-lang

clean:
	$(RM) -r build
	$(RM) -r $(PACKAGE).egg-info/
	$(RM) -r $(TRADUC_DIR)/*/*.mo

#test: clean
#	py.test

# Build or update Portable Object Base Translation for gettext

build-pot:
	$(call gettext)

build-lang:
	$(call build_translation, $(TRADUC_DIR))

# install-lang:
# 	$(INSTALL_DIR) $(TRADUC_DEST)
# 	$(call install_translation, $(TRADUC_DIR))

install: # install-lang
	python3 setup.py install --no-compile $(PYTHON_OPTS)

dist:
	git archive --format=tar --prefix $(PACKAGE)-$(VERSION)/ HEAD | gzip -9 > $(PACKAGE)-$(VERSION).tar.gz

# List in .PHONY to force generation at each call
.PHONY: all clean build-pot build-lang install-lang install dist
