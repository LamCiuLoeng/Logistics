# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2012-6-1
#  @author: CL.Lam
#  Description:
###########################################
'''
from datetime import datetime as dt
import random, os
from elaphe import code128
from sys2do.setting import UPLOAD_FOLDER, UPLOAD_FOLDER_PREFIX, UPLOAD_FOLDER_URL
from sys2do.model import UploadFile
from sys2do.util.common import _error, _info
import traceback


def generate_barcode_file(s, ext = '.jpg'):
    if not s : return None
    try:
        if len(s) % 2 != 0 :    s = '0' + s
        codestring = '^105%s' % s  #code 128 C format
        c = code128.Code128()

        f = c.render(str(codestring), options = dict(includetext = True, height = 0.4, textxalign = 'center'), scale = 2, margin = 5)
        file_name = "%s%.4d%s" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000), ext)
        file_dir = os.path.join(UPLOAD_FOLDER_PREFIX, UPLOAD_FOLDER)
        if not os.path.exists(file_dir): os.makedirs(file_dir)
        full_path = os.path.join(file_dir, file_name)
        f.save(full_path)
        return UploadFile(name = file_name,
                   path = os.path.join(UPLOAD_FOLDER, file_name),
                   url = "/".join([UPLOAD_FOLDER_URL, file_name]),
                   size = os.path.getsize(full_path),
                   type = ext[1:],
                   )
    except:
        _error(traceback.print_exc())
        return None





if __name__ == "__main__":

#    barcode('qrcode', '\u我顶你个肺啊', options = dict(version = 9, eclevel = 'M'), margin = 10, data_mode = '8bits')   # Generates PIL.EpsImageFile instance
#    _.show()

#    codestring = '^105109864805319'
#    codestring = '^105120607000001'

    print generate_barcode_file('19864805319')
