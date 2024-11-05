==============
NGS test utils
==============

Utilities for generation of synthetic NGS files.

A simple showcase::

    from ngs_test_utils import testcase

    class ExampleTestCase(testcase.NgsTestCase):
        """NGS-test-utils showcase."""

        def test_example(self):
            """Make a simple GTf and BAM file."""

            self.gtf = self.make_gtf([
                dict(feature="gene", start=100, end=500, gene_id="G1"),
                dict(feature="exon", start=100, end=200, gene_id="G1"),
                dict(feature="exon", start=400, end=500, gene_id="G1"),
            ])

            self.bam = self.make_bam(
                chroms=[("chr1", 1000)],
                segments=[
                    dict(qname="r1", pos=150, cigar=[(0, 75)]),
                    dict(qname="r2", pos=250, cigar=[(0, 150)]),
                ],
            )

            # Use these files to run your tests...

In the above example you can see:

- Test case class subclasses ``testcase.NgsTestCase`` instead of
  ``unittest.TestCase``. This class brings in all the methods for
  generating synthetic files.
- Methods for generation of files aim to support "Pythonic"
  construction of NGS files from scratch. Although the methods try to be
  user-friendly,  one needs to be familiar with the structure of the
  file format.
- Method ``self.make_gtf`` accepts list of GTF segments. Each of these
  segments represents a line in a GTF file. Segment is given as a dict
  of values that represent columns (and attributes) of a line in GTF
  file.
- Method ``self.make_bam`` accepts a list of chromosomes (this is
  ingredient for BAM header) and list of segments (for BAM body).
