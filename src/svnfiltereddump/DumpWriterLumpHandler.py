import StringIO
import hashlib
import urllib2
import json
from collections import namedtuple
import logging

from SvnLump import SvnLump
from ContentTin import ContentTin


class DumpWriterLumpHandler(object):
    def __init__(self, config_name):
        self._revision = None
        self._config = DumpWriterLumpHandler._load_config(config_name)
        self._content_cache = {}
        for command in self._config.commands:
            self._get_content(command)

    def post_process(self, lump, writer):
        self._revision = lump.revision if lump.revision else self._revision
        commands = self._match_commands(lump)
        for command in commands:
            new_lump = self._new_lump(command)
            writer(new_lump)
            logging.info("Added '%s' at revision %s" % (new_lump.path, self._revision))

    def _match_commands(self, lump):
        commands = []
        for command in self._config.commands:
            if lump.has_copy_from is False or command.node.copy_from is True:
                node = command.node
                if lump.path == node.path and lump.kind == node.kind and lump.action == node.action:
                    commands.append(command)
        return commands

    def _get_content(self, command):
        if command.content.source == "url":
            url = command.content.url
            content = self._content_cache.get(url, None)
            if not content:
                content = urllib2.urlopen(url).read()
                self._content_cache[url] = content
        else:
            content = command.content.body
        return content

    def _new_lump(self, command):
        path = command.content.path if command.content.path else command.node.path
        path += '/' + command.content.name
        content = self._get_content(command)
        content_length = len(content)
        content_md5 = self._get_hexdigest(content)
        lump = SvnLump().set_header("Node-path", path).\
            set_header("Node-kind", "file").\
            set_header("Node-action", "add").\
            set_header("Content-length", str(content_length)).\
            set_header("Text-content-md5", content_md5).\
            set_header("Text-content-length", str(content_length))
        content_stream = StringIO.StringIO(content)
        lump.content = ContentTin(content_stream, content_length, content_md5)
        return lump

    @staticmethod
    def _get_hexdigest(content):
        algo = hashlib.md5()
        algo.update(content)
        return algo.hexdigest()

    @staticmethod
    def _load_config(name):
        return json.load(open(name, "r"), object_hook=lambda o: namedtuple('Events', o.keys())(*o.values()))
