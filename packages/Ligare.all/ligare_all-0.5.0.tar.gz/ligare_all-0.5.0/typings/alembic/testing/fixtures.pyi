"""
This type stub file was generated by pyright.
"""

from contextlib import contextmanager
from typing import Any, Dict
from sqlalchemy import testing
from sqlalchemy.testing.fixtures import TablesTest as SQLAlchemyTablesTest, TestBase as SQLAlchemyTestBase
from ..migration import MigrationContext
from ..util.sqla_compat import sqla_14

testing_config = ...
class TestBase(SQLAlchemyTestBase):
    is_sqlalchemy_future = ...
    @testing.fixture()
    def ops_context(self, migration_context): # -> Generator[Operations, Any, None]:
        ...
    
    @testing.fixture
    def migration_context(self, connection): # -> MigrationContext:
        ...
    
    @testing.fixture
    def connection(self): # -> Generator[Any, Any, None]:
        ...
    


class TablesTest(TestBase, SQLAlchemyTablesTest):
    ...


if sqla_14:
    ...
else:
    class FutureEngineMixin:
        __requires__ = ...
    
    
def capture_db(dialect=...): # -> tuple[Engine, list[Any]]:
    ...

_engs: Dict[Any, Any] = ...
@contextmanager
def capture_context_buffer(**kw): # -> Generator[BytesIO | StringIO, Any, None]:
    ...

@contextmanager
def capture_engine_context_buffer(**kw): # -> Generator[StringIO, Any, None]:
    ...

def op_fixture(dialect=..., as_sql=..., naming_convention=..., literal_binds=..., native_boolean=...): # -> ctx:
    class buffer_:
        ...
    
    
    class ctx(MigrationContext):
        ...
    
    

class AlterColRoundTripFixture:
    __requires__ = ...
    def setUp(self): # -> None:
        ...
    
    def tearDown(self): # -> None:
        ...
    


