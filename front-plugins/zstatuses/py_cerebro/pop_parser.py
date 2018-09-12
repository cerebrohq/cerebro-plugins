import poplib
import email
import sys
import os

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir)

import cclib

def checkConfig(cron_conf):
	return True \
		and 'replier_pop_addr' in cron_conf.OPTS \
		and 'replier_pop_login' in cron_conf.OPTS \
		and 'replier_pop_psswd' in cron_conf.OPTS;
		

def decodeHeader(header):
	H = email.header.decode_header(header);

	res = '';
	for h in H:
		if h[1] != None:
			res += h[0].decode(h[1]) + ' ';
		else:
			res += h[0] + ' ';

	return res;

def getHeader(msg,  headName):
	header = msg.__getitem__(headName)
	if header:
		return decodeHeader(header);
	else:
		return None;

def extractDoc(M, index):
	popMsg = M.retr(index + 1);
	M.dele(index + 1);

	jmsg = b"\n".join(popMsg[1]);
	mime = email.message_from_bytes(jmsg);

	plainDoc = None;
	htmlDoc = None;
	attachArray = list();
	subject = None;

	subject = getHeader(mime,  'Subject');

	for msg in mime.walk():
		contentType = msg.get_content_type();
		contentCharset = msg.get_content_charset()
		if not contentCharset:
			contentCharset = 'UTF-8';

		# print('> msg: type: ',  contentType, ' charSet:', contentCharset);
		if contentType.startswith('text') and contentCharset and contentCharset!='':
			if not plainDoc or not htmlDoc:
				loadDec = msg.get_payload(decode=True);
				doc = loadDec.decode(contentCharset);

				if not plainDoc and contentType.startswith('text/plain'):
					plainDoc = doc;

				if not htmlDoc and contentType.startswith('text/html'):
					htmlDoc = doc;

		fileNameHead = msg.get_filename();
		if fileNameHead:
			fileName = decodeHeader(fileNameHead);
			file = msg.get_payload(decode=True);
			attachArray.append([fileName,  file]);

	if plainDoc:
		return [subject,  plainDoc,  attachArray, mime, jmsg];
	else:
		return [subject,  htmlDoc,  attachArray, mime, jmsg];

def connectServer(cron_conf):
	if 'replier_pop_ssl' in cron_conf.OPTS and cron_conf.OPTS['replier_pop_ssl']:
		M = poplib.POP3_SSL(cron_conf.OPTS['replier_pop_addr'],  995)
	else:
		M = poplib.POP3(cron_conf.OPTS['replier_pop_addr'])

	M.user(cron_conf.OPTS['replier_pop_login'])
	M.pass_(cron_conf.OPTS['replier_pop_psswd'])

	return M;


def reportText(cron_conf, text, doc, adminSubject):
	smtpOptions = cclib.smtpOptions(cron_conf);
	mime = doc[3];
	jmsg = doc[4];


	subject = getHeader(mime,  'Subject');
	retAddr = getHeader(mime,  'Return-Path');

	
	if len(retAddr) > 0:
		cclib.email(smtpOptions, retAddr, text, subject);

	if len(cron_conf.MAIL_ADMIN) > 0:
		cclib.email(smtpOptions, cron_conf.MAIL_ADMIN, text, adminSubject,  [[jmsg,  'user.email']])

def reportError(cron_conf, ex, doc):
	if cron_conf.DEBUG:
		print('XCPT while msg process:',  ex);

	ex_text = str(ex).partition("\n");
	text = "Email reply processing error: " + ex_text[0];

	if len(ex_text[2]) > 0:
		text += "\n\n\n\n";
		text += "Problem techinal info:\n";
		text += ex_text[2];

	reportText(cron_conf, text, doc, 'pop3 processing error')
