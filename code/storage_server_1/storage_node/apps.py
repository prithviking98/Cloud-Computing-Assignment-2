from django.apps import AppConfig


class StorageNodeConfig(AppConfig):
    name = 'storage_node'

    def read(self):
    	#notify ui_server that you are up
