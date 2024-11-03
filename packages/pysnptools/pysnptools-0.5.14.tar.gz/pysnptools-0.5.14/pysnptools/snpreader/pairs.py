import os
import numpy as np
import logging
import unittest
import doctest
from pathlib import Path
from pysnptools.util.pairs import _Pairs as UtilPairs

from pysnptools.snpreader import SnpReader


class _Pairs(SnpReader):
    """
    Experimental.
    """

    # !!
    # !!!see fastlmm\association\epistasis.py for code that allows ranges of snps to be specified when making pairs
    def __init__(
        self,
        snpreader0,
        snpreader1=None,
        do_standardize=True,
        sid_materialize_limit=1000 * 1000,
        _include_single_times_single=False,
    ):
        # !!! could add option to change snp separator and another to encode chrom, etc in the snp name
        super(_Pairs, self).__init__()
        self._ran_once = False
        self.snpreader0 = snpreader0
        self.snpreader1 = snpreader1
        self.do_standardize = do_standardize
        self.sid_materialize_limit = sid_materialize_limit
        self._include_single_times_single = _include_single_times_single

    def __repr__(self):
        part2 = "" if self.snpreader1 is None else ",{0}".format(self.snpreader1)
        return "{0}({1}{2})".format(self.__class__.__name__, self.snpreader0, part2)

    @property
    def row(self):
        """*same as* :attr:`iid`"""
        if not hasattr(self, "_row"):
            self._row = self.snpreader0.row
            assert self.snpreader1 is None or np.array_equal(
                self._row, self.snpreader1.row
            ), "Expect snpreaders to have the same iids in the same order"
        return self._row

    @property
    def col(self):
        """*same as* :attr:`sid`"""
        if not hasattr(self, "_col"):
            assert (
                self.col_count < self.sid_materialize_limit
            ), "{:,} is too many sids to materialize".format(self.col_count)
            if self.snpreader1 is None:
                col_0 = self.snpreader0.col
                col_list = []
                self.index0_list = []  # !!!should be _index0_list, etc
                self.index1_list = []
                for index0 in range(self.snpreader0.col_count):
                    # logging.info("index0={0} of {1}".format(index0,self.snpreader0.col_count))# !!!
                    start1 = index0 if self._include_single_times_single else index0 + 1
                    for index1 in range(start1, self.snpreader0.col_count):
                        col_list.append("{0},{1}".format(col_0[index0], col_0[index1]))
                        self.index0_list.append(index0)
                        self.index1_list.append(index1)
                self._col = np.array(col_list)
                self.index0_list = np.array(self.index0_list)
                self.index1_list = np.array(self.index1_list)
            else:
                col_0 = self.snpreader0.col
                col_1 = self.snpreader1.col
                assert (
                    len(set(col_0) & set(col_1)) == 0
                ), "Pairs currently requires two snpreaders to have no sids in common"
                col_list = []
                self.index0_list = []
                self.index1_list = []
                for index0 in range(self.snpreader0.col_count):
                    # logging.info("index0={0} of {1}".format(index0,self.snpreader0.col_count))# !!!
                    for index1 in range(self.snpreader1.col_count):
                        col_list.append("{0},{1}".format(col_0[index0], col_1[index1]))
                        self.index0_list.append(index0)
                        self.index1_list.append(index1)
                self._col = np.array(col_list)
                self.index0_list = np.array(self.index0_list)
                self.index1_list = np.array(self.index1_list)

        assert self.col_count == len(self._col), "real assert"
        return self._col

    @property
    def col_count(self):
        n0 = self.snpreader0.col_count
        if self.snpreader1 is None:
            if self._include_single_times_single:
                return (n0 * n0 + n0) // 2
            else:
                return (n0 * n0 - n0) // 2
        else:
            return n0 * self.snpreader1.col_count

    @property
    def col_property(self):
        """*same as* :attr:`pos`"""
        if not hasattr(self, "_col_property"):
            self._col_property = np.zeros([self.sid_count, 3], dtype=np.int64)
        return self._col_property

    def copyinputs(self, copier):
        # doesn't need to self._run_once() because only uses original inputs !!!is this true?
        self.snpreader0.copyinputs(copier)
        if self.snpreader1 is not None:
            self.snpreader1.copyinputs(copier)

    def _run_once(self):
        if self._ran_once:
            return

        self._ran_once = True
        self.col

    def _read(
        self,
        iid_index_or_none,
        sid_index_or_none,
        order,
        dtype,
        force_python_only,
        view_ok,
        num_threads,
    ):
        self._run_once()
        dtype = np.dtype(dtype)

        iid_count_in = self.iid_count
        sid_count_in = self.sid_count

        if iid_index_or_none is not None:
            len(iid_index_or_none)
        else:
            range(iid_count_in)

        if sid_index_or_none is not None:
            len(sid_index_or_none)
            sid_index = sid_index_or_none
        else:
            sid_index = range(sid_count_in)

        sid_index_inner_0 = self.index0_list[
            sid_index
        ]  # Find the sid_index of the left snps of interest
        sid_index_inner_1 = self.index1_list[
            sid_index
        ]  # Find the sid_index of the right snps of interest
        if self.snpreader1 is None:
            sid_index_inner_01 = np.unique(
                np.r_[sid_index_inner_0, sid_index_inner_1]
            )  # Index of every snp of interest
            inner_01 = self.snpreader0[iid_index_or_none, sid_index_inner_01].read(
                order=order,
                dtype=dtype,
                force_python_only=force_python_only,
                view_ok=True,
                num_threads=num_threads,
            )  # read every val of interest
            val_inner_01 = (
                inner_01.standardize(num_threads=num_threads).val
                if self.do_standardize
                else inner_01.val
            )

            sid_index_inner_01_reverse = {
                v: i for i, v in enumerate(sid_index_inner_01)
            }  # Dictionary of snp_index to position in sid_index_inner_01
            sid_index_inner_0_in_val = np.array(
                [sid_index_inner_01_reverse[i] for i in sid_index_inner_0]
            )  # Replace snp_index0 with column # in val_inner_01
            sid_index_inner_1_in_val = np.array(
                [sid_index_inner_01_reverse[i] for i in sid_index_inner_1]
            )  # Replace snp_index1 with column # in val_inner_01
            val_inner_0 = val_inner_01[
                :, sid_index_inner_0_in_val
            ]  # Extract the vals for the left snps of interest
            val_inner_1 = val_inner_01[
                :, sid_index_inner_1_in_val
            ]  # Extract the vals for the right snps of interest
        else:
            inner_0 = self.snpreader0[iid_index_or_none, sid_index_inner_0].read(
                order=order,
                dtype=dtype,
                force_python_only=force_python_only,
                view_ok=True,
                num_threads=num_threads,
            )  # read every val of interest
            inner_1 = self.snpreader1[iid_index_or_none, sid_index_inner_1].read(
                order=order,
                dtype=dtype,
                force_python_only=force_python_only,
                view_ok=True,
                num_threads=num_threads,
            )  # read every val of interest
            val_inner_0 = (
                inner_0.standardize(num_threads=num_threads).val
                if self.do_standardize
                else inner_0.val
            )
            val_inner_1 = (
                inner_1.standardize(num_threads=num_threads).val
                if self.do_standardize
                else inner_1.val
            )
        val = (
            val_inner_0 * val_inner_1
        )  # Element multiplication creates the vals for the pairs
        return val


def split_on_sids(snpreader, part_count):
    sid_count = snpreader.sid_count
    start = 0
    for part_index in range(1, part_count + 1):
        end = part_index * sid_count // part_count
        yield snpreader[:, start:end]
        start = end


class _Pairs2(SnpReader):
    def __init__(
        self,
        snpreader0,
        snpreader1=None,
        do_standardize=True,
        sid_materialize_limit=1000 * 1000,
        _include_single_times_single=False,
    ):  # !!! could add option to change snp separator and another to encode chrom, etc in the snp name
        super(_Pairs2, self).__init__()
        self._ran_once = False
        self.snpreader0 = snpreader0
        self.snpreader1 = snpreader1
        self.do_standardize = do_standardize
        self.sid_materialize_limit = sid_materialize_limit
        self._include_single_times_single = _include_single_times_single
        self._utilpairs = UtilPairs(
            snpreader0.sid,
            snpreader1.sid if snpreader1 is not None else snpreader0.sid,
            include_singles=_include_single_times_single,
            duplicates_ok=False,
        )

    def __repr__(self):
        part2 = "" if self.snpreader1 is None else ",{0}".format(self.snpreader1)
        return "{0}({1}{2})".format(self.__class__.__name__, self.snpreader0, part2)

    @property
    def row(self):
        """*same as* :attr:`iid`"""
        if not hasattr(self, "_row"):
            self._row = self.snpreader0.row
            assert self.snpreader1 is None or np.array_equal(
                self._row, self.snpreader1.row
            ), "Expect snpreaders to have the same iids in the same order"
        return self._row

    @property
    def col(self):
        """*same as* :attr:`sid`"""
        if not hasattr(self, "_col"):
            assert (
                self.col_count < self.sid_materialize_limit
            ), "{:,} is too many sids to materialize".format(self.col_count)
            # !!!self.index0_list = self.snpreader0.sid_to_index((sid0 for sid0,sid1 in self._utilpairs[:])) # !!! can we do without these?
            # !!!self.index1_list = snpreader1.sid_to_index(sid1 for sid0,sid1 in self._utilpairs[:])# !!!can we do without these?
            self._col = np.array(list(",".join(pair) for pair in self._utilpairs[:]))
        return self._col

    @property
    def col_count(self):
        return len(self._utilpairs)

    @property
    def col_property(self):
        """*same as* :attr:`pos`"""
        if not hasattr(self, "_col_property"):
            self._col_property = np.zeros([self.sid_count, 3], dtype=np.int64)
        return self._col_property

    def copyinputs(self, copier):
        # doesn't need to self.run_once() because only uses original inputs !!!is this true?
        self.snpreader0.copyinputs(copier)
        if self.snpreader1 is not None:
            self.snpreader1.copyinputs(copier)

    def run_once(self):
        if self._ran_once:
            return

        self._ran_once = True
        self.col

    def _read(
        self,
        iid_index_or_none,
        sid_index_or_none,
        order,
        dtype,
        force_python_only,
        view_ok,
        num_threads,
    ):
        self.run_once()

        iid_count_in = self.iid_count

        if iid_index_or_none is not None:
            len(iid_index_or_none)
        else:
            range(iid_count_in)

        if sid_index_or_none is not None:
            len(sid_index_or_none)
            sid_index_out = sid_index_or_none
        else:
            raise NotImplementedError("TODO: This branch has not been implemented yet")
            # sid_index_out = splice(None)  # !!! test this

        pair_array = np.array(
            list(self._utilpairs[sid_index_out])
        )  # !!!make more efficient with npfromiter?
        snpreader1 = self.snpreader1 if self.snpreader1 is not None else self.snpreader0
        sid_index_inner_0 = self.snpreader0.sid_to_index(pair_array[:, 0])
        sid_index_inner_1 = snpreader1.sid_to_index(pair_array[:, 1])

        if self.snpreader1 is None:
            sid_index_inner_01 = np.unique(
                np.r_[sid_index_inner_0, sid_index_inner_1]
            )  # Index of every snp of interest
            inner_01 = self.snpreader0[iid_index_or_none, sid_index_inner_01].read(
                order=order,
                dtype=dtype,
                force_python_only=force_python_only,
                view_ok=True,
                num_threads=num_threads,
            )  # read every val of interest
            val_inner_01 = (
                inner_01.standardize().val if self.do_standardize else inner_01.val
            )

            sid_index_inner_01_reverse = {
                v: i for i, v in enumerate(sid_index_inner_01)
            }  # Dictionary of snp_index to position in sid_index_inner_01
            sid_index_inner_0_in_val = np.array(
                [sid_index_inner_01_reverse[i] for i in sid_index_inner_0]
            )  # Replace snp_index0 with column # in val_inner_01
            sid_index_inner_1_in_val = np.array(
                [sid_index_inner_01_reverse[i] for i in sid_index_inner_1]
            )  # Replace snp_index1 with column # in val_inner_01
            val_inner_0 = val_inner_01[
                :, sid_index_inner_0_in_val
            ]  # Extract the vals for the left snps of interest
            val_inner_1 = val_inner_01[
                :, sid_index_inner_1_in_val
            ]  # Extract the vals for the right snps of interest
        else:
            inner_0 = self.snpreader0[iid_index_or_none, sid_index_inner_0].read(
                order=order,
                dtype=dtype,
                force_python_only=force_python_only,
                view_ok=True,
                num_threads=num_threads,
            )  # read every val of interest
            inner_1 = self.snpreader1[iid_index_or_none, sid_index_inner_1].read(
                order=order,
                dtype=dtype,
                force_python_only=force_python_only,
                view_ok=True,
                num_threads=num_threads,
            )  # read every val of interest
            val_inner_0 = (
                inner_0.standardize().val if self.do_standardize else inner_0.val
            )
            val_inner_1 = (
                inner_1.standardize().val if self.do_standardize else inner_1.val
            )
        val = (
            val_inner_0 * val_inner_1
        )  # Element multiplication creates the vals for the pairs
        return val


# !!! keep these?




def epi_reml(
    pair_snps,
    pheno,
    covar=None,
    kernel_snps=None,
    output_dir="results",
    part_count=33,
    runner=None,
    override=False,
):
    from pysnptools.kernelreader import SnpKernel
    from pysnptools.standardizer import Unit
    import datetime
    from fastlmm.association import single_snp # type: ignore

    part_list = list(split_on_sids(pair_snps, part_count))
    part_pair_count = (part_count * part_count + part_count) / 2
    part_pair_index = -1
    print("part_pair_count={0:,}".format(part_pair_count))
    K0 = SnpKernel(
        kernel_snps or pair_snps, standardizer=Unit()
    ).read()  # Precompute the similarity
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    start_time = datetime.datetime.now()
    for i in range(part_count):
        part_i = part_list[i]
        for j in range(i, part_count):
            part_pair_index += 1
            pairs = _Pairs2(part_i) if i == j else _Pairs2(part_i, part_list[j])
            print(
                "Looking at pair {0},{1} which is {2} of {3}".format(
                    i, j, part_pair_index, part_pair_count
                )
            )
            output_file = "{0}/result.{1}.{2}.tsv".format(
                output_dir, part_pair_index, part_pair_count
            )
            if override or not os.path.exists(output_file):
                result_df_ij = single_snp(
                    pairs,
                    K0=K0,
                    pheno=pheno,
                    covar=covar,
                    leave_out_one_chrom=False,
                    count_A1=True,
                    runner=runner,
                )
                result_df_ij.to_csv(output_file, sep="\t", index=False)
                print(result_df_ij[:1])
                time_so_far = datetime.datetime.now() - start_time
                total_time_estimate = (
                    time_so_far * part_pair_count / (part_pair_index + 1)
                )
                print(total_time_estimate)


class TestPairs(unittest.TestCase):
    def test_run1(self):
        from pysnptools.snpreader import Bed

        root = Path(r"D:\OneDrive\programs\epireml")  # !!! make this work without this
        runner = None
        # runner = LocalMultiProc(multiprocessing.cpu_count(),just_one_process=False)

        bed_original = Bed(str(root / "syndata.bed"), count_A1=False)
        pheno = str(root / "pheno.txt")
        covar = str(root / "cov.txt")  # set to None, if none
        output_dir = r"m:/deldir/results.run1"
        part_count = 2

        epi_reml(
            bed_original[:, -20:],
            pheno,
            covar=covar,
            output_dir=output_dir,
            part_count=part_count,
            runner=runner,
            override=True,
        )
        # !!! check answer?

    def test_run2(self):
        from pysnptools.snpreader import Bed

        root = Path(r"D:\OneDrive\programs\epireml")  # !!! make this work without this
        runner = None
        # runner = LocalMultiProc(multiprocessing.cpu_count(),just_one_process=False)
        bed_original = Bed(
            str(root / "syndata.bed"), count_A1=False
        )  # Read only the first 10 SNPs
        pheno = str(root / "pheno.txt")
        covar = str(root / "cov.txt")
        output_dir = r"m:/deldir/results.run2"
        part_count = 1

        epi_reml(
            bed_original[:, :20],
            pheno,
            kernel_snps=bed_original,
            covar=covar,
            output_dir=output_dir,
            part_count=part_count,
            runner=runner,
            override=True,
        )

        # !!! check answer? against M:\deldir\refresults.run1 and 2


def getTestSuite():
    """
    set up composite test suite
    """

    test_suite = unittest.TestSuite([])
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPairs))
    return test_suite


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    TestPairs().test_run1()
    TestPairs().test_run2()

    suites = getTestSuite()
    r = unittest.TextTestRunner(failfast=True)
    r.run(suites)

    result = doctest.testmod()
    assert result.failed == 0, "failed doc test: " + __file__

    print("done")

    from pysnptools.snpreader import Bed

    if False:
        from pysnptools.snpreader import Bed
        from pysnptools.util import example_file  # Download and return local file name

        bed_file = example_file("doc/ipynb/all.*", "*.bed")
        bed = Bed(bed_file, count_A1=False)
        print(f"{bed.sid_count:,}")
        pairs = _Pairs(bed)
        print(f"{pairs.sid_count:,}")
        subset = pairs[:10, 10000:10010]
        print(subset.read().val.shape)
        print(subset.sid)

    if False:
        data_file = r"d:\OneDrive\programs\epiCornell\syndata.bed"
        if False:
            from pysnptools.snpreader import SnpData
            import numpy as np

            bed1 = Bed("../../tests/datasets/synth/all")
            print(bed1.iid_count, bed1.sid_count, bed1.iid_count * bed1.sid_count)
            # goal 1500 individuals x 27000 SNP
            snpdata1 = bed1.read()
            iid = bed1.iid
            sid = ["sid{0}".format(i) for i in range(27000)]
            val = np.tile(snpdata1.val, (3, 6))[:, :27000].copy()
            # snpdata = Pheno('pysnptools/examples/toydata.phe').read()         # Read data from Pheno format
            snpdata2 = SnpData(iid, sid, val)
            print(
                snpdata2.iid_count,
                snpdata2.sid_count,
                snpdata2.iid_count * snpdata2.sid_count,
            )
            Bed.write(snpdata2, data_file, count_A1=False)

        synbed = Bed(data_file)
        print(synbed.iid_count, synbed.sid_count, synbed.iid_count * synbed.sid_count)

        part_count = 1000
        part_list = list(split_on_sids(synbed, part_count))

        pairs00 = _Pairs(part_list[0])
        from fastlmm.association import single_snp

        pheno_fn = r"d:\OneDrive\programs\epiCornell\pheno.txt"
        cov_fn = r"d:\OneDrive\programs\epiCornell\cov.txt"
        results_df = single_snp(
            pairs00,
            K0=synbed,
            pheno=pheno_fn,
            covar=cov_fn,
            leave_out_one_chrom=False,
            count_A1=True,
        )

        if False:
            import pandas as pd
            for i, synbed_part_i in enumerate(synbed_part_list):  # noqa: F821
                for j, synbed_part_j in enumerate(synbed_part_list):  # noqa: F821
                    if j < i:
                        continue  # not break
                    print("Looking at pair {0},{1}".format(i, j))
                    pairs = (
                        _Pairs(synbed_part_i)
                        if i == j
                        else _Pairs(synbed_part_i, synbed_part_j)
                    )
                    # print(pairs.iid)
                    print("{:,}".format(pairs.sid_count))
                    # print(pairs.sid)
                    # print(pairs.pos)
                    # print(pairs.row_property)
                    snpdata = pairs.read()  #
                    # print(snpdata.val)

        import datetime
        from pysnptools.kernelreader import SnpKernel
        from pysnptools.standardizer import Unit
        from pysnptools.util.mapreduce1.runner import LocalMultiProc
        from pysnptools.util.mapreduce1 import map_reduce

        # runner=None
        runner = LocalMultiProc(1, just_one_process=False)

        part_pair_count = (part_count * part_count + part_count) // 2
        part_pair_index = -1
        print("part_pair_count={0:,}".format(part_pair_count))

        K0 = SnpKernel(synbed, standardizer=Unit()).read()  # Precompute the similarity

        start_time = datetime.datetime.now()
        for i, part_i in enumerate(part_list):

            def mapper1(j):
                # from fastlmm.association import single_snp
                # from pysnptools.snpreader import Pairs
                # print('Z')
                # part_j = part_list[j]
                # print('A')
                print(
                    "Looking at pair {0},{1} which is {2} of {3}".format(
                        i, j, part_pair_index + j + 1, part_pair_count
                    )
                )
                # pairs = Pairs(part_i) if i==j else Pairs(part_i,part_j)
                # result_df_ij = single_snp(pairs, K0=K0, pheno=pheno_fn, covar=cov_fn, leave_out_one_chrom=False, count_A1=True)
                # print(result_df_ij[:1])
                # return result_df_ij

            result_df_i = map_reduce(
                range(i, part_count),
                mapper=mapper1,
                reducer=lambda result_j_list: pd.concat(result_j_list),
                runner=runner,
                name="js",
            )
            part_pair_index += part_count - i
            time_so_far = datetime.datetime.now() - start_time
            total_time_estimate = time_so_far * part_pair_count / (part_pair_index + 1)
            print(total_time_estimate)
