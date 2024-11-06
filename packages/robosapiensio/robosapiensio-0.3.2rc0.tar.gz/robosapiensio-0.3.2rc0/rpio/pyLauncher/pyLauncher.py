from rpio.utils.auxiliary import *


def launch(launchFile='launch.xml'):
    """Function to launch one or more python software component using a launch description file

        :param [launchFile]: [launch description file(XML)], defaults to [launch.xml]
        :type [launchFile]: [String](, optional)
        ...
        :return: [Functions returns nothing]
        :rtype: [None]
        """

    # 0. interpret launch file
    launchDescription = parse_launch_xml(file=launchFile,formalism="python")
    print(launchDescription)

    print(extractCommands(launchDescription))

    # 1. launch all commands at once
    execute_commands(extractCommands(launchDescription))

