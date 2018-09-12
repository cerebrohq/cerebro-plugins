zstatuses - complex plugin wint events and actions

Actions (action.py):
- Recalculate dates - Start and Finish date of selected task will be recalculated from sub-tasks
Start date will be setted to minimum Start date of sub-tasks
Finish date will be setted to maximum Finish date of sub-tasks

Events (events.py):
- Block status changing from 'statuses_from_blocked' ('Request' in example) to 'statuses_to_blocked' ('Done', 'Ready' in example)
- If new status in 'statuses_to_stop' ('Done', 'Ready', 'Closed' in example) and task progress less than 100% task progress will be setted to 100% and Finish date will be now date.
- If new status in 'statuses_from_reset'('Not required' in example) and task progress is 100% task progress will be reset to 0%.
- If user set status 'status_ready_to_start' value ('Ready to start' in example) in first time, Start date of task will be setted to now date.
- If user that allocated to task post first report to taks, Start date of task will be setted to now date.