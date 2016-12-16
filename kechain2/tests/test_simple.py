import betamax
import kechain2

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'kechain2/tests/cassettes'


class TestApi(object):
    def test_parts(self):
        from kechain2.api import session

        with betamax.Betamax(session) as vcr:
            vcr.use_cassette('parts')

            kechain2.login("***REMOVED***")

            part_set = kechain2.parts()

            assert len(part_set) == 29

    def test_part(self):
        from kechain2.api import session

        with betamax.Betamax(session) as vcr:
            vcr.use_cassette('part')

            kechain2.login("***REMOVED***")

            gears = kechain2.part('Bike').property('Gears')

            assert gears.value == 6
