import sys

from loguru import logger

from sumdups import Sumdups

# -------------------------------------------------------------------------------

logger.remove(0)
logger.add(sys.stdout, level="TRACE")

# @pytest.fixture
# def atfile():
#    name = 'yellow'
#    with open(name, 'w') as fp:
#        print('lemon\n@norecurse\ngoldenrod', file=fp)
#    yield '@' + name
#    os.unlink(name)

# -------------------------------------------------------------------------------


class TestSumdups:

    # pylint: disable=too-few-public-methods

    def test_one(self):
        print(Sumdups.fill)
