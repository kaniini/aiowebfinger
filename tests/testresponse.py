import json
import xml.etree.ElementTree as etree
import unittest

from aiowebfinger.response import JRDResponse, XRDResponse


class JRDParseTests(unittest.TestCase):
    def setUp(self):
        datafile = open('fixtures/mastodon-hit.json')
        self.jrd = json.load(datafile)
        datafile.close()

        self.resp = JRDResponse(self.jrd)

    def test_subject(self):
        self.assertEqual('acct:kaniini@mastodon.dereferenced.org', self.resp.subject)

    def test_aliases(self):
        self.assertIn('https://mastodon.dereferenced.org/@kaniini', self.resp.aliases)

    def test_links(self):
        self.assertIn('salmon', self.resp.invlinks)


class XRDParseTests(unittest.TestCase):
    def setUp(self):
        datafile = open('fixtures/mastodon-hit.xml')
        self.xrd = datafile.read()
        datafile.close()

        self.resp = XRDResponse(etree.XML(self.xrd))

    def test_subject(self):
        self.assertEqual('acct:kaniini@mastodon.dereferenced.org', self.resp.subject)

    def test_aliases(self):
        self.assertIn('https://mastodon.dereferenced.org/@kaniini', self.resp.aliases)

    def test_links(self):
        self.assertIn('salmon', self.resp.invlinks)
