from django.db import connection, transaction

from .database_lock import DatabaseLock


class DatabaseAdvisoryLock(DatabaseLock):
    """
    This class is pretty much same as DatabaseLock except that
    it uses transaction level advisory lock which ensures that
    lock acquisition and lock lease renewal are mutually exclusive
    operations as far as all the database calls are concerned.
    This will work ONLY with Postgres.
    """

    def __init__(self, name, lease_time, record_id):
        super(DatabaseAdvisoryLock, self).__init__(name, lease_time, record_id)
        self.advisory_lock_query = f"SELECT pg_advisory_xact_lock({self.record_id})"

    def _acquire_lock(self) -> bool:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.execute(self.advisory_lock_query)
            return self._do_acquire_lock()

    def renew_lease(self) -> bool:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.execute(self.advisory_lock_query)
            return self._do_renew_lease()
