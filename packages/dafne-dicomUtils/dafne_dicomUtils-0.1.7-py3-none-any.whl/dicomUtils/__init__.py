#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Copyright (c) 2021 Dafne-Imaging Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import flexidep
from . import resources
flexidep.standard_install_from_resource(resources, 'runtime_dependencies.cfg')

from .dicom3D import load3dDicom, save3dDicom
from .misc import loadDicomFile, dosma_volume_from_path, realign_medical_volume

def medical_volume_from_path(*args, **kwargs):
    volume, *_ = dosma_volume_from_path(*args, **kwargs)
    return volume

from .padorcut import padorcut