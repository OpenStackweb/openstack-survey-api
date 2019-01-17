
class DBRouter(object):
    """
    A router to control all database operations on models in the
    reports application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read reports models go to openstack_db.
        """
        if model._meta.app_label == 'reports':
            return 'openstack_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write reports models go to openstack_db.
        """
        if model._meta.app_label == 'reports':
            return 'openstack_db'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """

        if app_label == 'reports':
            return False
        return None