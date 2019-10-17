# -*- coding: utf-8 -*-

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
import smtplib
import time
import sys
import tempfile
import os
import traceback
import zipfile
import re

# Python version
PY3 = sys.version_info[0] == 3

def formatException(e):
	exception_list = traceback.format_stack()
	exception_list = exception_list[:-2]
	exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
	exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
	exception_str = "CC traceback (most recent call last):\n"
	exception_str += "".join(exception_list)
	# Removing the last \n
	exception_str = exception_str[:-1]
	return exception_str

def extractFilePath(filePath):
	return filePath.replace('\\', '/').rsplit('/', 1)[0]

def extractFileName(filePath):
	p = filePath.replace('\\', '/').rsplit('/', 1);
	return p[1] if len(p) >= 2 else p[0];
	
def hash16_64(b16_str):
	"""
	:param string b16_str: hash in base16 format
	:returns: hash in base64 format
	:rtype: string

	Converts hash string from base16 to base64 format.
	"""
	if len(b16_str)!=64:
		raise Exception('Wrong hash length (muse be 64)');

	ba = base64.b16decode(b16_str.encode('ascii'));
	return base64.standard_b64encode(ba).decode('ascii').replace('+', '-').replace('/', '_').replace('=', '~')

def hash64_16(b64_str):
	"""
	:param string b64_str: hash in base64 format
	:returns: hash in base16 format
	:rtype: string

	Converts hash string from base64 to base16 format.
	"""
	ba = base64.standard_b64decode(b64_str.replace('-', '+').replace('_', '/').replace('~', '=').encode('ascii'))
	ret = base64.b16encode(ba).decode('ascii')
	if len(ret)!=64:
		raise RuntimeError('Wrong hash length (muse be 64): ' + ret);
	return ret;
	
def correctFileName(fname):
	return fname\
	.replace("\r", "_") \
	.replace("\n", "_") \
	.replace("\\", "_") \
	.replace("/", "_") \
	.replace("*", "_") \
	.replace("?", "_") \
	.replace("|", "_") \
	.replace(">", "_") \
	.replace("<", "_") \
	.replace("\"", "") \
	.replace("'", "") \
	.replace("`", "") \
	.replace(" ", "_");

def splitEmailAddr(mailTo, bcc):
	to_list = re.split(';|,|\n|\r|\s', mailTo)

	uniqMail = set();
	for a in to_list:
		if a and len(a) > 0:
			uniqMail.add(a);

	for a in bcc:
		uniqMail.add(a);

	toAddrs = list();
	for a in uniqMail:
		a = a.strip();
		if a and len(a) > 0:
			toAddrs.append(a);

	return toAddrs;


def email(smtpOptions,  emailAddr, text, subj, attachments=list(), bcc=list()):
	# <smtpOptions> must be a dictianry.
	# Mandatory keys are:
	#	* addr - smtp server
	# Optional keys are:
	#	* from - sender mail address.
	#		default: to "Cerebro Mail Service <no-reply@cerebrohq.com>"
	#	* ssl - use SSL.
	#		default: False
	#	* tls - start TLS
	#		default: False
	#	* login - user name to login on SMTP
	#		default: None
	#	* psswd - user password to login on SMTP
	#		default: None
	#	* log - log email sent
	#		default: False
	#	* skip - skip rea; mail send. Used for debug
	#		default: False
	#	* debugEmail - override mail adress
	#
	#   * To - set To header
	#   * Cc - set Cc header
	#
	#   * zipFile - compress all atachments in zip and attach it
	#
	# emailAddr - is a comma-separated list of emails
	#
	# attachments must be list of two component entries: [<bytearray> - atachment content, <str>  - attachment name]
	#
	# Example use:
	# 	email({'addr' : 'cerebrohq.com', 'ssl' : False},  'user@example.com', 'message text', 'message subject')

	mailTo = emailAddr;

	if 'debugEmail' in smtpOptions:
		toAddrs = [ smtpOptions['debugEmail'] ];
		print('email adress overriden {0} -> {1}'.format(emailAddr,  smtpOptions['debugEmail']));

	else:
		toAddrs = splitEmailAddr(mailTo, bcc);
		#print('emailAddr ', emailAddr);
		#print('toaddr ', toAddrs);
		#print('uniqMail ', uniqMail);

	if 'from' in smtpOptions:
		mailFrom = smtpOptions['from'];
	else:
		mailFrom = 'Cerebro Mail Service <no-reply@cerebrohq.com>';

	msg = MIMEMultipart();
	msg['Subject'] = Header(subj, 'utf-8');
	msg['From'] = mailFrom;
	msg['To'] = smtpOptions['To'] if ('To' in smtpOptions) else mailTo;
	if 'Cc' in smtpOptions:
		msg['Cc'] = smtpOptions['Cc'];

	try:
		if str('<html>') in text:
			part2 = MIMEText(text.encode('utf-8'), 'html', 'utf-8')
		else:
			part2 = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
	except Exception as ex:
		msgErr = time.strftime('%Y-%m-%d %H:%M:%S') + ': email encode FAILED <' + emailAddr + '> : ' + str(ex) + "\n";
		msgErr += "MESSAGE DUMP BEGIN:\n"
		msgErr += str(base64.encodebytes(text.encode('unicode_internal')), 'ascii')
		msgErr += "MESSAGE DUMP END\n"

		if ('log' in smtpOptions) and smtpOptions['log']:
			sys.stderr.write(msgErr);
			sys.stderr.flush();

		raise Exception(msgErr);

	msg.attach(part2)

	if 'zipFile' in smtpOptions:
		if len(attachments) > 0:
			zFileName = tempfile.mktemp();

			zFile = zipfile.ZipFile(zFileName, mode='a', compression=zipfile.ZIP_DEFLATED);
			for attach in attachments:
				zFile.writestr(correctFileName(attach[1]), attach[0]);
			zFile.close()

			attachments = [ [open(zFileName , 'rb').read(), smtpOptions['zipFile']] ];
			os.remove(zFileName);

	for attach in attachments:
		attachment = MIMEBase("application", "octet-stream")
		attachment.add_header('Content-Disposition', 'attachment', filename = correctFileName(attach[1]))
		attachment.add_header('Content-Transfer-Encoding', 'base64')
		attachment.set_payload(str(base64.encodebytes(attach[0]), 'ascii'))
		msg.attach(attachment)


	try:
		if not(('skip' in smtpOptions) and smtpOptions['skip']):

			useTLS = ('tls' in smtpOptions and smtpOptions['tls']);
			useSSL = ('ssl' in smtpOptions and smtpOptions['ssl']);

			port = 25;
			if useSSL:
				port = 465;

			if 'port' in smtpOptions:
				port = smtpOptions['port'];

			if useSSL:
				smtp = smtplib.SMTP_SSL(smtpOptions['addr'], port)
			else:
				smtp = smtplib.SMTP(smtpOptions['addr'], port)

			if useTLS:
				smtp.ehlo();
				smtp.starttls();
				smtp.ehlo();

			if 'login' in smtpOptions and len(smtpOptions['login'])>0:
				smtp.login(smtpOptions['login'], smtpOptions['psswd'])

			smtp.sendmail(mailFrom, toAddrs, msg.as_string())

		if ('log' in smtpOptions) and smtpOptions['log']:
			print(time.strftime('%Y-%m-%d %H:%M:%S') + ': email sent to: ', emailAddr);

	except Exception as ex:
		if ('log' in smtpOptions) and smtpOptions['log']:
			msgErr = time.strftime('%Y-%m-%d %H:%M:%S') + ': email FAILED <' + emailAddr + '> : ' + str(ex) + "\n";
			sys.stderr.write(msgErr);
			sys.stderr.flush();
		raise;

def isRunTime(category,  timeIntervalSec):
	tmp = tempfile.gettempdir();
	fn = tmp + '/cerebro.IsTime.' + category + '.signal';
	if not os.path.exists(fn):
		open(fn, 'w').write(time.ctime());
		return True;

	ft = os.path.getmtime(fn);
	gt = time.time();
	if ft + timeIntervalSec <= gt:
		open(fn, 'w').write(time.ctime());
		return True;

	return False;

def has_flag(flags, flag):
	"""
	:param int flags: flag values.
	:param int flag: flag.
	:returns: "True" if the flag is set, otherwise - "False".
	:rtype:  bool

	Checks if the flag is set in flags.
	"""
	return ((flags & (1 << flag))!=0)

def smtpOptions(cron_conf):
	ret = {
		'addr' : cron_conf.MAIL_SMTP
		, 'ssl' : False
		, 'log' : cron_conf.DEBUG
		, 'from' : cron_conf.MAIL_FROM
	};

	if 'smtp_port' in cron_conf.OPTS:
		ret['port'] = cron_conf.OPTS['smtp_port'];

	if 'smtp_tls' in cron_conf.OPTS:
		ret['tls'] = cron_conf.OPTS['smtp_tls'];

	if len(cron_conf.MAIL_LOGIN)>0:
		ret['login'] = cron_conf.MAIL_LOGIN;

	if len(cron_conf.MAIL_PSSWD)>0:
		ret['psswd'] = cron_conf.MAIL_PSSWD;

	if cron_conf.DEBUG:
		ret['debugEmail'] = cron_conf.MAIL_ADMIN;

	return ret;

def string_unicode(string):
	try:
		if PY3:
			if not isinstance(string, str):
				string = str(string.decode('utf-8'))
		else:
			if not isinstance(string, unicode):
				string = unicode(string.decode('utf-8'))
	except:
		pass
	return string

def string_byte(string):
	try:
		if PY3:
			if isinstance(string, str):
				string = string.encode('utf-8')
		else:
			if isinstance(string, unicode):
				string = string.encode('utf-8')
	except:
		pass
	return string

def error_unicode(exception):
	if PY3:
		return str(exception)
	else:
		return string_unicode(exception.message)
