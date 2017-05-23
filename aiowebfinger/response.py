import xml.etree.ElementTree as etree


RELS = {
    'activity_streams': 'http://activitystrea.ms/spec/1.0',
    'avatar': 'http://webfinger.net/rel/avatar',
    'atom': 'http://apinamespace.org/atom',
    'describedby': 'describedby',
    'hcard': 'http://microformats.org/profile/hcard',
    'open_id': 'http://specs.openid.net/auth/2.0/provider',
    'opensocial': 'http://ns.opensocial.org/2008/opensocial/activitystreams',
    'ostatus_subscribe': 'http://ostatus.org/schema/1.0/subscribe',
    'portable_contacts': 'http://portablecontacts.net/spec/1.0',
    'profile': 'http://webfinger.net/rel/profile-page',
    'salmon': 'salmon',
    'salmon_mention': 'http://salmon-protocol.org/ns/salmon-mention',
    'salmon_replies': 'http://salmon-protocol.org/ns/salmon-replies',
    'updates_from': 'http://schemas.google.com/g/2010#updates-from',
    'webfist': 'http://webfist.org/spec/rel',
    'xfn': 'http://gmpg.org/xfn/11',
}


REL_ATTRS = {
    'ostatus_subscribe': 'template',
}


class CommonResponse:
    def __init__(self):
        self.invlinks = {l['rel']: l for l in self.links if 'rel' in l}

    def __repr__(self):
        return '%s(subject=%r, aliases=%r, properties=%r, links=%r)' % (self.__class__.__name__, self.subject, self.aliases, self.properties, self.links)

    def rel(self, relation: str, attr: str='href') -> str:
        if relation not in self.invlinks:
            return

        link = self.invlinks[relation]
        if attr:
            return link.get(attr)
        return link


class JRDResponse(CommonResponse):
    """A response object which wraps the given JRD object (provided as an already unpacked dictionary)."""
    def __init__(self, jrd: dict):
        self.jrd = jrd
        super().__init__()

    def __getattr__(self, name: str):
        if name in RELS:
            return self.rel(RELS[name], REL_ATTRS.get(name, 'href'))
        return getattr(self.jrd, name)

    @property
    def subject(self) -> str:
        return self.jrd.get('subject')

    @property
    def aliases(self) -> list:
        return self.jrd.get('aliases', [])

    @property
    def properties(self) -> dict:
        return self.jrd.get('properties', {})

    @property
    def links(self) -> list:
        return self.jrd.get('links', [])


class XRDResponse(CommonResponse):
    """A response object which wraps the given XRD object (provided as an ElementTree)."""
    def __init__(self, xrd: etree.Element):
        self.xrd = xrd
        super().__init__()

    def __getattr__(self, name: str):
        if name in RELS:
            return self.rel(RELS[name], REL_ATTRS.get(name, 'href'))
        return getattr(self.xrd, name)

    @property
    def subject(self) -> str:
        ref = self.xrd.find('{http://docs.oasis-open.org/ns/xri/xrd-1.0}Subject')
        if ref is None or not ref.text:
            return
        return ref.text

    @property
    def aliases(self) -> list:
        refs = self.xrd.findall('{http://docs.oasis-open.org/ns/xri/xrd-1.0}Alias')
        if not refs:
            return []
        return [el.text for el in refs]

    @property
    def properties(self) -> dict:
        refs = self.xrd.findall('{http://docs.oasis-open.org/ns/xri/xrd-1.0}Property')
        if not refs:
            return {}
        return {el.attrib['type']: el.text for el in refs if 'type' in el}

    @property
    def links(self) -> list:
        refs = self.xrd.findall('{http://docs.oasis-open.org/ns/xri/xrd-1.0}Link')
        if not refs:
            return []
        return [el.attrib for el in refs]

