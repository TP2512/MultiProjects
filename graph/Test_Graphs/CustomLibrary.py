from TestObject import TestObject
from robot.api.logger import info, debug, trace, console


class CustomLibrary:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self,tc_session_reset=True) -> None:
        self.ROBOT_LIBRARY_SCOPE = 'TEST' if tc_session_reset else 'SUITE'
        console(f'Library Scope is {self.ROBOT_LIBRARY_SCOPE}')
        self._session = None
        # self.dbaname = ''
        self._connection: TestObject = None

    def connect(self, mongostring):
        self._connection = TestObject(mongostring)
        info(f'Connection established to {mongostring}')

    def disconnect(self):
        self._connection = None
        info('Connection closed')

    @property
    def connection(self):
        if not self._connection:
            raise SystemError('No Connection established! Connect to DB first!')
        return self._connection

    @property
    def session(self):
        if self._session is None:
            raise PermissionError('No valid user session. Authenticate first!')
        return self._session

    def dbconnect(self, dbname) -> None:
        self._session = self.connection.dbuse(dbname)

    def dbdisconnect(self):
        self.connection.dbclose()

    def get_all_collections(self):
        return self.connection.get_all_collections(self.session)


