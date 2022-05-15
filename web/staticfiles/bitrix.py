import bitrix24
import os
import datetime

class B24:
    def __init__(self):
        self.bx24 = bitrix24.Bitrix24(os.environ.get("BITRIX_TOKEN"))

    def bitrix_check_task(self, id_person):
        try:
            return (self.bx24.callMethod(
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
            return (self.bx24.callMethod('bizproc.workflow.start',
                                       TEMPLATE_ID=14,
                                       DOCUMENT_ID=['lists', 'BizprocDocument', vv],
                                       PARAMETERS={'list': f'{avrora}'}
                                       ))
        except bitrix24.BitrixError as message:
            return message

    def sonet_group_get(self, group_id):
        try:
            return (self.bx24.callMethod(
                "sonet_group.get",
                arFilter={"ID": group_id}
            ))
        except bitrix24.BitrixError as message:
            return message

class Avrora_4(B24):

    def sonet_group_get_all(self):
        try:
            return (self.bx24.callMethod(
                "sonet_group.get"
            ))
        except bitrix24.BitrixError as message:
            return message

    def user_get(self, id_user):
        try:
            return (self.bx24.callMethod(
                "user.get",
                filter={'ID': id_user}
            ))
        except bitrix24.BitrixError as message:
            return message

    def lists_get(self,id_group):
        try:
            return (self.bx24.callMethod(
                "lists.get",
                IBLOCK_TYPE_ID='lists_socnet',
                SOCNET_GROUP_ID=id_group
            ))
        except bitrix24.BitrixError as message:
            return message

    def lists_field_get(self, list_id, group_id):
        try:
            return (self.bx24.callMethod(
                "lists.field.get",
                IBLOCK_TYPE_ID='lists_socnet',
                IBLOCK_ID=list_id,
                SOCNET_GROUP_ID=group_id
            ))
        except bitrix24.BitrixError as message:
            return message
    def deal_get(self,id_deal):
        try:
            return (self.bx24.callMethod(
                "crm.deal.get",
                id=id_deal
            ))
        except bitrix24.BitrixError as message:
            return message

    def list_element_get_group(self, list_id, group_id):
        try:
            return (self.bx24.callMethod(
                "lists.element.get",
                IBLOCK_TYPE_ID='lists_socnet',
                IBLOCK_ID=list_id,
                SOCNET_GROUP_ID=group_id
            ))
        except bitrix24.BitrixError as message:
            return message
    def list_element_get(self, id_list):
        try:
            return (self.bx24.callMethod(
                "lists.element.get",
                IBLOCK_TYPE_ID='lists',
                IBLOCK_ID=id_list,
                ELEMENT_ORDER={'DATE_CREATE': 'asc'}

            ))
        except bitrix24.BitrixError as message:
            return message

    def people_time(self, id_deal):
        global group_id
        name = self.deal_get(id_deal)['TITLE']
        itog = {}
        group = self.sonet_group_get_all()
        for i in group:
            if i['NAME'] == name:
                group_id = i['ID']
        list_id = self.lists_get(group_id)[0]['ID']
        list_info = (self.lists_field_get(list_id=list_id, group_id=group_id))
        month = {}
        for m in list_info:
            if 'PROPERTY_' in m and m!= 'PROPERTY_513':
                month.update({m: list_info[m]['NAME']})

        info = self.list_element_get_group(list_id=list_id, group_id=group_id)
        for l in info:
            id_user = l['CODE'].split("_")[1]
            user_name = self.user_get(id_user)[0]
            user_name_final = user_name['LAST_NAME']+ ' ' + user_name['NAME']+ ' ' +user_name['SECOND_NAME']

            counter = 0
            for s in month:
                a = list(month.keys())[counter]
                counter+=1
                try:
                    if month[s] not in list(itog.keys()):
                        itog.update({month[s]:{user_name_final: list(l[a].values())[0]}})
                    else:
                        itog[month[s]].update({user_name_final: list(l[a].values())[0]})
                except:
                    pass
        return itog

    def posting(self, id_deal):
        itog = {}
        info = self.list_element_get(18)
        for i in info:
            id_d = (list(i['PROPERTY_193'].values()))[0]
            if id_d == str(id_deal):
                data_create =datetime.datetime.strptime(i['DATE_CREATE'], "%d.%m.%Y %H:%M:%S")
                a = list(itog.keys())
                data_final = data_create.strftime("%B%Y")
                if data_final not in a:
                    itog.update({data_final:[f'{list(i["PROPERTY_251"].values())[0]}']})
                else:
                    itog[data_final].append(list(i["PROPERTY_251"].values())[0])

        return itog

    def application(self, id_deal):
        itog= {}
        info = self.list_element_get(37)
        for i in info:
            try:
                id_d = (list(i['PROPERTY_214'].values()))[0]
                if id_d == ('D_'+str(id_deal)):
                    expenditure = (list(i['PROPERTY_245'].values()))[0]
                    data_create = datetime.datetime.strptime(i['DATE_CREATE'], "%d.%m.%Y %H:%M:%S")
                    data_final = data_create.strftime("%B%Y")
                    a = list(itog.keys())

                    if expenditure == '08-01 (БДДС) Билеты для сотрудников ПП' \
                            or expenditure ==' 08-02 (БДДС) Проживание в гостиницах сотрудников ПП' \
                            or expenditure ==' 08-03 (БДДС) Суточные для сотрудников ПП' \
                            or expenditure =='08-08 (БДДС) Прочие расходы в командировке сотрудников ПП':
                        keys = 'posting'
                    elif expenditure == 'СЕБ 03-01 (БДДС) Вознаграждение за услуги производственного назначения по договору ГПХ и самозанятым (без учета НДФЛ)' \
                            or expenditure == 'СЕБ 05-02 (БДДС) Страховые взносы на вознаграждение (ГПХ, самозанятые) по услугам производственного назначения' \
                            or expenditure =='СЕБ 05-02 (БДДС) Страховые взносы на вознаграждение (ГПХ, самозанятые) по услугам производственного назначения' \
                            or expenditure=='СЕБ 14-02 (БДДС) Расходы на подрядчиков производственного характера (услуги сторонних организаций) по проектированию':
                        keys = 'contractor'
                    elif expenditure == '16-01 (БДДС) Представительские расходы производственного назначения':
                        keys = 'hospitality expenses'
                    elif expenditure == '33-01 (БДДС) Агентские расходы':
                        keys = 'agents commission'
                    else:
                        keys = 'other expenses'
                    if data_final not in a:
                        itog.update({data_final: {keys: [f'{list(i["PROPERTY_217"].values())[0]}']}})
                    else:
                        if keys in list(itog[data_final].keys()):
                            itog[data_final][keys].append(list(i["PROPERTY_217"].values())[0])
                        else:
                            itog[''].update(
                                {data_final: {keys: [f'{list(i["PROPERTY_217"].values())[0]}']}})
            except:
                pass

        return itog

    def main(self, id_deal):
        posting = self.posting(id_deal)
        application = self.application(id_deal)
        people_time = self.people_time(id_deal)
        data = {'POSTING':posting,
                'PEOPLE_TIME': people_time,
                'APPLICATION': application
                }
        return data