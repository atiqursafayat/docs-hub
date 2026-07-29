# Spec changeset — Extension auto-fill "Học AppSheet"

Read this file before exporting changeset JSON to the extension (Step 4 = YES). The content below is the engine's original specification — adhere to it strictly.

## Output (MUST follow exactly)

Return ONLY a single JSON object. No markdown fences, no prose, no comments. Shape:

```
{
  "changes": [
    {
      "op": "set_column" | "add_view" | "set_view" | "add_action" | "set_action" | "add_format_rule" | "set_format_rule",
      "table": "ExistingTableName (for a view = its 'For this data'; for an action = the table it applies to)",
      "view": "ExistingViewName (set_view only)",
      "viewType": "calendar|deck|table|gallery|detail|map|chart|dashboard|form|onboarding|card",
      "position": "view: left most|left|center|right|right most|menu|ref — action: Primary|Prominent|Inline|Hide",
      "groupAggregate": "NONE|COUNT|SUM :: colName|AVERAGE :: colName|MIN :: colName|MAX :: colName",
      "action": "ExistingActionName (set_action only)",
      "rule": "ExistingFormatRuleName (set_format_rule only)",
      "actionType": "SET_COLUMN_VALUE|EDIT_RECORD|DELETE_RECORD|ADD_RECORD|ADD_RECORD_TO|COPY_EDIT_ROW|REF_ACTION|NAVIGATE_APP|NAVIGATE_URL|OPEN_FILE|CALL|SMS|EMAIL|COMPOSITE",
      "assignments": [ { "column": "existing_col", "value": "AppSheet expression" } ],
      "referencedTable": "REF_ACTION only — table whose action will run",
      "referencedAction": "REF_ACTION only — name of an EXISTING action on referencedTable",
      "referencedRows": "REF_ACTION only — expression returning the rows to act on, e.g. SELECT(Child[id], condition)",
      "actions": [ "ExistingActionName1", "ExistingActionName2" ],
      "target": "NAVIGATE_APP: LINKTOVIEW(\"ViewName\") or LINKTOROW(...) ; NAVIGATE_URL: a URL expression",
      "targetTable": "ADD_RECORD_TO only — the table the new row is added to",
      "columns": [ "col_to_format", "__action__ActionName" ],
      "highlightColor": "red|orange|yellow|green|cyan|blue|purple|pink|themeMainColor|#RRGGBB",
      "textColor": "same options as highlightColor",
      "bold": "true|false", "italic": "true|false", "underline": "true|false", "uppercase": "true|false", "strikethrough": "true|false",
      "imageSize": "Large|Medium|Small|Tiny|Text",
      "condition": "AppSheet expression (action 'Only if this condition is true')",
      "needsConfirmation": "true | false",
      "confirmationMessage": "text or expression",
      "icon": "FontAwesome icon name WITHOUT prefix, e.g. shopping-cart, truck, warehouse, file-invoice, calendar, user, check (view & action only)",
      "column": "existing_column_name",
      "name": "new view or action name (used by add_view / add_action only — NOT for columns)",
      "type": "Text|Number|Decimal|Ref|Enum|EnumList|Date|DateTime|Yes/No|Price|Percent|...",
      "appFormula": "AppSheet expression",
      "initialValue": "AppSheet expression",
      "suggestedValues": "AppSheet expression",
      "validIf": "AppSheet expression",
      "displayName": "AppSheet expression or text",
      "showIf": "true | false | expression",
      "editableIf": "true | false | expression",
      "requireIf": "true | false | expression",
      "resetIf": "true | false | expression"
    }
  ]
}
```

## Rules

- on `set_column` requires `table` and `column` (an EXISTING column). Optional: appFormula, initialValue, suggestedValues, validIf, displayName, showIf, editableIf, requireIf, resetIf.
- DO NOT use virtual columns. NEVER emit op `add_virtual_column` and never create computed/virtual columns. For ANY computed value or formula, set the App formula on an EXISTING real column via op `set_column` (that column must already exist in the schema). If a suitable column does not exist, use set_column on the closest existing column or omit it — do NOT invent a virtual column.
- on `add_view` creates a UX view; requires `table`, `name`, `viewType`. Optional: position, groupAggregate, showIf, displayName, icon.
- on `set_view` edits an existing view; requires `view` (its current name). Optional: table, viewType, position, groupAggregate, showIf, displayName, icon.
- View ops support ONLY those fields — Sort by / Group by columns are NOT supported yet, do not emit them. For a view, `showIf` is its Show-if formula and `displayName` is the view's Display name.
- on `add_action` creates a Behavior action; requires `table`, `name`, `actionType`. Optional: position (Primary|Prominent|Inline|Hide), displayName, icon, condition, needsConfirmation, confirmationMessage, and for actionType SET_COLUMN_VALUE or ADD_RECORD_TO an `assignments` array of {column, value}. For ADD_RECORD_TO also set `targetTable` (the table receiving the new row); its assignments set the NEW row's columns (columns of targetTable), and [_THISROW] refers to the source row.
- on `set_action` edits an existing action; requires `action` (its current name) and usually `table`. Optional: same fields as add_action.
- actionType `REF_ACTION` ("Data: execute an action on a set of rows") REQUIRES `referencedTable` + `referencedAction` (an EXISTING action on that table). `referencedRows` is the row-set expression (optional). Set referencedTable BEFORE referencedAction.
- actionType `COMPOSITE` ("Grouped: execute a sequence of actions") REQUIRES `actions`: an ordered array of EXISTING action names on the SAME table. Create the child actions first (earlier in the changes list), then the COMPOSITE that lists them.
- FIXING ERRORS: If the user reports a problem in an EXISTING column/view/action (e.g. a broken Valid If, App formula, Show-if, or action condition), diagnose the cause and return a corrective changeset using set_column / set_view / set_action that overwrites the broken field with a corrected expression. The user may paste the current (broken) expression and the error text — read them, then output ONLY the fixed JSON. Use the App schema/context (table names, column names, types, Enum values) to keep expressions valid; never invent names.
- on `add_format_rule` creates a UX Format Rule; requires `table` (For this data) + `name`. Optional: condition (If this condition is true), columns (array of column names and/or `__action__ActionName`), icon, highlightColor (background), textColor, bold/italic/underline/uppercase/strikethrough (true/false), imageSize. Colors accept a named theme color (red, green, themeMainColor, …) or a #hex value.
- on `set_format_rule` edits an existing Format Rule; requires `rule` (its current name). Optional: same fields as add_format_rule (`table` only helps locate the rule; `name` renames it).
- `icon` (view, action & format rule): a FontAwesome Solid icon NAME only, no "fa"/"fas"/"fa-" prefix (e.g. "shopping-cart", "truck", "warehouse"). Always pick a fitting icon when creating a view or action. If an action or view is HIDDEN (action position "Hide", or a view not shown in the app), set its `icon` to "minus".
- Action ops: `condition` is the "Only if this condition is true" formula; `assignments` applies ONLY to SET_COLUMN_VALUE. For actionType NAVIGATE_APP set `target` to LINKTOVIEW("ViewName") (or LINKTOROW(...)); for NAVIGATE_URL set `target` to the URL expression. CALL/SMS/EMAIL/OPEN_FILE targets are not supported yet — do not emit them.
- Use ONLY table and column names that appear in the app schema. NEVER invent names. If a needed name is missing, return {"changes": []}.
- Expression fields are raw AppSheet expressions with [Column] refs. Do NOT start them with "=".
- Switch fields (showIf/editableIf/requireIf/resetIf) must be the string "true", "false", or a boolean expression string.
- TEXT LITERALS: a literal text value (NOT an expression) must be wrapped in double quotes, because AppSheet parses / - * + ( ) , < > = and spaces around them as operators. Example: a Display name "Tên vật tư / thiết bị" — keep the quotes; without them AppSheet reads / as division, - as minus, * as multiply, () as grouping. Apply this to displayName, confirmationMessage, fixed text values, suggested/Enum value labels, and any literal string used inside an expression (e.g. [trang_thai] = "Đã xong"). Do NOT quote real expressions, functions, or [column] references.
- A new view/action `name` should be concise and not start with an underscore.
- Only include the fields the user actually asked to set; omit empty fields.
- LIST EXPRESSIONS: whenever an expression uses SELECT(...) (or any list-returning function) and the order matters, wrap it with SORT() so results come back ordered — e.g. SORT(SELECT(Orders[id], [status]="Đã xác nhận"), TRUE). Default to wrapping SELECT in SORT(...) unless the user explicitly says order does not matter. Keep the existing condition/columns unchanged inside.

## AppSheet Expression Language — Key Rules

### Basic syntax
- Reference columns using square brackets: `[ColumnName]`
- Current context: `[_THIS]` (current column) `[_THISROW]` (current line) `[_THISROW_BEFORE]` (value before modification)
- Strings using double quotation marks: `"Hello"`; Boolean: `TRUE`, `FALSE`
- Comparisons of equality use a single symbol. `=` (Not `==`); otherwise it is `<>`
- Logic: `AND(a, b)`, `OR(a, b)`, `NOT(x)` — Do not use `&&`/`||`
- Condition: `IF(cond, then, else)`; multiple branches: `IFS(c1, v1, c2, v2, ...)`, `SWITCH(expr, case1, v1, ..., default)`

### Commonly used functions
- Text: `CONCATENATE`, `LEFT`, `RIGHT`, `MID`, `LEN`, `UPPER`, `LOWER`, `SUBSTITUTE`, `TEXT(value, format)`, `FIND`, `TRIM`, `CONTAINS`
- Number: `ABS`, `ROUND`, `ROUNDDOWN/UP`, `INT`, `MOD`, `MIN`, `MAX`, `SUM(list)`, `AVERAGE(list)`, `COUNT(list)`
- Date and time: `TODAY()`, `NOW()`, `DATE`, `TIME`, `HOUR`, `DAY`, `MONTH`, `YEAR`, `WEEKDAY`, `WORKDAY`, `EOMONTH`
- List/Table: `SELECT(Table[Col], filter [, distinct])`, `FILTER("Table", filter)`, `LOOKUP(value, "Table", "MatchCol", "ReturnCol")`, `ANY`, `TOP`, `INDEX`, `IN`, `CONTAINS`, `ORDERBY`, `SPLIT`, `LIST`
- User: `USEREMAIL()`, `USERNAME()`, `USERROLE()`, `USERSETTINGS("KeyName")`, `CONTEXT("View")`, `CONTEXT("ViewType")`, `CONTEXT("Host")`
- Check: `ISBLANK`, `ISNOTBLANK`, `ISNUMBER`
- Deref qua ref: `[Customer].[Email]`; related list: `REF_ROWS("ChildTable", "ParentRefColumn")`
- Navigation: `LINKTOROW(key, "View")`, `LINKTOFORM("View", "Col1", v1, ...)`, `LINKTOFILTEREDVIEW("View", filter)`, `LINKTOVIEW("View")`

### Data selection pattern
- All lines: `Table[KeyCol]`
- Filter values: `SELECT(Orders[ID], [Status] = "Open")`
- One value: `ANY(SELECT(...))` or `LOOKUP(...)`
- Counting / Adding: `COUNT(SELECT(...))`, `SUM(SELECT(Orders[Total], [Customer] = [_THISROW].[ID]))`

### Mistakes to avoid
- Do not use SQL syntax (WHERE, JOIN, GROUP BY).
- Do not use `==`, `&&`, `||` JS/Excel type
- Do not enclose column names in quotation marks — column names used `[ngoặc vuông]`
- Contains a substring: `CONTAINS([col], "x")`, do not use LIKE
- Column names are case-sensitive; function names are not.

### Official reference source
- Standard documentation: https://support.google.com/appsheet/ — adhere strictly to the function names, function signatures, and behaviors in the documentation; do not invent functions/column types/options that are not in the documentation.
- Anything that is uncertain or not stated here: clearly state that it is uncertain and direct the user to the corresponding Help page; do not guess.
