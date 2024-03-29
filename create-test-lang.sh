#!/bin/bash

PO_EN=tests/locales/en/LC_MESSAGES/test.po
PO_DE=tests/locales/de/LC_MESSAGES/test.po

MO_EN=tests/locales/en/LC_MESSAGES/test.mo
MO_DE=tests/locales/de/LC_MESSAGES/test.mo

TEST_POT=tests/locales/test.pot

xgettext -L python -d test -o tests/locales/test1.pot testdata/testlang/test1/__init__.py
xgettext -L python -d test -o tests/locales/tester.pot testdata/testlang/test1/tester.py

msgcat tests/locales/test1.pot tests/locales/tester.pot -o $TEST_POT

if [ ! -f "$PO_EN" ]; then
    cp $TEST_POT $PO_EN
fi

if [ ! -f "$PO_DE" ]; then
    cp $TEST_POT $PO_DE
fi

if [ -f "$PO_EN" ]; then
    msgmerge -N -U $PO_EN $TEST_POT
fi

if [ -f "$PO_DE" ]; then
    msgmerge -N -U $PO_DE $TEST_POT
fi

msgfmt -o $MO_DE $PO_DE
msgfmt -o $MO_EN $PO_EN
