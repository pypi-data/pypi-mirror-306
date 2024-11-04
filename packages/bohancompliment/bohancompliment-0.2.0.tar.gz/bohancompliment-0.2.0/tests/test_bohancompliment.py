# File: tests/test_bohancompliment.py

import unittest
from unittest.mock import patch
from bohancompliment import ComplimentGenerator  # Corrected import

class TestComplimentGenerator(unittest.TestCase):
    
    def setUp(self):
        self.cg = ComplimentGenerator()
        self.sample_name = "Alice"
        self.sample_trait = "problem-solving"
        self.sample_language = "en"
        self.sample_invalid_language = "jp"
        self.sample_compliment = "You're awesome, {name}!"
        self.sample_translation = [
            "¡Eres increíble, {name}!",
            "{name}, haces del mundo un lugar mejor!"
        ]

    # Test __init__
    def test_initial_compliments(self):
        self.assertTrue(len(self.cg.compliments) > 0, "Compliments list should not be empty upon initialization.")
    
    def test_initial_translations(self):
        expected_languages = {'en', 'es', 'fr', 'de', 'it'}
        self.assertEqual(set(self.cg.translations.keys()), expected_languages, "Translations should include the expected languages.")

    # Test compliment method
    @patch('bohancompliment.generator.random.choice')
    def test_compliment_valid_name(self, mock_choice):
        mock_choice.return_value = self.cg.compliments[0]
        compliment = self.cg.compliment(self.sample_name)
        expected = self.cg.compliments[0].format(name=self.sample_name)
        self.assertEqual(compliment, expected, "Compliment should be correctly formatted with the given name.")

    def test_compliment_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.cg.compliment(123)  # Non-string name

    def test_compliment_empty_name(self):
        with self.assertRaises(ValueError):
            self.cg.compliment("   ")  # Empty or whitespace name

    # Test personalized_compliment method
    def test_personalized_compliment_valid(self):
        result = self.cg.personalized_compliment(self.sample_name, self.sample_trait)
        expected = f"{self.sample_name}, your {self.sample_trait} is truly remarkable!"
        self.assertEqual(result, expected, "Personalized compliment should be correctly formatted.")

    def test_personalized_compliment_invalid_name(self):
        with self.assertRaises(TypeError):
            self.cg.personalized_compliment(456, self.sample_trait)  # Non-string name

    def test_personalized_compliment_invalid_trait(self):
        with self.assertRaises(ValueError):
            self.cg.personalized_compliment(self.sample_name, "   ")  # Empty trait

    # Test multi_compliment method
    @patch('bohancompliment.generator.random.choice')
    def test_multi_compliment_valid(self, mock_choice):
        mock_choice.side_effect = self.cg.compliments[:3]
        compliments = self.cg.multi_compliment(self.sample_name, 3)
        expected = [comp.format(name=self.sample_name) for comp in self.cg.compliments[:3]]
        self.assertEqual(compliments, expected, "Should return the correct number of formatted compliments.")

    def test_multi_compliment_invalid_name(self):
        with self.assertRaises(TypeError):
            self.cg.multi_compliment(None, 2)  # Non-string name

    def test_multi_compliment_invalid_count_type(self):
        with self.assertRaises(TypeError):
            self.cg.multi_compliment(self.sample_name, "two")  # Non-integer count

    def test_multi_compliment_invalid_count_value(self):
        with self.assertRaises(ValueError):
            self.cg.multi_compliment(self.sample_name, 0)  # Non-positive count

    # Test compliment_in_language method
    @patch('bohancompliment.generator.random.choice')
    def test_compliment_in_language_valid(self, mock_choice):
        mock_choice.return_value = self.cg.translations[self.sample_language][0]
        compliment = self.cg.compliment_in_language(self.sample_name, self.sample_language)
        expected = self.cg.translations[self.sample_language][0].format(name=self.sample_name)
        self.assertEqual(compliment, expected, "Compliment in specified language should be correctly formatted.")

    def test_compliment_in_language_unsupported(self):
        result = self.cg.compliment_in_language(self.sample_name, self.sample_invalid_language)
        expected = f"Language '{self.sample_invalid_language}' not supported."
        self.assertEqual(result, expected, "Should return error message for unsupported language.")

    def test_compliment_in_language_invalid_name(self):
        with self.assertRaises(TypeError):
            self.cg.compliment_in_language(789, self.sample_language)  # Non-string name

    def test_compliment_in_language_invalid_language(self):
        with self.assertRaises(ValueError):
            self.cg.compliment_in_language(self.sample_name, "   ")  # Empty language

    # Test add_compliment method
    def test_add_compliment_valid(self):
        initial_length = len(self.cg.compliments)
        self.cg.add_compliment(self.sample_compliment)
        self.assertEqual(len(self.cg.compliments), initial_length + 1, "Compliment should be added to the list.")
        self.assertIn(self.sample_compliment, self.cg.compliments, "Added compliment should be in the compliments list.")

    def test_add_compliment_invalid(self):
        invalid_compliment = "You're awesome!"  # Missing {name}
        with self.assertRaises(ValueError):
            self.cg.add_compliment(invalid_compliment)

    # Test add_translation method
    def test_add_translation_valid(self):
        new_language = "jp"
        initial_languages = set(self.cg.list_languages())
        self.cg.add_translation(new_language, self.sample_translation)
        updated_languages = set(self.cg.list_languages())
        self.assertIn(new_language, updated_languages, "New language should be added to translations.")
        for comp in self.sample_translation:
            self.assertIn(comp, self.cg.translations[new_language], "All new compliments should be added to the new language.")

    def test_add_translation_invalid_missing_placeholder(self):
        invalid_compliments = ["Eres increíble!", "¡Haces del mundo mejor!"]  # Missing {name}
        with self.assertRaises(ValueError):
            self.cg.add_translation("pt", invalid_compliments)

    # Test list_languages method
    def test_list_languages_initial(self):
        expected_languages = ['en', 'es', 'fr', 'de', 'it']
        self.assertCountEqual(self.cg.list_languages(), expected_languages, "Initial languages should match expected set.")

    def test_list_languages_after_addition(self):
        new_language = "jp"
        self.cg.add_translation(new_language, self.sample_translation)
        languages = self.cg.list_languages()
        self.assertIn(new_language, languages, "Newly added language should appear in the languages list.")

    # Test add_translation overwriting existing language
    def test_add_translation_overwrite(self):
        new_compliments = ["New compliment 1, {name}!", "New compliment 2, {name}!"]
        self.cg.add_translation("en", new_compliments)
        self.assertEqual(self.cg.translations["en"], new_compliments, "Existing language compliments should be overwritten.")

    # Test that all compliments contain {name} after additions
    def test_all_compliments_have_name_placeholder(self):
        for compliment in self.cg.compliments:
            self.assertIn("{name}", compliment, "All compliments must include '{name}' placeholder.")
        for lang_compliments in self.cg.translations.values():
            for compliment in lang_compliments:
                self.assertIn("{name}", compliment, "All translated compliments must include '{name}' placeholder.")

if __name__ == '__main__':
    unittest.main()
