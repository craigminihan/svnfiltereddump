from SvnLump import SvnLump


class EmptyRevision(object):
    def __init__(self, writer):
        self._writer = writer
        self._lump = SvnLump()
        self._lump.set_header('Revision-number', None)
        self._lump.set_header('Content-length', "0")

    def process_revision(self, rev, aux_data):
        assert aux_data is None
        self._lump.set_header('Revision-number', str(rev))

        self._writer.write_lump(self._lump)
