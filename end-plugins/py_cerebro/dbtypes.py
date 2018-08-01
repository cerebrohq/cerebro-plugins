# -*- coding: utf-8 -*-

"""
The py_cerebro.dbtypes module contains descriptions of tuples and bit flags,
used for work with the database.
"""

TASK_DATA_ = ''
"""
.. rubric:: Task tuple fields
"""
TASK_DATA_MTM							= 0
"""
Time of data change.
"""
TASK_DATA_ID								= 1
"""
Task ID.
"""
TASK_DATA_PARENT_ID						= 2
"""
Parent task ID.
"""
TASK_DATA_PLANNED_DELTA				= 3
"""
Obsolete, not used.
"""
TASK_DATA_NAME							= 4
"""
Task name.
"""
TASK_DATA_PARENT_URL						= 5
"""
Full path to the parent task. Example: */Test project/Scene 1/*
"""
TASK_DATA_ACTIVITY_NAME					= 6
"""
Activity name.
"""
TASK_DATA_ACTIVITY_ID						= 7
"""
Activity ID.
"""
TASK_DATA_SELF_USERS_DECLARED			= 8
"""
Time, signed off by users, minutes. Type - float.
"""
TASK_DATA_SELF_USERS_APPROVED			= 9
"""
Confirmed signed off time, minutes. Type - float.
"""
TASK_DATA_CREATED						= 10
"""
Task creation time.
"""
TASK_DATA_PRIORITY						= 11
"""
Task priority.
"""
TASK_DATA_PROGRESS						= 12
"""
Task progress. Type - float, from 0.0 to 100.0.
"""
TASK_DATA_PLANNED						= 13
"""
Planned working time for the task, hours. Type - float.
"""
TASK_DATA_USERS_DECLARED					= 14
"""
Time, signed off by users on current task and its subtasks, hours. Type - float.
"""
TASK_DATA_USERS_APPROVED					= 15
"""
Confirmed signed off time on current task and its subtasks, hours. Type - float.
"""
TASK_DATA_THUMBS							= 16
"""
Thumbnail hash sums. Type - string. Separator ';'.
"""
TASK_DATA_FLAGS							= 17
"""
Task flags.
"""
TASK_DATA_MODERATOR_ID					= 18
"""
ID of a user who changed the task.
"""
TASK_DATA_CREATOR_ID						= 19
"""
Id of a user who created the task.
"""
TASK_DATA_MODIFIED						= 20
"""
Time when the task was modified.
"""
TASK_DATA_ALLOCATED						= 21
"""
Users allocated to the task. Type - string. Separator ';'.
"""
TASK_DATA_OFFSET							= 22
"""
Calculated start time of the task, days from 01.01.2000. Type - float.
"""
TASK_DATA_DURATION						= 23
"""
Calculated duration of the task, days. Type - float.
"""
TASK_DATA_PROJECT_ID						= 24
"""
ID of the project, the task belongs to.
"""
TASK_DATA_PRIVILEGE						= 25
"""
Current user's access rights to the task. Type - integer.
"""
TASK_DATA_HUMAN_START					= 26
"""
User-defined task start time, days from 01.01.2000. Type - float.
"""
TASK_DATA_HUMAN_FINISH					= 27
"""
User-defined task finish time, days from 01.01.2000. Type - float.
"""
TASK_DATA_SELF_BUDGET						= 28
"""
Task budget.
"""
TASK_DATA_SELF_SPENT						= 29
"""
Task costs.
"""
TASK_DATA_BUDGET							= 30
"""
Total budget for the task and its subtasks.
"""
TASK_DATA_SPENT						= 31
"""
Total costs of the task and its subtasks.
"""
TASK_DATA_RESOURCE_SELF_DECLARED			= 32
"""
Signed off time of a material resource, minutes. Type - float.
"""
TASK_DATA_RESOURCE_SELF_APPROVED			= 33
"""
Confirmed signed off time of a material resource, minutes. Type - float.
"""
TASK_DATA_RESOURCE_DECLARED				= 34
"""
Signed off time of a material resource for the task and its subtasks, hours. Type - float.
"""
TASK_DATA_RESOURCE_APPROVED				= 35
"""
Confirmed signed off time of a material resource for the task and its subtasks, hours. Type - float.
"""
TASK_DATA_SELF_STATUS						= 36
"""
User-defined (manually set) task status.
"""
TASK_DATA_CC_STATUS						= 37
"""
Calculated (automatic) task status.
Calculated status may differ from the user-defined one, as it may be inherited from its parent task.
Calculated status is the effective (actual) status of the task.
"""
TASK_DATA_CC_STATUS_STAT				= 38
"""
Status summary on the parent task.
"""
TASK_DATA_ORDER						= 39
"""
Task order number.
"""

TASK_FLAG_ = ''
"""
.. rubric:: Task flags
"""
TASK_FLAG_DELETED					= 0
"""
Task deleted.
"""
TASK_FLAG_PERM_INHERIT_BLOCK			= 1
"""
Permission inheritance is reset for the task.
"""
TASK_FLAG_CLOSED						= 2
"""
Task closed.
"""
TASK_FLAG_TASK_AS_EVENT				= 3
"""
Task marked as event.
"""
TASK_FLAG_SUSPENED					= 4
"""
Task paused.
"""
TASK_FLAG_FORUM_LOCKED				= 5
"""
Task Forum locked.
"""
TASK_FLAG_CLOSED_EFFECTIVE			= 30
"""
Task closed, because its parent task is closed also.
"""
TASK_FLAG_SUSPENED_EFFECTIVE			= 31
"""
Task paused, because its parent task is closed also.
"""
TASK_FLAG_HAS_CHILD					= 32
"""
Task has subtasks.
"""
TASK_FLAG_HAS_MESSAGES				= 33
"""
There are messages in the task Forum.
"""
TASK_FLAG_NEED_ANSWER				= 34
"""
Task is reply pending (according to current user's access rights).
"""
TASK_FLAG_HAS_SUB_PERMS				= 35
"""
???
"""
TASK_FLAG_ASSIGNED					= 38
"""
Current user is allocated to this task.
"""
TASK_FLAG_INTEREST					= 39
"""
Current user follows this task.
"""
TASK_FLAG_LAST_EV_CLIENT_VIS			= 44
"""
The last message in the task Forum is visible for Clients.
"""
TASK_FLAG_LAST_EV_APPROVED			= 45
"""
The last message in the task Forum is accepted (confirmed).
"""
TASK_FLAG_HAS_PLANNED				= 56
"""
Task has its own planned time.
"""
TASK_FLAG_HAS_PROGRESS				= 59
"""
Task has its own progress value.
"""
TASK_FLAG_IS_REFERENCE				= 61
"""
Task is a reference to the original task.
"""

TASK_PRIORITY_ = ''
"""
.. rubric:: Priority values
"""
TASK_PRIORITY_LOW					= -2
"""
Low prority.
"""
TASK_PRIORITY_BELOW_NORMAL			= -1
"""
Below normal priority.
"""
TASK_PRIORITY_NORMAL					= 0
"""
Nomal priority.
"""
TASK_PRIORITY_ABOVE_NORMAL			= 1
"""
Above normal priority.
"""
TASK_PRIORITY_HIGHT					= 2
"""
High priority.
"""
TASK_PRIORITY_CRITICAL				= 3
"""
Critical priority.
"""

COPY_TASKS_ = ''
"""
.. rubric:: Copy tasks
"""
COPY_TASKS_SUB_TASKS				= 1
"""
Copy sub tasks
"""
COPY_TASKS_TAGS						= 2
"""
Copy tags
"""
COPY_TASKS_ASSIGNED_USERS			= 4
"""
Copy assigned users
"""
COPY_TASKS_EVENTS					= 8
"""
Copy events (by default only definition)
"""
COPY_TASKS_FULL_EVENT_COPY			= 16
"""
Copy all events
"""
COPY_TASKS_ATTACHMENTS				= 32
"""
Copy attachments
"""
COPY_TASKS_INTERNAL_LINKS			= 64
"""
Copy internal links
"""
COPY_TASKS_EXTERNAL_LINKS_OUT		= 128
"""
Copy external links out
"""
COPY_TASKS_EXTERNAL_LINKS_IN		= 256
"""
Copy external links in
"""
COPY_TASKS_PERMISSIONS				= 512
"""
Copy permissions
"""
COPY_TASKS_SUBSCRIBE_USERS_FULL		= 1024
"""
subscribe users with full protocol (may be slow)
"""


TASK_LINK_ = ''
"""
.. rubric:: Task interconnection tuple fields
"""
TASK_LINK_MTM		= 0
"""
Time of connection change.
"""
TASK_LINK_ID 		= 1
"""
Connection ID.
"""
TASK_LINK_DEL 		= 2
"""
If False, the connection is deleted.
"""
TASK_LINK_SRC 		= 3
"""
The task is predecessor.
"""
TASK_LINK_DST 		= 4
"""
The task is follower.
"""
TASK_LINK_FLAGS 	= 5
"""
Connection flags.
"""

TASK_ALLOCATED_ = ''
"""
.. rubric:: Allocated user tuple fields
"""
TASK_ALLOCATED_ID 		= 0
"""
User ID.
"""
TASK_ALLOCATED_NAME 	= 1
"""
User full name.
"""
TASK_ALLOCATED_FLAGS 	= 2
"""
User flags.
"""


MESSAGE_DATA_ = ''
"""
.. rubric:: Message tuple fields
"""
MESSAGE_DATA_MTM                	= 0
"""
Time of data modification.
"""
MESSAGE_DATA_ID                 	= 1
"""
Message ID.
"""
MESSAGE_DATA_PID                	= 2
"""
Parent message ID.
"""
MESSAGE_DATA_TYPE               	= 3
"""
Message Type.
"""
MESSAGE_DATA_CREATOR_NAME       	= 4
"""
Message author's name.
"""
MESSAGE_DATA_CREATED            	= 5
"""
Time of message creation.
"""
MESSAGE_DATA_WORK_TIME          	= 6
"""
Working time to sign off, minutes.
"""
MESSAGE_DATA_TEXT               	= 7
"""
Message text in HTML format.
"""
MESSAGE_DATA_APPROVED_TIME      	= 8
"""
Confirmed signed off time, minutes.
"""
MESSAGE_DATA_FLAGS              	= 9
"""
Message flags.
"""
MESSAGE_DATA_MODERATOR_NAME			= 10
"""
Message editor's name.
"""
MESSAGE_DATA_TID                	= 11
"""
ID of the task, the message belongs to.
"""
MESSAGE_DATA_XMTM               	= 12
"""
Real time of data modification.
"""
MESSAGE_DATA_CREATOR_ID         	= 13
"""
Message author's ID.
"""
MESSAGE_DATA_MODERATOR_ID       	= 14
"""
Messgae editor's ID.
"""
MESSAGE_DATA_STATUS_ID      	= 15
"""
Status ID.
"""

MESSAGE_TYPE_ = ''
"""
.. rubric:: Message types
"""
MESSAGE_TYPE_DEFINITION         =0
"""
Message type -- Definition.
"""
MESSAGE_TYPE_REVIEW             =1
"""
Message type -- Review.
"""
MESSAGE_TYPE_REPORT             =2
"""
Message type -- Report.
"""
MESSAGE_TYPE_NOTE               =3
"""
Message type -- Note.
"""
MESSAGE_TYPE_CLIENT_REVIEW		=4
"""
Message type -- Client Review.
"""
MESSAGE_TYPE_RESOURCE_REPORT	=5
"""
Message type -- Resource Report.
"""
MESSAGE_TYPE_STATUS_CHANGES	=6
"""
Message of change of the status of the task.
"""


MESSAGE_FLAG_ = ''
"""
.. rubric:: Message flags
"""
MESSAGE_FLAG_CLIENT_VISIBLE 		= 0
"""
Message is visible for clients.
"""
MESSAGE_FLAG_APPROVED       		= 1
"""
Report is accepted (confirmed).
"""

ATTACHMENT_DATA_ = ''
"""
.. rubric:: Attachment tuple fields
"""
ATTACHMENT_DATA_MTM                	= 0
"""
Time of data modification.
"""
ATTACHMENT_DATA_EVENT_ID          	= 1
"""
Message ID.
"""
ATTACHMENT_DATA_DEL                	= 2
"""
If not equal to 0, the attacment is deleted.
"""
ATTACHMENT_DATA_GROUP_ID               	= 3
"""
Attachment ID.
"""
ATTACHMENT_DATA_CREATED        	= 4
"""
Time of creation.
"""
ATTACHMENT_DATA_HASH            	= 5
"""
File hash sum.
"""
ATTACHMENT_DATA_TAG          		= 6
"""
Type of file attached.
"""
ATTACHMENT_DATA_FILE_SIZE               	= 7
"""
File size, bytes.
"""
ATTACHMENT_DATA_FILE_NAME      	= 8
"""
File name of the attached file.
"""
ATTACHMENT_DATA_COMMENT         	= 9
"""
Comment to the file.
"""
ATTACHMENT_DATA_ID						= 10
"""
ID of the file attached.
"""

ATTACHMENT_TAG_ = ''
"""
.. rubric:: Attachments tags
"""
ATTACHMENT_TAG_FILE = 0
"""
Attachment entry type -- file.
"""
ATTACHMENT_TAG_THUMB1 = 1
"""
Attachment entry type -- first frame or still image thumbnail 
"""
ATTACHMENT_TAG_THUMB2 = 2
"""
Attachment entry type -- middle frame thumbnail.
"""
ATTACHMENT_TAG_THUMB3 = 3
"""
Attachment entry type -- last frame thumbnail.
"""
ATTACHMENT_TAG_REVIEW = 4
"""
Attachment entry type -- review file
"""
ATTACHMENT_TAG_LINK = 5
"""
Attachment entry type -- link to file
"""


USER_DATA_ = ''
"""
.. rubric:: User tuple field
"""
USER_DATA_ID		=	0
"""
User ID.
"""
USER_DATA_FULL_NAME	=	1
"""
User full name.
"""
USER_DATA_FLAGS			=	2
"""
User flags.
"""
USER_DATA_LOGIN			=	3
"""
User login.
"""
USER_DATA_FIRST_NAME	=	4
"""
User's first name.
"""
USER_DATA_LAST_NAME	=	5
"""
User's last name.
"""
USER_DATA_EMAIL			=	6
"""
User's e-mail.
"""
USER_DATA_PHONE			=	7
"""
User's phone number.
"""
USER_DATA_ICQ				=	8
"""
User's ICQ/Skype ID.
"""

USER_FLAG_ = ''
"""
.. rubric:: User flags
"""
USER_FLAG_IS_RESOURCE = 1
"""
Is a material resource.
"""

ACTIVITY_DATA_ = ''
"""
.. rubric:: Activity tuple fields
"""
ACTIVITY_DATA_ID			=	0
"""
Activity ID.
"""
ACTIVITY_DATA_NAME		=	1
"""
Activity name.
"""
ACTIVITY_DATA_COLOR	=	2
"""
Activity color. RGB format is presented as an integer.
"""

STATUS_DATA_ = ''
"""
.. rubric:: Status tuple field
"""
STATUS_DATA_ID					=	0
"""
Status ID.
"""
STATUS_DATA_NAME			=	1
"""
Status name.
"""
STATUS_DATA_FLAGS			=	2
"""
Status flags.
"""
STATUS_DATA_ORDER			=	3
"""
Status order number.
"""
STATUS_DATA_DESCRIPTION	=	4
"""
Status description.
"""
STATUS_DATA_ICON				=	5
"""
Status icon. XPM format.
"""
STATUS_DATA_COLOR			=	6
"""
Status color. RGB format is presented as an integer.
"""
STATUS_DATA_UNID				=	7
"""
Universe ID.
"""
STATUS_DATA_PERM_LEAVE	=	8
"""
Permissions to leave status.
"""
STATUS_DATA_PERM_ENTER	=	9
"""
Permissions to enter status.
"""

STATUS_FLAG_ = ''
"""
.. rubric:: Status flags
"""
STATUS_FLAG_INHERITABLE = 1
"""
Status is inherited.
"""
STATUS_FLAG_WORK_STARTED = 2
"""
Type status, meaning that the task is in progress.
"""
STATUS_FLAG_WORK_STOPPED = 3
"""
Type status, meaning that the task was stopped.
If :py:const:'STATUS_FLAG_WORK_STARTED <py_cerebro.dbtypes.STATUS_FLAG_WORK_STARTED>` and :py:const:'STATUS_FLAG_WORK_STOPPED <py_cerebro.dbtypes.STATUS_FLAG_WORK_STOPPED>` flags are reseted,
then the type of status will mean that the task is suspended.
"""

TAG_DATA_ = ''
"""
.. rubric:: Tag tuple field
"""
TAG_DATA_MTM    = 0
"""
Time of data change.
"""
TAG_DATA_ID			=	1
"""
Tag ID.
"""
TAG_DATA_PROJECT_ID		=	2
"""
Project ID.
"""
TAG_DATA_NAME		=	3
"""
Tag name.
"""
TAG_DATA_TYPE		=	4
"""
Tag type.
"""

TAG_TYPE_ = ''
"""
.. rubric:: Типы тегов
"""
TAG_TYPE_INTEGER         =0
"""
Integer.
"""
TAG_TYPE_ENUM         =1
"""
Enumeration.
"""
TAG_TYPE_FLOAT         =2
"""
Floating-point number.
"""
TAG_TYPE_STRING         =3
"""
String.
"""
TAG_TYPE_MULTI_ENUM    =4
"""
Multiple enumeration. A tag of this type may contain several enumerations.
"""

TAG_ENUM_DATA_ = ''
"""
.. rubric:: Enumeration Tuple Fields of a Tag
"""
TAG_ENUM_DATA_MTM   		= 0
"""
Data change time.
"""
TAG_ENUM_DATA_ID			=	1
"""
Tag’s enumeration ID.
"""
TAG_ENUM_DATA_TAG_ID		=	2
"""
Tag ID.
"""
TAG_ENUM_DATA_NAME		=	3
"""
Enumeration name.
"""

TASK_TAG_DATA_ = ''
"""
.. rubric:: Tuple Fields of Tag Values
"""
TASK_TAG_DATA_TASK_ID   		= 0
"""
Task ID.
"""
TASK_TAG_DATA_TAG_ID			=	1
"""
Tag ID.
"""
TASK_TAG_DATA_TYPE		=	2
"""
Tag type.
"""
TASK_TAG_DATA_NAME		=	3
"""
Tag name.
"""
TASK_TAG_DATA_VALUE		=	4
"""
Tag value. Type - string. In case of multiple enumerations, the latter are separated by semicolons.
"""

TASK_TAG_ENUM_ = ''
"""
.. rubric:: Tuple fields of tag enumerations set on task
"""
TASK_TAG_ENUM_MTM   		= 0
"""
Data change time.
"""
TASK_TAG_ENUM_ID			=	1
"""
Enumeration ID.
"""
TASK_TAG_ENUM_NAME		=	2
"""
Enumeration name.
"""





