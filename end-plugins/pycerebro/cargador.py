# -*- coding: utf-8 -*-
"""
Access module to the Cargador file storage.
More on Cargador settings, see section:
":ref:`carga-advanced-params`"

.. rubric:: Classes

* :py:class:`py_cerebro.cargador.Cargador`

"""

try:
	import xmlrpc.client as xmlrpc
except:
	import xmlrpclib as xmlrpc

import os, requests
from requests.utils import requote_uri
from .cclib import string_byte, PY3


class Cargador(xmlrpc.ServerProxy): 

	__slots__ = ('host', 'http_port', 'http_proxy')

	"""
	Cargador class to access the Cargador file storage.
	
	.. rubric:: Methods

	* :py:meth:`import_file() <py_cerebro.cargador.Cargador.import_file>`
	
	The following methods are inherited from the XML-RPC object:	
		
		catalogDelete(hash HASH, password STR)
		catalogDownload(hash HASH, siteList STR, CommenceFlags INT, userName STR, url STR, retryCount INT)
		catalogResolve(hash HASH)
		catalogUpload(hash HASH, siteList STR, CommenceFlags INT, userName STR, url STR, retryCount INT)
		controlIO(hash HASH, TableKind INT, Action INT)
		statusInfo()
		statusTables(tablesBitMaks INT, flags INT)
	
	More information about these methods, see the section:ref:`capi-xml-rpc`.
	"""	
	
	def __init__(self, _host, _rpc_port, _http_port, _http_proxy = ''):
		
		xmlrpc.ServerProxy.__init__(self, 'http://{0}:{1}'.format(_host, _rpc_port))
		self.host = _host
		self.http_port = _http_port
		self.set_proxy(_http_proxy)

	def set_proxy(self, _http_proxy):
		if _http_proxy is not None and len(_http_proxy) > 0:
			self.http_proxy = _http_proxy if _http_proxy.startswith('http') else 'http://' + _http_proxy
		else:
			self.http_proxy = ''

	def import_file(self, file_name, url):
		"""
		:param string file_name: path to the file.
		:param string url: storage place locator. The full path of the task, serves as locator, for example, 'Test project/Test task'.
		
		Imports the file in the file storage using HTTP protocol with PUT method
		and returns it to the hash in the base64 format.

		::
		
			rpc = py_cerebro.cargador.Cargador('server', 4040, 4080); # create a Cargador class object
			rpc.import_file('cargador.py', 'Test Folder')) # import the file in the Cargador file storage.
		"""

		c_url = u'{0}{1}/{2}'.format(u'' if url.startswith('/') else u'/', url.rstrip('/'), os.path.basename(file_name))
		host = u'{0}:{1}'.format(self.host, self.http_port)

		full_url = u'http://{0}{1}'.format(host, c_url)
		if not PY3: full_url = string_byte(full_url)

		content_lenght = '{0}'.format(os.stat(file_name).st_size)
		headers = {
			"User-Agent": "Python uploader",
			"Content-type": "application/octet-stream",
			"Accept": "text/plain",
			"host": host,
			"accept-encoding": "gzip, deflate",
			"content-length": content_lenght
		}

		ret = None
		with open(file_name, "rb") as fh:
			response = requests.put(requote_uri(full_url)
									, headers=headers
									, proxies = {'http': self.http_proxy} if len(self.http_proxy) else {}
									, data=fh.read()
									)
			if response.status_code != 201:
				raise RuntimeError('Attachment failed with code: ' + str(response.status_code) + '. reason: ' + response.reason)
			
			ret = response.content.decode('ascii').strip()
		
		return ret

	def download_file(self, file_name, hash):
		"""
		:param string file_name: path to the donwloaded file.
		:param string hash: file hash sum on storage.

		Downloads the file from the file storage using HTTP protocol with GET method
		and returns True on success.
		"""

		host = '{0}:{1}'.format(self.host, self.http_port)
		headers = {
			"User-Agent": "Python downloader",
			"Content-type": "application/octet-stream",
			"Accept": "text/plain",
			"host": host,
			"accept-encoding": "gzip, deflate",
		}
		full_url = "http://{0}/file?hash={1}".format(host, hash)

		response = requests.get(requote_uri(full_url)
								, headers=headers
								, proxies = {'http': self.http_proxy} if len(self.http_proxy) else {}
								, stream=True
								)
		if response.status_code == 200:
			with open(file_name, 'wb') as fh:
				for chunk in response.iter_content(1024):
					fh.write(chunk)

		return response.status_code == 200
