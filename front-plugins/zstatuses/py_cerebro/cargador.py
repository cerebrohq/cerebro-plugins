# -*- coding: utf-8 -*-
"""
Access module to the Cargador file storage.
More on Cargador settings, see section:
":ref:`carga-advanced-params`"

.. rubric:: Classes

* :py:class:`py_cerebro.cargador.Cargador`

"""


import os
import urllib
import xmlrpc.client
import http.client

class Cargador(xmlrpc.client.ServerProxy):
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

	def __init__(self, _host, _rpc_port, _http_port):

		super(Cargador, self).__init__('http://{0}:{1}'.format(_host, _rpc_port))
		self.host = _host
		self.http_port = _http_port

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
		c_url = url
		if c_url.startswith('/'):
			c_url = c_url.lstrip('/')

		if c_url.endswith('/'):
			c_url = c_url.rstrip('/')

		c_url = c_url + '/' + os.path.basename(file_name)
		
		host = '{0}:{1}'.format(self.host, self.http_port)
		content_lenght = '{0}'.format(os.stat(file_name).st_size)
		headers = {
			"User-Agent": "Python uploader",
			"Content-type": "application/octet-stream",
			"Accept": "text/plain",
			"host": host,
			"accept-encoding": "gzip, deflate",
			"content-length": content_lenght}

		f = open(file_name, "rb")

		conn = http.client.HTTPConnection(self.host, self.http_port)
		conn.request("PUT", self.host + ':' + str(self.http_port) + '/' + urllib.parse.quote_plus(c_url), f, headers)

		response = conn.getresponse()
		#print(response.status, response.reason);
		if(response.status!=201):
			raise RuntimeError('Attachment failed with code: ' + str(response.status) + '. reason: ' + response.reason);

		ret = response.read().decode('ascii').strip()

		conn.close()
		return ret

