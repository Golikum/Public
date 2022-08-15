<h1 align="center">Аналитика маркетинговой активности</h>
<h3 align="center">На базе Power BI и Битрикс24</h> 
<br><br>

# #
[Отчёт в Power BI](https://app.powerbi.com/view?r=eyJrIjoiY2MwNzY5ZDQtMDFiNi00NmZlLWFlNzItNzY0MzAxZmFiZTNiIiwidCI6IjA1ZjZlMTJjLWFlYmMtNDFjMi05ZDliLTRmOTJlMzg3NzUxMCIsImMiOjl9)
<br><br>

## Техническое решение

Данные вытягиваются из портала Битрикс24 через коннектор в json-формате и обрабатываются в Power Query.

Используются такие таблицы:

- Activities – Список маркетинговых активностей по ID
- ActivitiesTitles – Названия маркетинговых активностей
- CALENDAR – Таблица-календарь (создаётся в DAX)
- Companies - Компании
- Contacts - Контакты
- Deals – Сделки
- Stages – Стадии сделки

Строится модель взаимосвязей.

Затем производится формирование дополнительных столбцов и мер в DAX.

После этого формируются визуализации.


### Операции в Power Query


Ниже приведены скрипты PowerQuery

«Получить данные» - функция, которая обращается к серверу-источнику, содержит адрес и секретный токен. Здесь не приведена. 


#### Activities
~~~
let
    Source = Contacts_from_source,
    #"Expanded Column1.json" = Table.ExpandRecordColumn(Source, "Column1.json", {"UF_CRM_1614686194"}, {"Column1.json.UF_CRM_1614686194"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Column1.json", each [Column1.json.UF_CRM_1614686194] <> false),
    #"Expanded Column1.json.UF_CRM_1614686194" = Table.ExpandListColumn(#"Filtered Rows", "Column1.json.UF_CRM_1614686194"),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded Column1.json.UF_CRM_1614686194", each ([Column1.json.UF_CRM_1614686194] <> null)),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows1",{{"Column1.json.UF_CRM_1614686194", "ActivityID"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"ActivityID", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"Title", "Create_date"})
in
    #"Removed Columns"
~~~

#### ActivitiesTitles


```
{% raw %}
let
    Source = Json.Document(Web.Contents(веб-хук, вытягивающий с портала названия активностей)),
    result = Source[result],
    result1 = result{0},
    LIST = result1[LIST],
    #"Converted to Table" = Table.FromList(LIST, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"ID", "VALUE"}, {"Column1.ID", "Column1.VALUE"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Column1",{{"Column1.ID", Int64.Type}, {"Column1.VALUE", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Column1.ID", "ActivityID"}, {"Column1.VALUE", "Title_original"}})
in
    #"Renamed Columns"
{% endraw %}
```


#### Companies 
~~~
let
    Source = ПолучитьДанные ("companies"),
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"id", "title", "create_date", "json"}, {"Column1.id", "Column1.title", "Column1.create_date", "Column1.json"}),
    #"Expanded Column1.json" = Table.ExpandRecordColumn(#"Expanded Column1", "Column1.json", {"Канал (Мероприятие откуда пришел) (UF_CRM_1614686194)"}, {"Column1.json.Канал (Мероприятие откуда пришел) (UF_CRM_1614686194)"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Column1.json",{{"Column1.id", "CompanyID"}, {"Column1.title", "CompanyName"}, {"Column1.create_date", "CompanyCreateDate"}, {"Column1.json.Канал (Мероприятие откуда пришел) (UF_CRM_1614686194)", "Activity"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"CompanyID", Int64.Type}, {"CompanyName", type text}, {"CompanyCreateDate", type date}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type",{{"CompanyName", "CompanyName_original"}})
in
    #"Renamed Columns1"
~~~

#### Contacts 
~~~
let
    Source = Contacts_from_source,
    #"Expanded Column1.json" = Table.ExpandRecordColumn(Source, "Column1.json", {"COMPANY_ID"}, {"Column1.json.COMPANY_ID"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Column1.json",{{"Column1.json.COMPANY_ID", "CompanyID"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"CompanyID", Int64.Type}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type",{{"Title", "Title_original"}})
in
    #"Renamed Columns1"
~~~

#### Deals
~~~
let
    Source = ПолучитьДанные ("deals"),
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"sum", "create_date", "id", "json"}, {"Column1.sum", "Column1.create_date", "Column1.id", "Column1.json"}),
    #"Expanded Column1.json" = Table.ExpandRecordColumn(#"Expanded Column1", "Column1.json", {"TITLE", "STAGE_ID", "COMPANY_ID", "CONTACT_ID"}, {"Column1.json.TITLE", "Column1.json.STAGE_ID", "Column1.json.COMPANY_ID", "Column1.json.CONTACT_ID"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Column1.json",{{"Column1.sum", "Sum"}, {"Column1.create_date", "Create_date"}, {"Column1.id", "DealID"}, {"Column1.json.TITLE", "Title"}, {"Column1.json.COMPANY_ID", "CompanyID"}, {"Column1.json.CONTACT_ID", "ContactID"}, {"Column1.json.STAGE_ID", "StageID"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Sum", Int64.Type}, {"DealID", Int64.Type}, {"CompanyID", Int64.Type}, {"ContactID", Int64.Type}, {"Create_date", type date}, {"Title", type text}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Changed Type",{"DealID", "Sum", "Create_date", "Title", "CompanyID", "ContactID"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Reordered Columns",{{"StageID", type text}}),
    #"Renamed Columns1" = Table.RenameColumns(#"Changed Type1",{{"Title", "Title_original"}})
in
    #"Renamed Columns1"
~~~

#### Stages
~~~
let
    Source = ПолучитьДанные ("stages"),
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"name", "status_id", "stage_type"}, {"Column1.name", "Column1.status_id", "Column1.stage_type"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Column1",{{"Column1.name", "Name"}, {"Column1.status_id", "StageID"}, {"Column1.stage_type", "Stage_type"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Name", type text}, {"StageID", type text}, {"Stage_type", type text}})
in
    #"Changed Type"
~~~

#### Contacts_from_source (промежуточная таблица)
~~~
let
    Client = ПолучитьДанные("contacts"),
    #"Converted to Table" = Table.FromList(Client, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"id", "title", "create_date", "json"}, {"Column1.id", "Column1.title", "Column1.create_date", "Column1.json"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Column1",{{"Column1.id", "ContactID"}, {"Column1.title", "Title"}, {"Column1.create_date", "Create_date"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"ContactID", Int64.Type}, {"Title", type text}, {"Create_date", type date}})
in
    #"Changed Type"
~~~
