#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysmi/license.html
#
import sys
import textwrap

try:
    import unittest2 as unittest

except ImportError:
    import unittest

from pysmi.parser.smi import parserFactory
from pysmi.codegen.pysnmp import PySnmpCodeGen
from pysmi.codegen.symtable import SymtableCodeGen
from pyasn1.type.constraint import ValueSizeConstraint
from pyasn1.type.namedval import NamedValues
from pysnmp.smi.builder import MibBuilder
from pysnmp.smi.view import MibViewController


class TypeDeclarationTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS

      IpAddress,
      Counter32,
      Gauge32,
      TimeTicks,
      Opaque,
      Integer32,
      Unsigned32,
      Counter64
        FROM SNMPv2-SMI

      TEXTUAL-CONVENTION
        FROM SNMPv2-TC;

    -- simple types
    TestTypeInteger ::= INTEGER
    TestTypeOctetString ::= OCTET STRING
    TestTypeObjectIdentifier ::= OBJECT IDENTIFIER

    -- application types
    TestTypeIpAddress ::= IpAddress
    TestTypeInteger32 ::= Integer32
    TestTypeCounter32 ::= Counter32
    TestTypeGauge32 ::= Gauge32
    TestTypeTimeTicks ::= TimeTicks
    TestTypeOpaque ::= Opaque
    TestTypeCounter64 ::= Counter64
    TestTypeUnsigned32 ::= Unsigned32

    -- constrained subtypes

    TestTypeEnum ::= INTEGER {
                        noResponse(-1),
                        noError(0),
                        tooBig(1)
                    }
    TestTypeSizeRangeConstraint ::= OCTET STRING (SIZE (0..255))
    TestTypeSizeConstraint ::= OCTET STRING (SIZE (8 | 11))
    TestTypeRangeConstraint ::= INTEGER (0..2)
    TestTypeSingleValueConstraint ::= INTEGER (0|2|4)

    TestTypeBits ::= BITS {
                        sunday(0),
                        monday(1),
                        tuesday(2),
                        wednesday(3),
                        thursday(4),
                        friday(5),
                        saturday(6)
                    }


    TestTextualConvention ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "1x:"
        STATUS       current
        DESCRIPTION
                "Test TC"
        REFERENCE
                "Test reference"
        SYNTAX       OCTET STRING

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()
        mibBuilder.loadTexts = True

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

        self.mibViewController = MibViewController(mibBuilder)

    def protoTestSymbol(self, symbol, klass):
        self.assertTrue(symbol in self.ctx, f"symbol {symbol} not present")

    def protoTestClass(self, symbol, klass):
        self.assertEqual(
            self.ctx[symbol].__bases__[0].__name__,
            klass,
            f"expected class {klass}, got {self.ctx[symbol].__bases__[0].__name__} at {symbol}",
        )

    def protoTestExport(self, symbol, klass):
        self.assertEqual(
            self.mibViewController.getTypeName(symbol),
            ("TEST-MIB", symbol),
            f"Symbol {symbol} not exported",
        )

    def testTextualConventionSymbol(self):
        self.assertTrue("TestTextualConvention" in self.ctx, "symbol not present")

    def testTextualConventionDisplayHint(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getDisplayHint(),
            "1x:",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionStatus(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getStatus(), "current", "bad STATUS"
        )

    def testTextualConventionDescription(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getDescription(),
            "Test TC",
            "bad DESCRIPTION",
        )

    def testTextualConventionReference(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getReference(),
            "Test reference",
            "bad REFERENCE",
        )

    def testTextualConventionClass(self):
        self.assertTrue(
            issubclass(
                self.ctx["TestTextualConvention"], self.ctx["TextualConvention"]
            ),
            "bad SYNTAX class",
        )

    def testTextualConventionExport(self):
        self.assertEqual(
            self.mibViewController.getTypeName("TestTextualConvention"),
            ("TEST-MIB", "TestTextualConvention"),
            f"not exported",
        )


# populate test case class with per-type methods

typesMap = (
    # TODO: Integer/Integer32?
    ("TestTypeInteger", "Integer32"),
    ("TestTypeOctetString", "OctetString"),
    ("TestTypeObjectIdentifier", "ObjectIdentifier"),
    ("TestTypeIpAddress", "IpAddress"),
    ("TestTypeInteger32", "Integer32"),
    ("TestTypeCounter32", "Counter32"),
    ("TestTypeGauge32", "Gauge32"),
    ("TestTypeTimeTicks", "TimeTicks"),
    ("TestTypeOpaque", "Opaque"),
    ("TestTypeCounter64", "Counter64"),
    ("TestTypeUnsigned32", "Unsigned32"),
    ("TestTypeTestTypeEnum", "Integer32"),
    ("TestTypeSizeRangeConstraint", "OctetString"),
    ("TestTypeSizeConstraint", "OctetString"),
    ("TestTypeRangeConstraint", "Integer32"),
    ("TestTypeSingleValueConstraint", "Integer32"),
)


def decor(func, symbol, klass):
    def inner(self):
        func(self, symbol, klass)

    return inner


for s, k in typesMap:
    setattr(
        TypeDeclarationTestCase,
        "testTypeDeclaration" + k + "SymbolTestCase",
        decor(TypeDeclarationTestCase.protoTestSymbol, s, k),
    )
    setattr(
        TypeDeclarationTestCase,
        "testTypeDeclaration" + k + "ClassTestCase",
        decor(TypeDeclarationTestCase.protoTestClass, s, k),
    )
    setattr(
        TypeDeclarationTestCase,
        "testTypeDeclaration" + k + "ExportTestCase",
        decor(TypeDeclarationTestCase.protoTestExport, s, k),
    )


# XXX constraints flavor not checked


class TypeDeclarationHyphenTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      Unsigned32
        FROM SNMPv2-SMI
      TEXTUAL-CONVENTION
        FROM SNMPv2-TC;

    Test-Textual-Convention ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "d-2"
        STATUS       current
        DESCRIPTION  "Test TC"
        SYNTAX       Unsigned32

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

        self.mibViewController = MibViewController(mibBuilder)

    def testTextualConventionSymbol(self):
        self.assertTrue("Test_Textual_Convention" in self.ctx, "symbol not present")

    def testTextualConventionExport(self):
        self.assertEqual(
            self.mibViewController.getTypeName("Test-Textual-Convention"),
            ("TEST-MIB", "Test-Textual-Convention"),
            f"Symbol not exported",
        )

    def testTextualConventionDisplayHint(self):
        self.assertEqual(
            self.ctx["Test_Textual_Convention"]().getDisplayHint(),
            "d-2",
            "bad DISPLAY-HINT",
        )


class TypeDeclarationTextTestCase(unittest.TestCase):
    R"""
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      Unsigned32
        FROM SNMPv2-SMI
      TEXTUAL-CONVENTION
        FROM SNMPv2-TC;

    TestTextualConvention ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "semantically
    invalid"
        STATUS       obsolete
        DESCRIPTION  "Test\n TC\"
        REFERENCE
    "\Test
      reference\\"
        SYNTAX       Unsigned32

    END
    """

    def setUp(self):
        docstring = textwrap.dedent(self.__class__.__doc__)
        ast = parserFactory()().parse(docstring)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast,
            {mibInfo.name: symtable},
            genTexts=True,
            textFilter=lambda symbol, text: text,
        )
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()
        mibBuilder.loadTexts = True

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testTextualConventionSymbol(self):
        self.assertTrue("TestTextualConvention" in self.ctx, "symbol not present")

    def testTextualConventionStatus(self):
        # Use a value other than "current" in this test, as "current" is the
        # default pysnmp value (which could mean the test value was never set).
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getStatus(), "obsolete", "bad STATUS"
        )

    def testTextualConventionDisplayHint(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getDisplayHint(),
            "semantically\ninvalid",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionDescription(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getDescription(),
            "Test\\n TC\\",
            "bad DESCRIPTION",
        )

    def testTextualConventionReference(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getReference(),
            "\\Test\n  reference\\\\",
            "bad REFERENCE",
        )


class TypeDeclarationNoLoadTextsTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      Unsigned32
        FROM SNMPv2-SMI
      TEXTUAL-CONVENTION
        FROM SNMPv2-TC;

    TestTextualConvention ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "d-2"
        STATUS       deprecated
        DESCRIPTION  "Test TC"
        REFERENCE    "Test reference"
        SYNTAX       Unsigned32

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {}, genTexts=True)
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(
            ast, {mibInfo.name: symtable}, genTexts=True
        )
        codeobj = compile(pycode, "test", "exec")

        self.ctx = {"mibBuilder": MibBuilder()}

        exec(codeobj, self.ctx, self.ctx)

    def testTextualConventionDisplayHint(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getDisplayHint(),
            "d-2",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionStatus(self):
        # Unlike all other classes, TextualConvention does take on the status
        # even if generating and loading texts is disabled.
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getStatus(), "deprecated", "bad STATUS"
        )

    def testTextualConventionDescription(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getDescription(),
            "",
            "bad DESCRIPTION",
        )

    def testTextualConventionReference(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().getReference(),
            "",
            "bad REFERENCE",
        )


# Note that the following test case verifies leniency with respect to deriving
# textual conventions from other textual conventions, which is disallowed per
# RFC 2579 Sec. 3.5, but widely used in the real world.
class TypeDeclarationInheritanceTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI
      TEXTUAL-CONVENTION
        FROM SNMPv2-TC;

    TestTypeInteger ::= INTEGER

    --
    -- without constraints
    --

    -- textual convention derived from base type
    TestTC-B ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "d-1"
        STATUS       current
        DESCRIPTION  "Test TC 1"
        SYNTAX       INTEGER

    -- textual convention for simple type, derived from base type
    TestTC-SB ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "d-2"
        STATUS       current
        DESCRIPTION  "Test TC 2"
        SYNTAX       TestTypeInteger

    -- textual convention for textual convention, derived from base type
    TestTC-TB ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "d-3"
        STATUS       current
        DESCRIPTION  "Test TC 3"
        SYNTAX       TestTC-B

    -- textual convention for textual convention, derived from simple type,
    -- in turn derived from base type
    TestTC-TSB ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "d-4"
        STATUS       current
        DESCRIPTION  "Test TC 4"
        SYNTAX       TestTC-SB

    -- textual convention for textual convention, derived from textual
    -- convention, in turn derived from base type
    TestTC-TTB ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "d-5"
        STATUS       current
        DESCRIPTION  "Test TC 5"
        SYNTAX       TestTC-TB

    --
    -- with constraints
    --

    TestTypeRangedOctetString ::= OCTET STRING (SIZE (0..255))

    -- textual convention derived from base type
    TestTC-C ::= TEXTUAL-CONVENTION
        STATUS       current
        DESCRIPTION  "Test TC 6"
        SYNTAX       OCTET STRING (SIZE (0..63))

    -- textual convention for simple type, derived from constrained type
    TestTC-SC ::= TEXTUAL-CONVENTION
        STATUS       current
        DESCRIPTION  "Test TC 7"
        SYNTAX       TestTypeRangedOctetString

    -- textual convention for textual convention, derived from constrained type
    TestTC-TC ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "1x:"
        STATUS       current
        DESCRIPTION  "Test TC 8"
        SYNTAX       TestTC-C (SIZE (16..31))

    -- textual convention for textual convention, derived from simple type,
    -- in turn derived from constrained type
    TestTC-TSC ::= TEXTUAL-CONVENTION
        DISPLAY-HINT "2x:"
        STATUS       current
        DESCRIPTION  "Test TC 9"
        SYNTAX       TestTC-SC (SIZE (32..47))

    -- textual convention for textual convention, derived from textual
    -- convention, in turn derived from base type
    TestTC-TTC ::= TEXTUAL-CONVENTION
        STATUS       current
        DESCRIPTION  "Test TC 10"
        SYNTAX       TestTC-TC (SIZE (20..23))

    --
    -- test objects (without constraints only)
    --

    testObjectB OBJECT-TYPE
        SYNTAX       TestTC-B
        MAX-ACCESS   read-only
        STATUS       current
        DESCRIPTION  "Test object"
        DEFVAL       { 123456 }
      ::= { 1 4 1 }

    testObjectSB OBJECT-TYPE
        SYNTAX       TestTC-SB
        MAX-ACCESS   read-only
        STATUS       current
        DESCRIPTION  "Test object"
        DEFVAL       { 123456 }
      ::= { 1 4 2 }

    testObjectTB OBJECT-TYPE
        SYNTAX       TestTC-TB
        MAX-ACCESS   read-only
        STATUS       current
        DESCRIPTION  "Test object"
        DEFVAL       { 123456 }
      ::= { 1 4 3 }

    testObjectTSB OBJECT-TYPE
        SYNTAX       TestTC-TSB
        MAX-ACCESS   read-only
        STATUS       current
        DESCRIPTION  "Test object"
        DEFVAL       { 123456 }
      ::= { 1 4 4 }

    testObjectTTB OBJECT-TYPE
        SYNTAX       TestTC-TTB
        MAX-ACCESS   read-only
        STATUS       current
        DESCRIPTION  "Test object"
        DEFVAL       { 123456 }
      ::= { 1 4 5 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testTextualConventionDisplayHintB(self):
        self.assertEqual(
            self.ctx["TestTC_B"]().getDisplayHint(),
            "d-1",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionDisplayHintSB(self):
        self.assertEqual(
            self.ctx["TestTC_SB"]().getDisplayHint(),
            "d-2",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionDisplayHintTB(self):
        self.assertEqual(
            self.ctx["TestTC_TB"]().getDisplayHint(),
            "d-3",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionDisplayHintTSB(self):
        self.assertEqual(
            self.ctx["TestTC_TSB"]().getDisplayHint(),
            "d-4",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionDisplayHintTTB(self):
        self.assertEqual(
            self.ctx["TestTC_TTB"]().getDisplayHint(),
            "d-5",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionValueRangeConstraintC(self):
        self.assertTrue(
            ValueSizeConstraint(0, 63)
            in self.ctx["TestTC_C"]().getSubtypeSpec().getValueMap(),
            "missing value size constraint",
        )

    def testTextualConventionDisplayHintC(self):
        self.assertEqual(
            self.ctx["TestTC_C"]().getDisplayHint(),
            "",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionValueRangeConstraintSC(self):
        self.assertTrue(
            ValueSizeConstraint(0, 255)
            in self.ctx["TestTC_SC"]().getSubtypeSpec().getValueMap(),
            "missing value size constraint",
        )

    def testTextualConventionDisplayHintSC(self):
        self.assertEqual(
            self.ctx["TestTC_SC"]().getDisplayHint(),
            "",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionValueRangeConstraintTC(self):
        self.assertTrue(
            ValueSizeConstraint(16, 31)
            in self.ctx["TestTC_TC"]().getSubtypeSpec().getValueMap(),
            "missing value size constraint",
        )

    def testTextualConventionDisplayHintTC(self):
        self.assertEqual(
            self.ctx["TestTC_TC"]().getDisplayHint(),
            "1x:",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionValueRangeConstraintTSC(self):
        self.assertTrue(
            ValueSizeConstraint(32, 47)
            in self.ctx["TestTC_TSC"]().getSubtypeSpec().getValueMap(),
            "missing value size constraint",
        )

    def testTextualConventionDisplayHintTSC(self):
        self.assertEqual(
            self.ctx["TestTC_TSC"]().getDisplayHint(),
            "2x:",
            "bad DISPLAY-HINT",
        )

    def testTextualConventionValueRangeConstraintTTC(self):
        self.assertTrue(
            ValueSizeConstraint(20, 23)
            in self.ctx["TestTC_TTC"]().getSubtypeSpec().getValueMap(),
            "missing value size constraint",
        )

    def testTextualConventionDisplayHintTTC(self):
        self.assertEqual(
            self.ctx["TestTC_TTC"]().getDisplayHint(),
            "1x:",
            "bad DISPLAY-HINT",
        )

    def testObjectTypePrettyValueB(self):
        self.assertEqual(
            self.ctx["testObjectB"].getSyntax().prettyPrint(), "12345.6", "bad DEFVAL"
        )

    def testObjectTypePrettyValueSB(self):
        self.assertEqual(
            self.ctx["testObjectSB"].getSyntax().prettyPrint(), "1234.56", "bad DEFVAL"
        )

    def testObjectTypePrettyValueTB(self):
        self.assertEqual(
            self.ctx["testObjectTB"].getSyntax().prettyPrint(), "123.456", "bad DEFVAL"
        )

    def testObjectTypePrettyValueTSB(self):
        self.assertEqual(
            self.ctx["testObjectTSB"].getSyntax().prettyPrint(), "12.3456", "bad DEFVAL"
        )

    def testObjectTypePrettyValueTTB(self):
        self.assertEqual(
            self.ctx["testObjectTTB"].getSyntax().prettyPrint(), "1.23456", "bad DEFVAL"
        )


class TypeDeclarationBitsTextualConventionSyntaxTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI
      TEXTUAL-CONVENTION
        FROM SNMPv2-TC;

    TestTextualConvention ::= TEXTUAL-CONVENTION
        STATUS       current
        DESCRIPTION  "Test TC"
        SYNTAX       BITS { value(0), otherValue(1) }

    testObject OBJECT-TYPE
        SYNTAX       TestTextualConvention
        MAX-ACCESS   read-only
        STATUS       current
        DESCRIPTION  "Test object"
      ::= { 1 4 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testTextualConventionNamedValues(self):
        self.assertEqual(
            self.ctx["TestTextualConvention"]().namedValues,
            NamedValues(("value", 0), ("otherValue", 1)),
            "bad NAMED VALUES",
        )

    def testObjectTypeNamedValues(self):
        self.assertEqual(
            self.ctx["testObject"].getSyntax().namedValues,
            NamedValues(("value", 0), ("otherValue", 1)),
            "bad NAMED VALUES",
        )


class TypeDeclarationTCEnumUsedByDefvalTestCase(unittest.TestCase):
    """
    TEST-MIB DEFINITIONS ::= BEGIN
    IMPORTS
      OBJECT-TYPE
        FROM SNMPv2-SMI
      TEXTUAL-CONVENTION
        FROM SNMPv2-TC;

    TestTextualConvention ::= TEXTUAL-CONVENTION
        STATUS       current
        DESCRIPTION  "Test TC"
        SYNTAX       INTEGER { enabled(1), disabled(2) }

    testObject1 OBJECT-TYPE
        SYNTAX       TestTextualConvention
        MAX-ACCESS   read-write
        STATUS       current
        DESCRIPTION  "Test object"
        DEFVAL       { enabled }
      ::= { 1 4 }

    testObject2 OBJECT-TYPE
        SYNTAX       TestTextualConvention { disabled(2) }
        MAX-ACCESS   read-write
        STATUS       current
        DESCRIPTION  "Test object"
        DEFVAL       { disabled }
      ::= { 1 5 }

    testObject3 OBJECT-TYPE
        SYNTAX       TestTextualConvention (2) -- dodgy; see comment below
        MAX-ACCESS   read-write
        STATUS       current
        DESCRIPTION  "Test object"
        DEFVAL       { disabled }
      ::= { 1 6 }

    END
    """

    def setUp(self):
        ast = parserFactory()().parse(self.__class__.__doc__)[0]
        mibInfo, symtable = SymtableCodeGen().gen_code(ast, {})
        self.mibInfo, pycode = PySnmpCodeGen().gen_code(ast, {mibInfo.name: symtable})
        codeobj = compile(pycode, "test", "exec")

        mibBuilder = MibBuilder()

        self.ctx = {"mibBuilder": mibBuilder}

        exec(codeobj, self.ctx, self.ctx)

    def testObjectTypeNamedValues1(self):
        self.assertEqual(
            self.ctx["testObject1"].getSyntax().namedValues,
            NamedValues(("enabled", 1), ("disabled", 2)),
            "bad NAMED VALUES",
        )

    def testObjectTypeSyntax1(self):
        self.assertEqual(self.ctx["testObject1"].getSyntax(), 1, "bad DEFVAL")

    def testObjectTypeNamedValues2(self):
        self.assertEqual(
            self.ctx["testObject2"].getSyntax().namedValues,
            NamedValues(
                ("disabled", 2),
            ),
            "bad NAMED VALUES",
        )

    def testObjectTypeSyntax2(self):
        self.assertEqual(self.ctx["testObject2"].getSyntax(), 2, "bad DEFVAL")

    # Note the omission of a testObjectTypeNamedValues3() here. RFC 2578 seems
    # to suggest that range-type constraints cannot be used on enumerated
    # integers, and smilint says it is illegal. However, such constructions are
    # used by some MIBs in practice. As of writing, pysmi parses but ignores
    # such range restrictions on enumerations; seeing as that behavior may be
    # changed in the future, the end result is not tested here.
    #
    # The resulting DEFVAL value is however tested below and must be set
    # properly either way. The main reason that we test this case, is that
    # before the commit that added this test class, this kind of construction
    # would trigger an exception in pysmi.

    def testObjectTypeSyntax3(self):
        self.assertEqual(self.ctx["testObject3"].getSyntax(), 2, "bad DEFVAL")


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
