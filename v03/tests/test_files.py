import csv,gzip,tempfile,unittest
from pathlib import Path


class FileTransport(unittest.TestCase):
    def test_csv_and_trace_cleanup_with_spaces(self):
        # Exercise normal stdlib handle lifetimes used by the release on POSIX and Windows.
        with tempfile.TemporaryDirectory(prefix="privtrace review ") as name:
            root=Path(name)
            path=root/"decision log.csv"
            with path.open("w",newline="",encoding="utf-8") as f:
                csv.writer(f).writerow(["signed","two, roles"])
            with path.open(newline="",encoding="utf-8") as f:
                self.assertEqual(next(csv.reader(f)),["signed","two, roles"])
            path.unlink()
            archive=root/"trace.gz"
            with gzip.open(archive,"wt",encoding="utf-8") as f:
                f.write("1\n")
            with gzip.open(archive,"rt",encoding="utf-8") as f:
                self.assertEqual(f.readline().rstrip(),"1")
            archive.unlink()
