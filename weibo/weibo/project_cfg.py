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
        if not self.rotate_worker():
            return self.conf['cookie']
        total_worker = self.total_worker()
        if total_worker <= 1:
            return self.conf['cookie']
        my_id = self.worker_id()
        tmp = []
        for i in range(len(self.conf['cookie'])):
            if i % total_worker == my_id:
                tmp.append(self.conf['cookie'][i])
        return tmp

    def total_worker(self):
        return self.conf['worker']['total']

    def worker_id(self):
        return self.conf['worker']['id']

    def rotate_worker(self):
        return self.conf['cookie_setting']['rotate_worker']

    def get_cookie_rotate_time(self):
        return self.conf['cookie_setting']['rotate_hour'] * 3600

    def get_database_url(self):
        return self.conf['database']['url']

    def get_database_port(self):
        return self.conf['database']['port']

    def get_database_name(self):
        return self.conf['database']['db']

    def get_start_accounts(self):
        return self.conf['start_account']

    def scrawl_fan_and_follow(self):
        return self.conf['scrawl']['fan_and_follow']

    def scrawl_user_profile(self):
        return self.conf['scrawl']['user_profile']

    def scrawl_user_weibo(self):
        return self.conf['scrawl']['user_weibo']

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
    print prj_conf.scrawl_fan_and_follow()
    print prj_conf.scrawl_user_profile()
    print prj_conf.scrawl_user_weibo()
