# -*- coding: utf-8 -*-
from tiramisu.option import FilenameOption, OptionDescription
def get_description():
    usbpath = FilenameOption('usbpath', "Chemin d'accès", properties=('mandatory',))
    descr = OptionDescription("filename1", "Simple filename", [usbpath])
    return descr
