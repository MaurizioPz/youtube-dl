# coding: utf-8
from __future__ import unicode_literals

import re
import sys
from .common import InfoExtractor
import time

from ..utils import (
    encode_dict,
)
from ..compat import (
    compat_chr,
    compat_parse_qs,
    compat_urllib_parse,
    compat_urllib_parse_unquote,
    compat_urllib_parse_unquote_plus,
    compat_urllib_parse_urlparse,
    compat_urllib_request,
    compat_urlparse,
    compat_str,
)


class VidtoIE(InfoExtractor):
    IE_NAME = 'vidto'
    IE_DESC = 'VidTo.me'
    _VALID_URL = r'https?://(?:www\.)?vidto\.me/(?P<id>[0-9a-zA-Z]+)\.html'
    _HOST = 'vidto.me'
    _TEST = {
        'url': 'http://vidto.me/ku5glz52nqe1.html',
        'info_dict': {
            'id': 'ku5glz52nqe1',
            'ext': 'mp4',
            'title': 'test.mp4'
        }
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')

        page = self._download_webpage(
            'http://%s/%s.html' % (self._HOST, video_id), video_id, 'Downloading video page')
        hash_regex = r'<input type="hidden" name="hash" value="(.*)">'
        hash_value = self._search_regex(hash_regex, page, 'hash', fatal=True)
        title_regex = r'<input type="hidden" name="fname" value="(.*)">'
        title = self._search_regex(title_regex, page, 'title', fatal=False)
        id_regex = r'<input type="hidden" name="id" value="(.*)">'
        id_value = self._search_regex(id_regex, page, 'id', fatal=True)
        cookies = self._get_cookies('http://%s/%s.html' % (self._HOST, video_id))


        form_str = {
            'op': 'download1',
            'imhuman': 'Proceed to video',
            'usr_login': '',
            'id': id_value,
            'fname': title,
            'referer': '',
            'hash': hash_value,
        }
        post_data = compat_urllib_parse.urlencode(encode_dict(form_str)).encode('ascii')
        req = compat_urllib_request.Request(url, post_data)
        req.add_header('Content-type', 'application/x-www-form-urlencoded')
        for key, morsel in cookies.iteritems():
            req.add_header('Cookie', '%s=%s' % (morsel.key, morsel.value))

        print("Waiting for countdown...")
        time.sleep(7)
        post_result = self._download_webpage(
            req, None,
            note='Proceed to video...', errnote='unable to proceed', fatal=True)

        file_link_regex = r'file_link ?= ?\'(https?:\/\/[0-9a-zA-z.\/\-_]+)'
        file_link = self._search_regex(file_link_regex, post_result, 'file_link', fatal=True)

        return {
            'id': video_id,
            'url': file_link,
            'title': title,
        }