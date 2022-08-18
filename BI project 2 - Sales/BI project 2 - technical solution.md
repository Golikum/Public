<h1 align="center">План-фактный анализ продаж</h>
<h3 align="center">На базе Power BI и Битрикс24</h> 
<br><br>

# #
[Отчёт в Power BI](https://app.powerbi.com/view?r=eyJrIjoiMWIxNmIzN2EtNmI3NS00YmM4LWEzZDAtMDliOThjZjY2MTRlIiwidCI6IjA1ZjZlMTJjLWFlYmMtNDFjMi05ZDliLTRmOTJlMzg3NzUxMCIsImMiOjl9)
<br><br>

## Техническое решение

Данные вытягиваются из портала Битрикс24 через коннектор в json-формате и обрабатываются в Power Query.  
Часть данных подтягивается через веб-хуки.

Используются такие таблицы:
- Меры
- Виды мероприятий
- Календарь (создаётся в DAX)
- Направления сделок
- Оплаты по сделкам
- План продаж
- Пользователи
- Сделки
- Стадии сделок

Строится модель взаимосвязей.

Затем производится формирование дополнительных столбцов и мер в DAX.

После этого формируются визуализации.

### Модель данных

![Модель данных](https://github.com/Golikum/Public/blob/3187eca81acc5b993c17e5f3a796d5b45787d4d8/BI%20project%202%20-%20Sales/%D0%9A%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%202%20%D1%81%D1%85%D0%B5%D0%BC%D0%B0%20%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D1%81%D0%B2%D1%8F%D0%B7%D0%B5%D0%B9.jpg?raw=true)


### Меры в DAX

~~~
Выполнение плана = DIVIDE(SUM('Сделки'[sum]), SUM('План продаж'[План сумма]))

Максимальное значение датчик продаж = MAX('Сделки'[Продаж, руб.],('Меры'[План итого])*2)

План итого = SUM('План продаж'[План сумма])
~~~


### Операции в Power Query


Ниже приведены скрипты PowerQuery

«Получить данные» - функция, которая обращается к серверу-источнику, содержит адрес и секретный токен. Здесь не приведена. 

[{% raw %}]: #

#### Виды мероприятий
~~~
let
    Источник = Json.Document(Web.Contents("Веб-хук для получения данных из Битрикс24")),
    #"Преобразовано в таблицу" = Table.FromRecords({Источник}),
    #"Развернутый элемент result" = Table.ExpandListColumn(#"Преобразовано в таблицу", "result"),
    #"Развернутый элемент result1" = Table.ExpandRecordColumn(#"Развернутый элемент result", "result", {"ID", "ENTITY_ID", "FIELD_NAME", "USER_TYPE_ID", "XML_ID", "SORT", "MULTIPLE", "MANDATORY", "SHOW_FILTER", "SHOW_IN_LIST", "EDIT_IN_LIST", "IS_SEARCHABLE", "SETTINGS", "LIST"}, {"result.ID", "result.ENTITY_ID", "result.FIELD_NAME", "result.USER_TYPE_ID", "result.XML_ID", "result.SORT", "result.MULTIPLE", "result.MANDATORY", "result.SHOW_FILTER", "result.SHOW_IN_LIST", "result.EDIT_IN_LIST", "result.IS_SEARCHABLE", "result.SETTINGS", "result.LIST"}),
    #"Развернутый элемент result.SETTINGS" = Table.ExpandRecordColumn(#"Развернутый элемент result1", "result.SETTINGS", {"DISPLAY", "LIST_HEIGHT", "CAPTION_NO_VALUE", "SHOW_NO_VALUE"}, {"result.SETTINGS.DISPLAY", "result.SETTINGS.LIST_HEIGHT", "result.SETTINGS.CAPTION_NO_VALUE", "result.SETTINGS.SHOW_NO_VALUE"}),
    #"Развернутый элемент result.LIST" = Table.ExpandListColumn(#"Развернутый элемент result.SETTINGS", "result.LIST"),
    #"Развернутый элемент result.LIST1" = Table.ExpandRecordColumn(#"Развернутый элемент result.LIST", "result.LIST", {"ID", "SORT", "VALUE", "DEF"}, {"result.LIST.ID", "result.LIST.SORT", "result.LIST.VALUE", "result.LIST.DEF"}),
    #"Развернутый элемент time" = Table.ExpandRecordColumn(#"Развернутый элемент result.LIST1", "time", {"start", "finish", "duration", "processing", "date_start", "date_finish"}, {"time.start", "time.finish", "time.duration", "time.processing", "time.date_start", "time.date_finish"}),
    #"Измененный тип" = Table.TransformColumnTypes(#"Развернутый элемент time",{{"result.ID", Int64.Type}, {"result.ENTITY_ID", type text}, {"result.FIELD_NAME", type text}, {"result.USER_TYPE_ID", type text}, {"result.XML_ID", type text}, {"result.SORT", Int64.Type}, {"result.MULTIPLE", type text}, {"result.MANDATORY", type text}, {"result.SHOW_FILTER", type text}, {"result.SHOW_IN_LIST", type text}, {"result.EDIT_IN_LIST", type text}, {"result.IS_SEARCHABLE", type text}, {"result.SETTINGS.DISPLAY", type text}, {"result.SETTINGS.LIST_HEIGHT", Int64.Type}, {"result.SETTINGS.CAPTION_NO_VALUE", type any}, {"result.SETTINGS.SHOW_NO_VALUE", type text}, {"result.LIST.ID", Int64.Type}, {"result.LIST.SORT", Int64.Type}, {"result.LIST.VALUE", type text}, {"result.LIST.DEF", type text}, {"total", Int64.Type}, {"time.start", type number}, {"time.finish", type number}, {"time.duration", type number}, {"time.processing", type number}, {"time.date_start", type datetimezone}, {"time.date_finish", type datetimezone}}),
    #"Переименованные столбцы" = Table.RenameColumns(#"Измененный тип",{{"result.LIST.VALUE", "Вид мероприятия"}, {"result.LIST.ID", "ID вида мероприятия"}}),
    #"Удаленные столбцы" = Table.RemoveColumns(#"Переименованные столбцы",{"result.ID", "result.ENTITY_ID", "result.FIELD_NAME", "result.USER_TYPE_ID", "result.XML_ID", "result.SORT", "result.MULTIPLE", "result.MANDATORY", "result.SHOW_FILTER", "result.SHOW_IN_LIST", "result.EDIT_IN_LIST", "result.IS_SEARCHABLE", "result.SETTINGS.DISPLAY", "result.SETTINGS.LIST_HEIGHT", "result.SETTINGS.CAPTION_NO_VALUE", "result.SETTINGS.SHOW_NO_VALUE", "result.LIST.DEF", "total", "time.start", "time.finish", "time.duration", "time.processing", "time.date_start", "time.date_finish"}),
    #"Переупорядоченные столбцы" = Table.ReorderColumns(#"Удаленные столбцы",{"ID вида мероприятия", "Вид мероприятия", "result.LIST.SORT"})
in
    #"Переупорядоченные столбцы"
~~~

#### Направления сделок
~~~
let
    categories = ПолучитьДанные("categories"),
    #"Преобразовано в таблицу" = Table.FromList(categories, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Развернутый элемент Column1" = Table.ExpandRecordColumn(#"Преобразовано в таблицу", "Column1", {"id", "name", "category"}, {"id", "name", "category"}),
    #"Измененный тип" = Table.TransformColumnTypes(#"Развернутый элемент Column1",{{"name", type text}, {"category", type text}, {"id", type text}}),
    #"Переименованные столбцы" = Table.RenameColumns(#"Измененный тип",{{"id", "category_id"}, {"name", "Направление"}})
in
    #"Переименованные столбцы"
~~~

#### Оплаты по сделкам
~~~
let
    Источник = ПолучитьДанные("list_49"),
    #"Преобразовано в таблицу" = Table.FromList(Источник, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Развернутый элемент Column1" = Table.ExpandRecordColumn(#"Преобразовано в таблицу", "Column1", {"id", "Название платежа", "Сделка", "Дата", "Сумма", "Статус"}, {"id", "Название платежа", "Сделка", "Дата", "Сумма", "Статус"}),
    #"Развернутый элемент Сделка" = Table.ExpandRecordColumn(#"Развернутый элемент Column1", "Сделка", {"deal"}, {"deal"}),
    #"Извлеченные значения" = Table.TransformColumns(#"Развернутый элемент Сделка", {"deal", each Text.Combine(List.Transform(_, Text.From)), type text}),
    #"Извлеченные значения1" = Table.TransformColumns(#"Извлеченные значения", {"Дата", each Text.Combine(List.Transform(_, Text.From)), type text}),
    #"Извлеченные значения2" = Table.TransformColumns(#"Извлеченные значения1", {"Сумма", each Text.Combine(List.Transform(_, Text.From)), type text}),
    #"Извлеченные значения3" = Table.TransformColumns(#"Извлеченные значения2", {"Статус", each Text.Combine(List.Transform(_, Text.From)), type text}),
    #"Удаленные столбцы" = Table.RemoveColumns(#"Извлеченные значения3",{"Название платежа"}),
    #"Измененный тип" = Table.TransformColumnTypes(#"Удаленные столбцы",{{"id", Int64.Type}, {"deal", Int64.Type}, {"Сумма", Int64.Type}, {"Дата", type date}})
in
    #"Измененный тип"
~~~

#### План продаж
~~~
let
    Источник = ПолучитьДанные("list_47"),
    #"Преобразовано в таблицу" = Table.FromList(Источник, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Развернутый элемент Column1" = Table.ExpandRecordColumn(#"Преобразовано в таблицу", "Column1", {"id", "Название", "Сотрудник", "Сентябрь 2021", "Октябрь 2021", "Ноябрь 2021", "Декабрь 2021", "Январь 2022"}, {"id", "Название", "Сотрудник", "Сентябрь 2021", "Октябрь 2021", "Ноябрь 2021", "Декабрь 2021", "Январь 2022"}),
    #"Добавлен пользовательский объект" = Table.AddColumn(#"Развернутый элемент Column1", "Пользовательский", each Table.ColumnNames(#"Развернутый элемент Column1")),
    #"Переименованные столбцы" = Table.RenameColumns(#"Добавлен пользовательский объект",{{"Пользовательский", "Список записей"}}),
    Пользовательский1 = Table.SelectColumns( #"Переименованные столбцы", {"Список записей"}),
    #"Развернутый элемент Список записей" = List.Distinct(Table.ToList(Table.ExpandListColumn(Пользовательский1, "Список записей"))),
    Пользовательский2 = #"Преобразовано в таблицу",
    #"Развернутый элемент Column2" = Table.ExpandRecordColumn(Пользовательский2, "Column1", #"Развернутый элемент Список записей"),
    #"Развернутый элемент Сотрудник" = Table.ExpandListColumn(#"Развернутый элемент Column2", "Сотрудник"),
    #"Развернутый элемент Сентябрь 2021" = Table.ExpandListColumn(#"Развернутый элемент Сотрудник", "Сентябрь 2021"),
    #"Развернутый элемент Октябрь 2021" = Table.ExpandListColumn(#"Развернутый элемент Сентябрь 2021", "Октябрь 2021"),
    #"Развернутый элемент Ноябрь 2021" = Table.ExpandListColumn(#"Развернутый элемент Октябрь 2021", "Ноябрь 2021"),
    #"Развернутый элемент Декабрь 2021" = Table.ExpandListColumn(#"Развернутый элемент Ноябрь 2021", "Декабрь 2021"),
    #"Развернутый элемент Январь 2022" = Table.ExpandListColumn(#"Развернутый элемент Декабрь 2021", "Январь 2022"),
    #"Переименованные столбцы1" = Table.RenameColumns(#"Развернутый элемент Январь 2022",{{"Сотрудник", "Сотрудник ID"}}),
    #"Удаленные столбцы" = Table.RemoveColumns(#"Переименованные столбцы1",{"id", "Название"}),
    #"Другие столбцы с отмененным свертыванием" = Table.UnpivotOtherColumns(#"Удаленные столбцы", {"Сотрудник ID"}, "Атрибут", "Значение"),
    #"Измененный тип" = Table.TransformColumnTypes(#"Другие столбцы с отмененным свертыванием",{{"Атрибут", type date}, {"Значение", Int64.Type}}),
    #"Переименованные столбцы2" = Table.RenameColumns(#"Измененный тип",{{"Атрибут", "Дата"}, {"Значение", "План сумма"}}),
    #"Измененный тип1" = Table.TransformColumnTypes(#"Переименованные столбцы2",{{"Сотрудник ID", Int64.Type}})
in
    #"Измененный тип1"
~~~

#### Пользователи
~~~
let
    portal_users = ПолучитьДанные("portal_users"),
    #"Преобразовано в таблицу" = Table.FromList(portal_users, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Развернутый элемент Column1" = Table.ExpandRecordColumn(#"Преобразовано в таблицу", "Column1", {"id", "email", "active", "full_name", "json"}, {"id", "email", "active", "full_name", "json"}),
    #"Развернутый элемент json" = Table.ExpandRecordColumn(#"Развернутый элемент Column1", "json", {"PERSONAL_BIRTHDAY", "WORK_COMPANY", "WORK_POSITION", "UF_DEPARTMENT", "USER_TYPE"}, {"PERSONAL_BIRTHDAY", "WORK_COMPANY", "WORK_POSITION", "UF_DEPARTMENT", "USER_TYPE"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Развернутый элемент json",{{"active", type logical}, {"email", type text}, {"full_name", type text}, {"id", type text}}),
    #"Переименованные столбцы" = Table.RenameColumns(#"Changed Type",{{"id", "user_id"}, {"full_name", "Ответственный_original"}})
in
    #"Переименованные столбцы"
~~~

#### Сделки
~~~
let
    deal = ПолучитьДанные("deals"),
    #"Преобразовано в таблицу" = Table.FromList(deal, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Развернутый элемент Column1" = Table.ExpandRecordColumn(#"Преобразовано в таблицу", "Column1", {"sum", "finish_date", "create_date", "id", "responsible_id", "type_id", "stage_id", "json"}, {"sum", "finish_date", "create_date", "id", "responsible_id", "type_id", "stage_id", "json"}),
    #"Развернутый элемент json" = Table.ExpandRecordColumn(#"Развернутый элемент Column1", "json", {"TITLE", "CATEGORY_ID", "STAGE_SEMANTIC_ID", "IS_NEW", "IS_RECURRING", "IS_RETURN_CUSTOMER", "IS_REPEATED_APPROACH", "PROBABILITY", "CURRENCY_ID", "OPPORTUNITY", "COMPANY_ID", "CONTACT_ID", "BEGINDATE", "CLOSEDATE", "OPENED", "CLOSED", "ASSIGNED_BY_ID", "CREATED_BY_ID", "MODIFY_BY_ID", "DATE_CREATE", "DATE_MODIFY", "SOURCE_ID", "LEAD_ID", "ADDITIONAL_INFO", "ORIGINATOR_ID", "UTM_SOURCE", "UTM_MEDIUM", "UTM_CAMPAIGN", "UTM_CONTENT", "UTM_TERM", "UF_CRM_AMO_643349", "UF_CRM_1591777444", "UF_CRM_1637684461", "Дата заезда (UF_CRM_5EDCB71EE602D)", "Дата выезда (UF_CRM_5EDCB71EEFD39)", "COMMENTS"}, {"TITLE", "CATEGORY_ID", "STAGE_SEMANTIC_ID", "IS_NEW", "IS_RECURRING", "IS_RETURN_CUSTOMER", "IS_REPEATED_APPROACH", "PROBABILITY", "CURRENCY_ID", "OPPORTUNITY", "COMPANY_ID", "CONTACT_ID", "BEGINDATE", "CLOSEDATE", "OPENED", "CLOSED", "ASSIGNED_BY_ID", "CREATED_BY_ID", "MODIFY_BY_ID", "DATE_CREATE", "DATE_MODIFY", "SOURCE_ID", "LEAD_ID", "ADDITIONAL_INFO", "ORIGINATOR_ID", "UTM_SOURCE", "UTM_MEDIUM", "UTM_CAMPAIGN", "UTM_CONTENT", "UTM_TERM", "UF_CRM_AMO_643349", "UF_CRM_1591777444", "UF_CRM_1637684461", "Дата заезда (UF_CRM_5EDCB71EE602D)", "Дата выезда (UF_CRM_5EDCB71EEFD39)", "COMMENTS"}),
    #"Переименованные столбцы1" = Table.RenameColumns(#"Развернутый элемент json",{{"UF_CRM_AMO_643349", "Вид мероприятия ID (UF_CRM_AMO_643349)"}, {"UF_CRM_1591777444", "Оплачено фактически (UF_CRM_1591777444)"}, {"UF_CRM_1637684461", "Дата внесения предоплаты (UF_CRM_1637684461)"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Переименованные столбцы1",{{"DATE_MODIFY", type datetimezone}, {"CLOSEDATE", type datetimezone}, {"BEGINDATE", type datetimezone}, {"sum", type number}, {"type_id", type text}, {"create_date", type date}, {"stage_id", type text}, {"COMMENTS", type text}, {"UTM_TERM", type text}, {"UTM_CONTENT", type text}, {"UTM_CAMPAIGN", type text}, {"UTM_MEDIUM", type text}, {"UTM_SOURCE", type text}, {"ORIGINATOR_ID", type text}, {"ADDITIONAL_INFO", type text}, {"SOURCE_ID", type text}, {"DATE_CREATE", type datetimezone}, {"id", type text}, {"finish_date", type date}, {"TITLE", type text}, {"CATEGORY_ID", type text}, {"Дата заезда (UF_CRM_5EDCB71EE602D)", type datetimezone}, {"Дата выезда (UF_CRM_5EDCB71EEFD39)", type datetimezone}}),
    #"Changed Type Date" = Table.TransformColumnTypes(#"Changed Type",{{"DATE_CREATE", type datetime}, {"DATE_MODIFY", type datetime}, {"CLOSEDATE", type datetime}, {"BEGINDATE", type datetime}, {"Дата заезда (UF_CRM_5EDCB71EE602D)", type date}, {"Дата выезда (UF_CRM_5EDCB71EEFD39)", type date}}),
    #"Добавлен пользовательский столбец" = Table.AddColumn(#"Changed Type Date", "Пользовательский", each Text.Combine({Date.ToText([#"Дата заезда (UF_CRM_5EDCB71EE602D)"], "MMMM"), " ", Date.ToText([#"Дата заезда (UF_CRM_5EDCB71EE602D)"], "yyyy")}), type text),
    #"Переименованные столбцы" = Table.RenameColumns(#"Добавлен пользовательский столбец",{{"Пользовательский", "Месяц и год заезда"}}),
    #"Измененный тип" = Table.TransformColumnTypes(#"Переименованные столбцы",{{"Дата внесения предоплаты (UF_CRM_1637684461)", type datetimezone}}),
    #"Извлеченная дата" = Table.TransformColumns(#"Измененный тип",{{"Дата внесения предоплаты (UF_CRM_1637684461)", DateTime.Date, type date}}),
    #"Измененный тип1" = Table.TransformColumnTypes(#"Извлеченная дата",{{"Оплачено фактически (UF_CRM_1591777444)", type number}, {"id", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Измененный тип1",{{"TITLE", "TITLE_original"}})
in
    #"Renamed Columns"
~~~

#### Стадии сделок
~~~
let
    stages = ПолучитьДанные("stages"),
    #"Преобразовано в таблицу" = Table.FromList(stages, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Развернутый элемент Column1" = Table.ExpandRecordColumn(#"Преобразовано в таблицу", "Column1", {"name", "status_id", "entity_id", "sort", "stage_type"}, {"name", "status_id", "entity_id", "sort", "stage_type"}),
    #"Переименованные столбцы" = Table.RenameColumns(#"Развернутый элемент Column1",{{"name", "Стадия"}}),
    #"Измененный тип" = Table.TransformColumnTypes(#"Переименованные столбцы",{{"status_id", type text}, {"entity_id", type text}, {"sort", Int64.Type}, {"stage_type", type text}, {"Стадия", type text}}),
    #"Переименованные столбцы1" = Table.RenameColumns(#"Измененный тип",{{"entity_id", "category"}}),
    #"Replaced Value" = Table.ReplaceValue(#"Переименованные столбцы1","Механика","Проработка",Replacer.ReplaceText,{"Стадия"})
in
    #"Replaced Value"
~~~

[{% endraw %}]: #
