from cleo import Application as BaseApplication

from kal.initialize import init
from kal import meta, commands as cmds


class Application(BaseApplication):
    def __init__(self, *args, **kwargs):
        init()
        super().__init__('kal', meta.__version__)
        for command in self.get_default_commands():
            self.add(command)

    def get_default_commands(self):
        return [
            cmds.EnvCommand(),
            cmds.CloneCommand(),
            cmds.KSTCommand(),
            cmds.UTCCommand(),
            cmds.BoxCommand(),
            cmds.LinkCommand(),
            cmds.RunCommand(),
            cmds.DockerCommand(),
            cmds.OcelCommand(),
        ]
