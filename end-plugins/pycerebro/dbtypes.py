# -*- coding: utf-8 -*-


# Поля кортежа данных задачи
TASK_DATA_MTM							= 0					# время модификации данных.
TASK_DATA_ID								= 1				# идентификатор задачи
TASK_DATA_PARENT_ID						= 2				# идентификатор родительской задачи
TASK_DATA_PLANNED_DELTA				= 3				# устаревшее, не используется
TASK_DATA_NAME							= 4				# имя задачи
TASK_DATA_PARENT_URL						= 5			# полный путь до родителькой задачи. Пример: /Test project/Scene 1/
TASK_DATA_ACTIVITY_NAME					= 6			# имя вида деятельности
TASK_DATA_ACTIVITY_ID						= 7			# идентификатор вида деятельности
TASK_DATA_SELF_USERS_DECLARED			= 8		# заявленное время пользователей по задаче в минутах. Тип float
TASK_DATA_SELF_USERS_APPROVED			= 9		# принятое время пользователей по задаче в минутах. Тип float
TASK_DATA_CREATED						= 10				# время создания задачи.
TASK_DATA_PRIORITY						= 11				# приоритет
TASK_DATA_PROGRESS						= 12				# прогресс. Тип float от 0.0 до 100.0
TASK_DATA_PLANNED						= 13				# запланированное время на задачу в часах. Тип float
TASK_DATA_USERS_DECLARED					= 14		# заявленное время пользователей по задаче и её подзадачам в часах. Тип float
TASK_DATA_USERS_APPROVED					= 15		# принятое время пользователей по задаче и её подзадачам в часах. Тип float
TASK_DATA_THUMBS							= 16				# хеши эскизов. Тип string. Разделитель ';'
TASK_DATA_FLAGS							= 17				# флаги задачи
TASK_DATA_MODERATOR_ID					= 18			# идентификатор пользователя, изменившего задачу
TASK_DATA_CREATOR_ID						= 19			# идентификатор автора задачи
TASK_DATA_MODIFIED						= 20				# время изменения задачи.
TASK_DATA_ALLOCATED						= 21			# назначенные пользователи (исполнители) на задачу. Тип string. Разделитель ';'
TASK_DATA_OFFSET							= 22				# рассчитанное время начала задачи в днях от 01.01.2000. Тип float
TASK_DATA_DURATION						= 23				# рассчитанная длительность задачи в днях. Тип float
TASK_DATA_PROJECT_ID						= 24			# идентификатор проекта задачи
TASK_DATA_PRIVILEGE						= 25				# права доступа текущего пользователя к задаче. Тип integer
TASK_DATA_HUMAN_START					= 26			# заданное время начала задачи в днях от 01.01.2000. Тип float
TASK_DATA_HUMAN_FINISH					= 27			# заданное время окончания задачи в днях от 01.01.2000. Тип float
TASK_DATA_SELF_BUDGET						= 28			# бюджет задачи
TASK_DATA_SELF_SPENT						= 29			# затраты (сумма платежи) по задаче
TASK_DATA_BUDGET							= 30				# бюджет задачи с её подзадачами
TASK_DATA_SPENT						= 31					# затраты (сумма платежей) по задаче с её подзадачами
TASK_DATA_RESOURCE_SELF_DECLARED			= 32	# заявленное время материальных ресурсов по задаче в минутах. Тип float
TASK_DATA_RESOURCE_SELF_APPROVED			= 33	# принятое время материальных ресурсов по задаче в минутах. Тип float
TASK_DATA_RESOURCE_DECLARED				= 34		# заявленное время материальных ресурсов по задаче с её подзадачами в часах. Тип float
TASK_DATA_RESOURCE_APPROVED				= 35		# принятое время материальных ресурсов по задаче с её подзадачами в часах. Тип float
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


# Флаги задачи
TASK_FLAG_DELETED					= 0			# задача удалена
TASK_FLAG_PERM_INHERIT_BLOCK			= 1	# у задачи сброшено наследование прав доступа
TASK_FLAG_CLOSED						= 2			# задача закрыта
TASK_FLAG_TASK_AS_EVENT				= 3		# задача помечена как событие
TASK_FLAG_SUSPENED					= 4			# задача остановлена (на паузе)
TASK_FLAG_FORUM_LOCKED				= 5		# форум задачи залочен
TASK_FLAG_CLOSED_EFFECTIVE			= 30		# задача закрыта, поскольку закрыта задача более верхнего уровня
TASK_FLAG_SUSPENED_EFFECTIVE			= 31	# задача остановлена, поскольку остановлена задача более верхнего уровня
TASK_FLAG_HAS_CHILD					= 32			# задача имеет подзадачи
TASK_FLAG_HAS_MESSAGES				= 33		# задача имеет сообщения в форуме
TASK_FLAG_NEED_ANSWER				= 34		# задача требует ответа (в соответствии с правами доступа текущего пользователя)
TASK_FLAG_HAS_SUB_PERMS				= 35
TASK_FLAG_ASSIGNED					= 38			# текуший пользователь является исполнителем на задаче
TASK_FLAG_INTEREST					= 39			# текуший пользователь следит за задачей
TASK_FLAG_LAST_EV_CLIENT_VIS			= 44	# последнее сообщение в задаче видимо для клиентов
TASK_FLAG_LAST_EV_APPROVED			= 45		# последнее сообщение в задаче принято
TASK_FLAG_HAS_PLANNED				= 56			# задача имеет собственное  запланированное время 
TASK_FLAG_HAS_PROGRESS				= 59		# задача имеет собственный прогресс

# Флаги копирования задач
COPY_TASKS_SUB_TASKS				= 1		# копировать подзадачи
COPY_TASKS_TAGS						= 2		# копировать теги
COPY_TASKS_ASSIGNED_USERS			= 4		# копировать назначенных пользователей
COPY_TASKS_EVENTS					= 8		# копировать постановку задачи
COPY_TASKS_FULL_EVENT_COPY			= 16	# копировать остальные сообщения
COPY_TASKS_ATTACHMENTS				= 32	# копировать вложения
COPY_TASKS_INTERNAL_LINKS			= 64	# копировать внутренние связи
COPY_TASKS_EXTERNAL_LINKS_OUT		= 128	# копировать внешние исходящие связи
COPY_TASKS_EXTERNAL_LINKS_IN		= 256	# копировать внешние входящие связи
COPY_TASKS_PERMISSIONS				= 512	# копировать права доступа
COPY_TASKS_SUBSCRIBE_USERS_FULL		= 1024	# копировать подписчиков

# Значения приоритета
TASK_PRIORITY_LOW					= -2			# низкий
TASK_PRIORITY_BELOW_NORMAL			= -1	# ниже нормального
TASK_PRIORITY_NORMAL					= 0		# нормальный
TASK_PRIORITY_ABOVE_NORMAL			= 1		# выше нормального
TASK_PRIORITY_HIGHT					= 2			# высокий
TASK_PRIORITY_CRITICAL				= 3			# критичный


# Поля кортежа данных связи между задачами
TASK_LINK_MTM		= 0 # время модификации связи
TASK_LINK_ID 		= 1 # идентификатор пользователя
TASK_LINK_DEL 		= 2 # если значение этого поля равно False, значит связь удалена
TASK_LINK_SRC 		= 3 # задача от которой идет связь
TASK_LINK_DST 		= 4 # задача к которой идет связь
TASK_LINK_FLAGS 	= 5 # флаги связи

# Поля кортежа данных назначенного пользователя (исполнителя)
TASK_ALLOCATED_ID 		= 0 # идентификатор пользователя
TASK_ALLOCATED_NAME 	= 1 # полное имя пользователя
TASK_ALLOCATED_FLAGS 	= 2 # флаги пользователя


# Поля кортежа данных сообщения
MESSAGE_DATA_MTM                	= 0				#  Время модификации данных
MESSAGE_DATA_ID                 	= 1				# Идентификатор сообщения
MESSAGE_DATA_PID                	= 2				# Идентификатор родительского сообщения
MESSAGE_DATA_TYPE               	= 3				# Тип сообщения
MESSAGE_DATA_CREATOR_NAME       	= 4		# Имя автора собщения
MESSAGE_DATA_CREATED            	= 5			# Время создания сообщения
MESSAGE_DATA_WORK_TIME          	= 6			# Рабочее время в минутах
MESSAGE_DATA_TEXT               	= 7				# Текст сообщения в формате html
MESSAGE_DATA_APPROVED_TIME      	= 8		# Принятое время в минутах
MESSAGE_DATA_FLAGS              	= 9				# Флаги сообщения
MESSAGE_DATA_MODERATOR_NAME			= 10	# Имя пользователя, изменившего сообщение
MESSAGE_DATA_TID                	= 11				# Идентификатор задачи, к которой относится сообщение
MESSAGE_DATA_XMTM               	= 12				# Реальное время модификации данных
MESSAGE_DATA_CREATOR_ID         	= 13			# Идентификатор автора собщения
MESSAGE_DATA_MODERATOR_ID       	= 14		# Идентификатор пользователя, изменившего сообщение
MESSAGE_DATA_STATUS_ID      	= 15
"""
Status ID.
"""


# Типы сообщений
MESSAGE_TYPE_DEFINITION         =0		# Тип сообщения - Постановка задачи
MESSAGE_TYPE_REVIEW             =1			# Тип сообщения - Рецензия
MESSAGE_TYPE_REPORT             =2			# Тип сообщения - Отчет
MESSAGE_TYPE_NOTE               =3			# Тип сообщения - Заметка
MESSAGE_TYPE_CLIENT_REVIEW		=4	# Тип сообщения - Рецензия клиента
MESSAGE_TYPE_RESOURCE_REPORT	=5	# Тип сообщения - Отчет за ресурс
MESSAGE_TYPE_STATUS_CHANGES	=6
"""
Message of change of the status of the task.
"""

# Флаги сообщения
MESSAGE_FLAG_CLIENT_VISIBLE 		= 0	# Сообщение видимо для клиентов
MESSAGE_FLAG_APPROVED       		= 1	# Сообщение принято (Отчет принят)

# Поля кортежа данных вложения
ATTACHMENT_DATA_MTM                	= 0				#  Время модификации данных
ATTACHMENT_DATA_EVENT_ID          	= 1				# Идентификатор сообщения
ATTACHMENT_DATA_DEL                	= 2				#  если значение этого поля не равно 0, значит вложение удалено
ATTACHMENT_DATA_GROUP_ID               	= 3		# Идентификатор вложения
ATTACHMENT_DATA_CREATED        	= 4					# Время создания
ATTACHMENT_DATA_HASH            	= 5					# Хеш файла
ATTACHMENT_DATA_TAG          		= 6					# Тип файла вложения
ATTACHMENT_DATA_FILE_SIZE               	= 7		# Размер файла вложения в байтах
ATTACHMENT_DATA_FILE_NAME      	= 8				# Имя файла вложения
ATTACHMENT_DATA_COMMENT         	= 9				# Комментарий к файлу
ATTACHMENT_DATA_ID						= 10				# Идентификатор файла вложения

ATTACHMENT_TAG_FILE = 0			# Тип записи вложения - файл
ATTACHMENT_TAG_THUMB1 = 1		# Тип записи вложения - эскиз первого кадра или эскиз изображения, если вложение 
ATTACHMENT_TAG_THUMB2 = 2		# Тип записи вложения - эскиз среднего кадра
ATTACHMENT_TAG_THUMB3 = 3		# Тип записи вложения - эскиз последнего кадра
ATTACHMENT_TAG_REVIEW = 4		# Тип записи вложения - файл рецензии
ATTACHMENT_TAG_LINK = 5			# Тип записи вложения - линк на файл


# Поля кортежа данных пользователя
USER_DATA_ID		=	0	# идентификатор пользователя
USER_DATA_FULL_NAME	=	1	# полное имя пользователя
USER_DATA_FLAGS			=	2	# флаги пользователя
USER_DATA_LOGIN			=	3	# логин пользователя
USER_DATA_FIRST_NAME	=	4	# имя пользователя
USER_DATA_LAST_NAME	=	5	# фамилия пользователя
USER_DATA_EMAIL			=	6	# e-mail пользователя
USER_DATA_PHONE			=	7	# телефон пользователя
USER_DATA_ICQ				=	8	# ICQ/Skype пользователя

# Флаги пользователя
USER_FLAG_IS_RESOURCE = 1	# является материльным ресурсом

# Поля кортежа данных вида деятельности
ACTIVITY_DATA_ID			=	0	# идентификатор вида деятельности
ACTIVITY_DATA_NAME		=	1	# имя вида деятельности
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






