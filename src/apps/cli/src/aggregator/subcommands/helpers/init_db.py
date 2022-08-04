import pkgutil

# It's used in import_models() below...
# pylint: disable-next=unused-import
import aggregator.db.models
from aggregator.db.engine.engine_utils import get_db_engine
from aggregator.db.models.base import Base
from sqlalchemy_utils import create_database, database_exists, drop_database


def create_db(engine):
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    with engine.connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")


def import_models():
    # It's the import that it thinks is unused...
    # pylint: disable-next=undefined-variable
    loader = pkgutil.get_loader(models)
    modules = []
    for submodule in pkgutil.iter_modules(
            ['/'.join(loader.path.split('/')[0:-1])]):
        finder, submodule_name, _ = submodule
        module = finder \
            .find_module(submodule_name) \
            .load_module(submodule_name)
        modules.append(module)
    return modules


def create_hypertables(engine, modules):
    with engine.connect() as conn:
        txn = conn.begin()
        for module in modules:
            try:
                hype = getattr(module, 'hypertable')
                conn.execute(hype)
            except AttributeError:
                pass
        txn.commit()


def init_db():
    engine = get_db_engine()
    create_db(engine)
    model_list = import_models()
    Base.metadata.create_all(engine)
    create_hypertables(engine, model_list)
