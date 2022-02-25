import bitrix24
from static.tok import bitrix_token as token



class B24:
    def __init__(self):
        self.token = bitrix24.Bitrix24(token)

    def bitrix_check_task(self, id_person):
        try:
            return (self.token.callMethod(
                "tasks.task.list",
                order={},
                filter={'RESPONSIBLE_ID': id_person},
                params={},
                select={},
            ))
        except bitrix24.BitrixError as message:
            return message

    def bizproc_workflow_start(self,avrora, vv):
        try:
            return (self.token.callMethod('bizproc.workflow.start',
                                       TEMPLATE_ID=14,
                                       DOCUMENT_ID=['lists', 'BizprocDocument', vv],
                                       PARAMETERS={'list': f'{avrora}'}
                                       ))
        except bitrix24.BitrixError as message:
            return message

    def sonet_group_get(self,group_id):
        try:
            return (self.token.callMethod(
                "sonet_group.get",
                arFilter={"ID": group_id}
            ))
        except bitrix24.BitrixError as message:
            return message

    def user_get(self,pk):
        try:
            return (self.token.callMethod(
                "user.get",
                filter={"ID": f"{pk}"}
            ))
        except bitrix24.BitrixError as message:
            return message

    def lists_element_get(self):
        try:
            return (self.token.callMethod(
                "lists.element.get",

            ))
        except bitrix24.BitrixError as message:
            return message