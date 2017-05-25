import unittest
from wplab.theme_builder.processor.link_processor import LinkProcessor

class LinkProcessorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if cls is LinkProcessorTest:
            raise unittest.SkipTest("Skip BaseTest tests, it's a base class")
        super(LinkProcessorTest, cls).setUpClass()

    def setUp(self):
        self.processor = LinkProcessor()

    def test_paragraph(self):
        self._test_no_link("<p>Some text</p>")

    def _test_no_link(self, line):
        self._test_line_processing(line, line)

    def _test_line_processing(self, line, expected_result):
        result = self.processor.process(line)
        self.assertEqual(result, expected_result, "Expected {}, got {}".format(expected_result, result))

    def test_relative_link(self):
        self._test_link('<img {}="img/image1.jpg">', '<img {}="<?php echo get_template_directory_uri(); ?>/img/image1.jpg">')

    def _test_link(self, line, expected_result):
        self._test_line_processing(line.format(self.attribute), expected_result.format(self.attribute))

    def test_absolute_link(self):
        self._test_link('<img {}="/img/image1.jpg">', '<img {}="/img/image1.jpg">')

    def test_external_http_link(self):
        self._test_link('<img {}="http://hostname/img/image1.jpg">', '<img {}="http://hostname/img/image1.jpg">')

    def test_external_https_link(self):
        self._test_link('<img {}="https://hostname/img/image1.jpg">', '<img {}="https://hostname/img/image1.jpg">')

    def test_spaces_around_equal_sign_relative_link(self):
        self._test_link('<img {} = "img/image1.jpg">', '<img {} = "<?php echo get_template_directory_uri(); ?>/img/image1.jpg">')

    def test_spaces_around_equal_sign_absolute_link(self):
        self._test_link('<img {} = "/img/image1.jpg">', '<img {} = "/img/image1.jpg">')

    def test_relative_link_with_dashes(self):
        self._test_link('<img {}="img/image-1.jpg">', '<img {}="<?php echo get_template_directory_uri(); ?>/img/image-1.jpg">')


class SrcLinkProcessorTest(LinkProcessorTest):

    @property
    def attribute(self):
        return "src"
