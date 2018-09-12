pstatuses Plugin

Changing statuses for linked tasks with rules:
- Selected task status changed to 'compose_status_to' value ('paused' in example)
- Selected task Parent contain 'compose_name' value ('Compose' in example)
- Task has income linked
- Linked task Parent contain 'render_name' value ('Render' in example)

If all is OK, Linked task status will be automatically changed to 'render_status_to' value ('could be better' in example)

Example tasks structure:

Root task
	|
	-> Render Parent
		|
		-> Render Task 1	--->
	|							|
	-> Compose Parent			|	Link
		|						|
		-> Compose Task 1	<---
		
If 'Compose Task 1' status will be changed to 'paused', 'Render Task 1' status will be automatically chaned to 'could be better'