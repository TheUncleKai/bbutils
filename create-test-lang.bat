@echo off

SET PO_EN=tests\locales\en\LC_MESSAGES\test.po
SET PO_DE=tests\locales\de\LC_MESSAGES\test.po

SET MO_EN=tests\locales\en\LC_MESSAGES\test.mo
SET MO_DE=tests\locales\de\LC_MESSAGES\test.mo

SET TEST_POT=tests\locales\test.pot


xgettext -L python -d test -o tests\locales\test1.pot testdata\testlang\test1\__init__.py
xgettext -L python -d test -o tests\locales\tester.pot testdata\testlang\test1\tester.py

msgcat tests\locales\test1.pot tests\locales\tester.pot -o %TEST_POT%

IF EXIST %PO_EN% (
    msgmerge -N -U %PO_EN% %TEST_POT%
) ELSE (
    copy %TEST_POT% %PO_EN%
)

IF EXIST %PO_DE% (
    msgmerge -N -U %PO_DE% %TEST_POT%
) ELSE (
    copy %TEST_POT% %PO_DE%
)

msgfmt -o %MO_DE% %PO_DE%
msgfmt -o %MO_EN% %PO_EN%
