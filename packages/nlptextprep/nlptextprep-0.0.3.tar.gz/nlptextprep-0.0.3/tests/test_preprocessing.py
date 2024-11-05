import unittest
from src.nlptextprep import preprocess_text

__author__ = "Tashu"
__copyright__ = "Tashu"
__license__ = "MIT"

class TestPreprocessing(unittest.TestCase):
    
    def test(self):
        self.assertEqual(preprocess_text("(4 - 2)/7"), "( 4 - 2 ) /7")
        self.assertEqual(preprocess_text("capetown@optique.co.za"), "capetown@optique.co.za")
        self.assertEqual(preprocess_text("HEllo https://www.natures-source.com/products/provita-lions-mane-5000-90-veggie-caps"), "hello https://www.natures-source.com/products/provita-lions-mane-5000-90-veggie-caps")
        self.assertEqual(preprocess_text("HELLO"), "hello")
        self.assertEqual(preprocess_text("Hello World"), "hello world")
        self.assertEqual(preprocess_text("123 (ABC)!"), "123 abc")
        self.assertEqual(preprocess_text("ÄÖÜ"), "aou")
        self.assertEqual(preprocess_text(""), "")
        self.assertEqual(preprocess_text("Line one\nLine two"), "line one line two")
        self.assertEqual(preprocess_text("Line one\rLine two"), "line one line two")
        self.assertEqual(preprocess_text("Line one\r\nLine two"), "line one line two")
        self.assertEqual(preprocess_text("Line one\n\n\n(Line two)"), "line one line two")
        self.assertEqual(preprocess_text("Line one\nLine two\rLine three\r\nLine four"),
                         "line one line two line three line four")
        self.assertEqual(preprocess_text("\n\n\n"), "")
        self.assertEqual(preprocess_text("No line breaks here"), "line break")
        self.assertEqual(preprocess_text("Hello, (world)!"), "hello world")
        self.assertEqual(preprocess_text("What's this? A test."), "what test")
        self.assertEqual(preprocess_text("Remove, all; punctuation: please."), "remov punctuat pleas")
        self.assertEqual(preprocess_text("U.S."), "us")
        self.assertEqual(preprocess_text("!!!Hello World!!!"), "hello world")
        self.assertEqual(preprocess_text("Price: $100.00!!"), "price $ 100.00")
        self.assertEqual(preprocess_text("Price: $100.00! Is it €120, or £150.50?"), "price $ 100.00 €120 £150.50")
        self.assertEqual(preprocess_text("No punctuation here"), "punctuat")
        self.assertEqual(preprocess_text("!!!"), "")
        self.assertEqual(preprocess_text("Remove all the stop words from this string"),
                         "remov stop word string")
        self.assertEqual(preprocess_text("I and to the"), "")
        self.assertEqual(preprocess_text("the and of in"), "")
        self.assertEqual(preprocess_text("running jumped playing"), "run jump play")
        self.assertEqual(preprocess_text("happily happier happiness"), "happili happier happi")
        self.assertEqual(preprocess_text("#hashtag running!"), "hashtag run")
        self.assertEqual(preprocess_text("RUNNING"), "run")
        self.assertEqual(preprocess_text("Data preprocessing is important"), "data preprocess import")
        self.assertEqual(preprocess_text("geese feet mice"), "gees feet mice")
        self.assertEqual(preprocess_text("The striped bats are hanging on their feet for best"),
                         "stripe bat hang feet best")
        self.assertEqual(preprocess_text("YCH�s Café’s Special!"), "ychs cafe special")
        self.assertEqual(preprocess_text("This text contains � special characters."), 
                         "text contain special charact")
        self.assertEqual(preprocess_text("Only normal characters here"), 
                         "normal charact")
        self.assertEqual(preprocess_text("This is encoded data: %20, \\xAB, and \\u1234."),
                         "encod data")
        self.assertEqual(preprocess_text("No encoded data here"), 
                         "encod data")
        self.assertEqual(preprocess_text("Encoded %7C and \\x3C\\x3E"), 
                         "encod")
        self.assertEqual(preprocess_text("More encoded \\x1A text %5B %5D"), 
                         "encod text")
        self.assertEqual(preprocess_text("<html><body><p>This is a paragraph.</p></body></html>"),
                         "paragraph")
        self.assertEqual(preprocess_text("<div><h1>Header</h1><p>Paragraph</p></div>"),
                         "header paragraph")
        self.assertEqual(preprocess_text("<b>Bold text</b> and <i>italic text</i>"),
                         "bold text ital text")
        self.assertEqual(preprocess_text("<tag>    </tag>Extra spaces after tag removal."), "extra space tag remov")

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            preprocess_text(123)  # Non-string input should raise ValueError

if __name__ == "__main__":
    unittest.main()
