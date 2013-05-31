GIT_COMMIT ?= HEAD
BUILD_NUMBER ?= 0
PKG_NAME := $(shell grep Package DEBIAN/control | awk '{ print $$2 }')
DISTRIBUTION = $(shell cat /etc/lsb-release | grep DISTRIB_CODENAME | cut -d '=' -f 2)
PKG_VERSION_DATE = $(shell date +%Y%m%d -u)
PKG_VERSION_GIT = $(shell git rev-list $(GIT_COMMIT) --abbrev-commit --max-count 1)
PKG_VERSION := $(PKG_VERSION_DATE)-$(BUILD_NUMBER)-$(PKG_VERSION_GIT)
PKG_ARCH := $(shell grep Architecture DEBIAN/control | awk '{ print $$2 }')
PKG := $(PKG_NAME)_$(PKG_VERSION)_$(DISTRIBUTION)_$(PKG_ARCH).deb

BUILD := ./build

all: clean $(PKG)

clean:
	rm -rf $(BUILD)
	rm -f $(PKG_NAME)*.deb

$(PKG): $(BUILD)/DEBIAN/control \
        $(BUILD)/DEBIAN/postinst \
        $(BUILD)/DEBIAN/conffiles \
        $(BUILD)/etc/get-out/config \
        $(BUILD)/etc/init/get-out.conf \
	$(BUILD)/usr/bin/get-out
	fakeroot -- dpkg-deb -z 9 --build $(BUILD) $@

$(BUILD)/DEBIAN/control: DEBIAN/control
	sed s/VERSION_PLACEHOLDER/$(PKG_VERSION)/ $< > $<.out
	install -D -m 0644 $<.out $@
	rm $<.out

$(BUILD)/DEBIAN/postinst: DEBIAN/postinst
	install -D -m 755 $< $@

$(BUILD)/DEBIAN/conffiles: DEBIAN/conffiles
	install -D -m 0644 $< $@

$(BUILD)/etc/get-out/config: config.default
	install -D -m 0644 $< $@

$(BUILD)/etc/init/get-out.conf: upstart.conf
	install -D -m 0644 $< $@

$(BUILD)/usr/bin/get-out: setup.py
	python $< install --install-layout=deb --prefix=/usr --root=$(BUILD)
