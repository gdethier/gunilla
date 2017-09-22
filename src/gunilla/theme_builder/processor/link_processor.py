from gunilla.theme_builder.processor import Processor
import re


class LinkProcessor(Processor):

    URL_PATTERN = '[\<\?>a-zA-Z0-9-_/\. ]*'

    URL_REGEX = re.compile(URL_PATTERN)

    LINK_ATTRIBUTES = ['src', 'href']

    def __init__(self):
        self._link_regex_list = []
        for attribute in self.LINK_ATTRIBUTES:
            self._link_regex_list.append(re.compile(self._build_link_pattern(attribute)))

    def _build_link_pattern(self, attribute):
        return '({}[\s]*=[\s]*)([\'\"])({})([\'\"])'.format(attribute, self.URL_PATTERN)

    def process(self, line):
        for regex in self._link_regex_list:
            line = regex.sub(self._rewrite_url_if_needed, line)
        return line

    def _rewrite_url_if_needed(self, match):
        link = match.group(0)
        url = match.group(3).strip()
        if self._is_relative(url):
            return self._rewrite_link(match)
        else:
            return link

    def _is_relative(self, url):
        return not (url.startswith('/') or url.startswith('http') or url.startswith('<?'))

    def _rewrite_link(self, match):
        return match.re.sub('\g<1>\g<2><?php echo get_template_directory_uri(); ?>/\g<3>\g<4>', match.group(0))
