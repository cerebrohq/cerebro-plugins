# -*- coding: utf-8 -*-

import cerebro
import visible.config as config

def before_event(event):
	if event.event_type() == event.EVENT_CREATION_OF_TASK:
		if not cerebro.core.user_profile()[cerebro.aclasses.Users.DATA_ID] in config.ignore_users:
			event.definition().set_client_visible(True)

	if event.event_type() == event.EVENT_CREATION_OF_MESSAGE:
		if not cerebro.core.user_profile()[cerebro.aclasses.Users.DATA_ID] in config.ignore_users:
			event.set_client_visible(True)

