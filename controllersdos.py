# -*- coding: utf-8 -*-
from odoo import http
from openerp.addons.web.controllers.main import serialize_exception,content_disposition
import base64
import random
import string
import xlsxwriter
import xlwt
from datetime import datetime
from io import BytesIO
import threading
from PIL import Image
import pyqrcode
import PyPDF2
import png
import os
import pandas as pd
import ast
from xml.sax.saxutils import escape, unescape
import requests
import shutil
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from io import StringIO, BytesIO
import responses
import mimetypes
from flask import Response
from werkzeug.datastructures import Headers

import time
import pdfkit

class AplicacionHaEvaluateController(http.Controller):

    @http.route('/impresionexcel/evaluate/<condiciontiempo>/<rolee>', auth='public')
    def index(self,condiciontiempo,rolee, **kw):
        return '<html><head></head><body><p>Prueba</p></body><html>'

    @http.route('/testc',auth='public')
    def index2135234(self, **kw):
        return '<p>prueba impresi ha actualizada la ultima todas las importaciones</p>'
