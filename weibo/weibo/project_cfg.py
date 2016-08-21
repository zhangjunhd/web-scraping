import yaml
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ProjectConf(object):
    def __init__(self, conf=''):
        if len(conf) == 0:
            conf = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'project.yaml')
        with open(conf, 'r') as f:
            self.conf = yaml.load(f)

    def get_cookies(self):
        return self.conf['cookie']

    def get_database_url(self):
        return self.conf['database']['url']

    def get_database_port(self):
        return self.conf['database']['port']

    def get_database_name(self):
        return self.conf['database']['db']

    def get_start_accounts(self):
        return self.conf['start_account']

    def __str__(self):
        return str(self.conf)

    __metaclass__ = Singleton


project_config = ProjectConf()


if __name__ == "__main__":
    prj_conf = ProjectConf()
    print prj_conf
    print prj_conf.get_cookies()
    print prj_conf.get_database_name()
    print prj_conf.get_database_port()
    print prj_conf.get_database_url()
    print prj_conf.get_start_accounts()
