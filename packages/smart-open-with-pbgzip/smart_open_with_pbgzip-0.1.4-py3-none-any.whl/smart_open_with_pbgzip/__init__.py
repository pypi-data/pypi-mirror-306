class PbgzipWriter:
    def __init__(self, stream, encoding = None):
        self.stream = stream
        self.encoding = encoding

    def write(self, to_write):
        if self.encoding and not isinstance(to_write, bytes):
            self.stream.write(to_write.encode(self.encoding))
        else:
            self.stream.write(to_write)

    def close(self):
        """Close the stream."""
        self.stream.close()

    @property
    def closed(self) -> bool:
        return self.stream.closed

    def flush(self):
        """Flush the stream."""
        self.stream.flush()

    def __enter__(self):
        """Support for context management (with statement)."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the stream is closed when exiting a context."""
        self.close()

    def writelines(self, lines):
        """Write a list of lines to the stream."""
        for line in lines:
            self.write(line)

    def readable(self):
        """Return False because this stream is not readable."""
        return False

    def writable(self):
        """Return True because this stream is writable."""
        return True

    def seekable(self):
        """Return False because this stream is not seekable."""
        return False

def _write_with_pbgzip(file_obj, mode):
    import gzip
    if "r" in mode:
        return gzip.GzipFile(fileobj=file_obj, mode=mode)
    else:
        import subprocess
        process = subprocess.Popen(["pbgzip", "-c"], stdin=subprocess.PIPE, stdout=open(str(file_obj.name), mode))
        return PbgzipWriter(process.stdin, encoding='utf-8')

def setup_smart_open_with_pbgzip():
    from smart_open import register_compressor
    import logging
    logging.getLogger('smart_open.compression').setLevel(logging.ERROR)
    register_compressor('.gz', _write_with_pbgzip)
    register_compressor('.gzip', _write_with_pbgzip)

def setup_smart_open_with_gzip():
    from smart_open import register_compressor
    from smart_open.compression import _handle_gzip
    import logging
    
    logging.getLogger('smart_open.compression').setLevel(logging.ERROR)
    register_compressor('.gz', _handle_gzip)
    register_compressor('.gzip', _handle_gzip)

setup_smart_open_with_pbgzip()