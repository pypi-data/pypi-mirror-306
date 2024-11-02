from .deeplake_db import Deeplake_DB
from .weaviate_db import Weaviate_DB


def get_vectorstore(db_type):
    if db_type == 'weaviate':
        return Weaviate_DB()
    elif db_type == 'deeplake':
        return Deeplake_DB()
    else:
        raise ValueError("Invalid db_type")
