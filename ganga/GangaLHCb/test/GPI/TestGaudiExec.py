

from os import makedirs, path
import shutil
from tempfile import gettempdir

from GangaCore.GPIDev.Base.Proxy import stripProxy
from GangaCore.testlib.GangaUnitTest import GangaUnitTest


class TestGaudiExec(GangaUnitTest):

    def testInternal(self):

        from GangaCore.GPI import GaudiExec, Job, LocalFile, DiracFile

        tmp_fol = gettempdir()
        gaudi_testFol = path.join(tmp_fol, 'GaudiExecTest')
        shutil.rmtree(gaudi_testFol, ignore_errors=True)
        makedirs(gaudi_testFol)
        gaudi_testOpts = path.join(gaudi_testFol, 'testOpts.py')
        with open(gaudi_testOpts, 'w+') as temp_opt:
            temp_opt.write("print('hello')")

        assert path.exists(gaudi_testOpts)

        gr = GaudiExec(directory=gaudi_testFol, options=[LocalFile(gaudi_testOpts)])

        assert isinstance(stripProxy(gr).getOptsFiles()[0], stripProxy(LocalFile))

        reconstructed_path = path.join(stripProxy(gr).getOptsFiles(
        )[0].localDir, stripProxy(gr).getOptsFiles()[0].namePattern)

        assert reconstructed_path == gaudi_testOpts

        assert open(reconstructed_path).read() == "print('hello')"

        j = Job()
        j.application = gr

        assert isinstance(j.application, GaudiExec)

        df = DiracFile(lfn='/not/some/file')

        gr.options = [df]

        assert gr.options[0].lfn == df.lfn

        shutil.rmtree(gaudi_testFol, ignore_errors=True)
