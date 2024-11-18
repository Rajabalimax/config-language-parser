import unittest
from main import parse_config, parse_value, ParserError


class TestParser(unittest.TestCase):
  def test_parse_value_string(self):
    self.assertEqual(parse_value('"test"', {}), "test")

  def test_parse_value_number(self):
    self.assertEqual(parse_value("123", {}), 123)

  def test_parse_value_constant(self):
    constants = {'my_const': 10}
    self.assertEqual(parse_value('?my_const', constants), 10)

  def test_parse_value_constant_undefined(self):
    constants = {}
    with self.assertRaisesRegex(ParserError, "Constant 'my_const' not defined"):
      parse_value('?my_const', constants)

  def test_parse_config_constant(self):
    config_text = """
    def my_const = 10
    """
    constants = {}
    config = parse_config(config_text, constants)
    self.assertEqual(config, {})
    self.assertEqual(constants, {'my_const': 10})

  def test_parse_config_empty_lines(self):
    config_text = """
    
        def my_const = 10

        """
    constants = {}
    config = parse_config(config_text, constants)
    self.assertEqual(config, {})
    self.assertEqual(constants, {'my_const': 10})


if __name__ == '__main__':
  unittest.main()