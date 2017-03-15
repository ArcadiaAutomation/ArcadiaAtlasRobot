# -*- coding: utf-8 -*-
from os.path import abspath, join as path_join
from random import choice
from string import ascii_lowercase

import pyautogui as ag
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.api import logger as LOGGER

from ..errors import ScreenshotFolderException


class _Screenshot(object):
    @property
    def _make_up_filename(self):
        try:
            suitename = BuiltIn().get_variable_value('${SUITE NAME}')
            suitename = suitename.replace(' ','')
            suitename = suitename.split(".")
            testname = BuiltIn().get_variable_value('${TEST NAME}')
            testname = testname.split("_")
            if len(suitename) > 1:
                path = 'screenshot-ImageHorizon-' + suitename[4] + '-' + testname[0]
            else:
                path = 'screenshot-ImageHorizon-' + suitename[0] + '-'+ testname[0]
        except RobotNotRunningError:
            LOGGER.info('Could not get suite name, using '
                        'default naming scheme')
            path = 'ImageHorizon-screenshot'
        path = '%s-%d.png' % (path, self.screenshot_counter)
        self.screenshot_counter += 1
        return path

    def take_a_screenshot(self):
        '''Takes a screenshot of the screen.

        This keyword is run on failure if it is not overwritten when
        `importing` the library.

        Screenshots are saved to the current working directory or in the
        ``screenshot_folder`` if such is defined during `importing`.

        The file name for the screenshot is the current suite name with a
        running integer appended. If this keyword is used outside of Robot
        Framework execution, file name is this library's name with running
        integer appended.
        '''
        target_dir = self.screenshot_folder if self.screenshot_folder else ''
        if not isinstance(target_dir, basestring):
            raise ScreenshotFolderException('Screenshot folder is invalid: '
                                            '"%s"' % target_dir)
        path = self._make_up_filename
        path = abspath(path_join(target_dir, path))
        LOGGER.info('Screenshot taken: {0}<br/><img src="{0}" '
                    'width="100%" />'.format(path), html=True)
        ag.screenshot(path)
