# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = rp-pppoe
VERSION = 3.10

DIR = $(PACKAGE)-$(VERSION)/src

BASE_URL = http://www.roaringpenguin.com/files/download/

INSTALL = yes
CLEAN = yes

install: compile
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/sbin
	@install -D $(DIR)/pppoe $(PKG_ROOT)$(PKG_DIR)/sbin/pppoe

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(PACKAGE)-$(VERSION)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif
	
include ../Makefile.rules
