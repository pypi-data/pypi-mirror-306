import unittest
#importing all our functions 
from codeshakespeare.shakespeare import (
    to_shakespeare, 
    to_shakespeare_error, 
    get_random_shakespeare_quote, 
    generate_shakespearean_commit_message
)
'''
need at least 12 functions since its 3 tests per function and we have four functions
'''
class TestCodeShakespeare(unittest.TestCase):

    def test_to_shakespeare_dramatic(self):
        """Test the 'dramatic' option of the to_shakespeare function."""
        comment = "This function loads data."
        result = to_shakespeare(comment, formality="dramatic")
        print(f"Dramatic formality result: {result}")
        self.assertEqual(result, "// Behold! This function loads data, a comment of utmost importance, full of thunderous thought!")

    def test_to_shakespeare_simple(self):
        """Test the 'simple' option of the to_shakespeare function."""
        comment = "This is a simple comment."
        result = to_shakespeare(comment, formality="simple")
        print(f"Simple formality result: {result}")
        self.assertEqual(result, "// A simple thought: This is a simple comment, yet profound in its own right.")

    def test_to_shakespeare_no_formality(self):
        """Test default behavior of the to_shakespeare function when no formality is specified."""
        comment = "This is a test."
        result = to_shakespeare(comment)
        print(f"Default formality result: {result}")
        self.assertEqual(result, "// O noble comment, This is a test, thou art rephrased in grandeur!")

    # Additional tests for `to_shakespeare_error`
    def test_to_shakespeare_error_history(self):
        """Test the 'history' option of the to_shakespeare_error function."""
        error_msg = "Syntax error."
        result = to_shakespeare_error(error_msg, severity="history")
        print(f"History severity result: {result}")
        self.assertEqual(result, "Mark ye well this error: 'Syntax error', for it shall be written in the annals of code!")

    def test_to_shakespeare_error_no_severity(self):
        """Test default behavior of the to_shakespeare_error function when no severity is specified."""
        error_msg = "Connection lost."
        result = to_shakespeare_error(error_msg)
        print(f"Default severity result: {result}")
        self.assertEqual(result, "Alas, an error hath occurred: 'Connection lost'. 'Tis a tragedy most foul.")

    def test_to_shakespeare_error_invalid_severity(self):
        """Test behavior when an invalid severity is provided for to_shakespeare_error."""
        error_msg = "File corrupted."
        result = to_shakespeare_error(error_msg, severity="unknown")
        print(f"Invalid severity result: {result}")
        self.assertEqual(result, "An error, 'File corrupted', and so the plot thickens.")

    # Additional tests for `get_random_shakespeare_quote`
    def test_get_random_shakespeare_quote_serious(self):
        """Test the 'serious' option of the get_random_shakespeare_quote function."""
        result = get_random_shakespeare_quote(style="serious")
        print(f"Serious quote result: {result}")
        serious_quotes = [
            "The code is afoot, let every function bear its weight.",
            "Once more unto the code, dear friends, once more!",
            "All the world's a stage, and all the men and women merely programmers."
        ]
        self.assertIn(result, serious_quotes)

    def test_get_random_shakespeare_quote_melancholic(self):
        """Test the 'melancholic' option of the get_random_shakespeare_quote function."""
        result = get_random_shakespeare_quote(style="melancholic")
        print(f"Melancholic quote result: {result}")
        melancholic_quotes = [
            "O woe is me, for the bugs have returned once more.",
            "Tomorrow, and tomorrow, and tomorrow creeps in this petty pace of debugging.",
            "Out, out, brief code! Thou art but a shadow of the program I once dreamed."
        ]
        self.assertIn(result, melancholic_quotes)

    def test_get_random_shakespeare_quote_default(self):
        """Test the default behavior of the get_random_shakespeare_quote function."""
        result = get_random_shakespeare_quote()
        print(f"Default quote result: {result}")
        playful_quotes = [
            "To code, or not to code, that is the question.",
            "Cry havoc and let slip the bugs of war!",
            "Parting is such sweet sorrow... especially when closing your IDE."
        ]
        self.assertIn(result, playful_quotes)

    # Additional tests for `generate_shakespearean_commit_message`
    def test_generate_shakespearean_commit_message_defeat(self):
        """Test the 'defeat' option of the generate_shakespearean_commit_message function."""
        result = generate_shakespearean_commit_message(emotion="defeat")
        print(f"Defeat emotion result: {result}")
        defeatist_messages = [
            "A commit, though it be filled with sorrow, must be made.",
            "This code, born of struggle, may yet rise again.",
            "O bitter fate, that this commit should come so soon."
        ]
        self.assertIn(result, defeatist_messages)

    def test_generate_shakespearean_commit_message_reflection(self):
        """Test the 'reflection' option of the generate_shakespearean_commit_message function."""
        result = generate_shakespearean_commit_message(emotion="reflection")
        print(f"Reflection emotion result: {result}")
        reflective_messages = [
            "In this commit, I find both progress and question.",
            "Tis not the end, but merely the next chapter of this code.",
            "Thus, the story unfolds with each commit, shaping our fate."
        ]
        self.assertIn(result, reflective_messages)

    def test_generate_shakespearean_commit_message_default(self):
        """Test default behavior of the generate_shakespearean_commit_message function."""
        result = generate_shakespearean_commit_message()
        print(f"Default commit message result: {result}")
        victorious_messages = [
            "Commit thy changes, for they doth bring glory!",
            "Thine errors are slain, and the code is just!",
            "This branch, once barren, now flourisheth with code."
        ]
        self.assertIn(result, victorious_messages)

if __name__ == '__main__':
    unittest.main()