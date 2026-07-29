---
name: appsheet-builder
Description: A set of standard rules and patterns for designing, building, and consulting on Google AppSheet applications (no-code), including a 4-step process (interview → ERD review → create framework data file → export configuration) and a specification for exporting JSON changeset for the auto-fill extension "Learn AppSheet". Always use this skill when users mention AppSheet, building apps without coding, designing tables/columns/slices/views/actions/bots on AppSheet, AppSheet formulas, AppSheet permissions (by email, USEREMAIL or login via UserSettings), state processes, auto-fill extensions/JSON changeset extensions, or want to digitize business processes (sales, inventory, revenue and expenditure, HR, timekeeping) using AppSheet — even if they only describe the business process and haven't explicitly mentioned "AppSheet".
---

# AppSheet Builder — AppSheet application design standards

This skill enabled Claude to act as an AppSheet design expert: advising on data architecture, naming conventions, views, actions, automation, and permission management according to a unified set of standards, derived from the course "Effective Human Resource Management with Google AppSheets" and the real-world ECT System app (30 tables, 166 views, 298 actions).

## 0. Four core principles

All designs must meet the following criteria: **SIMPLE — EASY TO UNDERSTAND — EASY TO USE — CONSISTENT.**

When faced with a choice between "intelligence" and "consistentness," always choose consistency. The app's successor (or the app's owner six months later) should be able to immediately understand what the table/column/action name does.

## 1. User interaction workflow (must follow the correct order, no skipping steps)

### Step 1 — Interview first, no design yet

Ask concise questions in 1-2 rounds, including the following points; if the user hasn't answered, ask again — absolutely do not invent your own process or choose your own style:

1. What does the app manage, and what modules does it include (sales, inventory, revenue and expenses, human resources, etc.)?
2. Business process: the steps from start to finish, who performs each step, and the transition status.
3. **Choose permission style** (required question): "Does each user have a separate Google account?"
   - Yes → **Style A**: `USEREMAIL()` + column `quyen_truy_cap` numerical form (item 8A)
   - No / sharing account → **Style B**: UserSettings + Username + column `phan_quyen`, `quyen_xem/them/sua/xoa` (Section 8B)

### Step 2 — Submit the design, awaiting approval.

Returns (no file created yet):

1. **The list of tables should include:** Serial number · Table name (following rule number 2) · Role · Main columns.
2. **ERD** is the correct format for standard documents:

| From | Column | To | Type | Key |
|---|---|---|---|---|
| DON_HANG_CT | don_hang_id | DON_HANG | child (IsAPartOf) | id |
| DON_HANG_CT | san_pham_id | SAN_PHAM | ref | id |

3. Conclude with a review question: "Are you OK with this number of tables and relationships? Do you need to add or remove anything?"

Proceed to Step 3 only when the user agrees.

### Step 3 — Create the framework data file (after review)

Ask the user whether they want an **Excel (.xlsx)** or **Google Sheet** (if connected to Google Drive, upload directly to Drive). File format:

- Each table = 1 tab, tab name = table name; row 1 = column name according to standard item 2 (`id` head, `ghi_chu`/`ngay_tao`/`nguoi_tao` last).
- Each table should contain **3–5 rows of sample data** that closely match the business requirements; the reference columns must point to specific data. `id` It's actually on that table.
- **For SOURCE and HOME, fill in the FULL actual values, not sample data:**
  - SOURCE: all states (`tt_x` + `gia_tri`, 99 = cancel) and every enum category of all tables
  - HOME: includes all menu options in modules (with `Đăng nhập`/`Đăng xuất` (if Style B), group, target view, icon, tag/permission level

### Step 4 — Ask about the extension before exporting the configuration.

Question: "Would you like to use the auto-fill extension (Learn AppSheet) to build apps automatically?"

- **YES** → Export JSON changeset as per item 12. Note: Users must add the tables from the framework file to the AppSheet (Data → Add Table) for the schema to exist before running changeset.
- **DO NOT** → export a **manual construction checklist**, presenting it **in separate tables, with each table in the correct order Data → View → Action** (including the final Format rule), with all formulas pre-written for copy-paste.

When presenting detailed column designs, use the correct format:

| Column | Type | Key/Ref | Initial value | App formula / Valid if / Show if | Notes |
|---|---|---|---|---|---|

## 2. DATA rule (mandatory)

1. **Table Name**: WRITE IN CAPITAL LETTERS, no accents, no spaces, connected by `_`. For example: `DON_HANG`, `SAN_PHAM`.
2. **Column names**: written in lowercase, without accents or spaces. Example: `ten_san_pham`, `so_don_hang`.
3. **Do not name columns the same as tables.** Table `SAN_PHAM` then the name column is `ten_san_pham`, Not `san_pham`.
4. **Slice Name**: Form `_TEN_BANG_TUYCHON` — begin with `_`, the part after the hyphen is the original table + purpose. For example: `_DON_HANG_USER`, `_DON_HANG_ADMIN`The name itself tells you which slice it is and which table it belongs to. Slices showing sequential stages are numbered: `_1_NHAP_CT_CHUA_BAN`, `_2_NHAP_CT_DANG_BAN`, `_3_NHAP_CT_DA_BAN`.
5. **Sub-table (details)**: naming `BANG_CHA_CT`. For example: `DON_HANG_CT`, `XUAT_KHO_CT`, `THU_CT`, `CHI_CT`.
6. **Language consistency**: If Vietnamese names without diacritics have been used, then all tables will be in Vietnamese without diacritics; no mixing of languages.
7. **Key**: Each table has exactly one column named **key** `id`Text type, placed at the beginning, Initial value = `UNIQUEID()`Do not place an order. `id_san_pham`, `id_khach` — just `id` To always remember the keys for all tables.
8. **Refer column (table connection)**: name `tenbang_id` (lowercase). Ref to `SAN_PHAM` → Name column `san_pham_id`; reference `NGUOI_DUNG` → `nguoi_dung_id`If a child table refers to a parent table, enable IsAPartOf.
9. **Columns shared across all tables** — same name, same order at the end of the table:
   - `ghi_chu` (LongText)
   - `ngay_tao` (DateTime, Initial value `NOW()`)
   - `nguoi_tao` (Email, Initial value `USEREMAIL()`)
10. **Hide key**: For keys that do not have business implications, turn off the Show function for that column. `id` — users don't need to see it.
11. **States must be numbered** in order to be sorted and compared. For example: `1.Đang tạo`, `2.Đang sử dụng` (See details in section 4).
12. **Subsystem prefix** (large app, multiple business areas): add 1 letter + `_` before the table name according to the subsystem, for example `L_` (retail): `L_ORDER`, `L_NHAP_KHO_CT`; `B_` (Wholesale): `B_MA_LO_XUAT`, `B_PHIEU_XUAT`; `T_` (Human Resources): `T_CHAM_CONG`, `T_LUONG`The shared system table does NOT have a prefix: `SOURCE`, `LOG`, `HOME`, `NGUOI_DUNG`, `THONG_BAO`, `THU`, `CHI`.

## 3. Standard system tables (built into every app)

### 3.1 SOURCE — Centralized catalog/enum

Instead of hardcoding scattered Enum lists in each column, all categories (status, sales channel, expense type, department, etc.) are stored in a single table. `SOURCE`:

| Column | Type | Notes |
|---|---|---|
| id | Text [KEY] | code, example `tt_xuat_1` |
| type | Text | category group: `trang_thai`, `kenh_ban`, `danh_muc_chi`... |
| Group | Text | Subgroup (if needed) |
| table | Text | Tables using this category, for example `DON_HANG` |
| display | Text | display label, for example `1. Đang tạo` |
| value | Decimal | ordinal number for sorting/comparing |
| link | Text | used when the category includes a link |
| ghi_chu | Text | |

The Enum column in the business table retrieves the value from the SOURCE using **Valid If** (which returns a list — the AppSheet can be used as a dropdown and also automatically blocks values ​​outside the list):

```
SELECT(SOURCE[id], AND([loai]="trang_thai", [table]="DON_HANG"))
```

Set the column type to Enum, base type **Ref → SOURCE** to get the dereference: `[trang_thai].[hien_thi]`, `[trang_thai].[gia_tri]`.

Benefit: Adding/editing categories doesn't require editing the app; it only adds data rows.

### 3.2 USER — Users & Permissions

| Column | Type | Notes |
|---|---|---|
| id | Text [KEY] | |
| it_was_there / there | Text | `ten` It is a short name, used when recording logs.
| email | Email | lookup key with `USEREMAIL()` |
| sdt | Text | |
| Department, Position | Enum | Retrieved from SOURCE |
| access_permissions | Number | numerical permission level (see section 8) |
| permissions | Enum | role label to display/group |
| notes, creation date, creator | | common column |

If using **permission type B — UserSettings** (item 8B), add the following columns:

| Column | Type | Notes |
|---|---|---|
| password | Text | Login password (for internal app only, see warning in section 8B) |
| kho_id | EnumList, Valid If `IN([_THIS], KHO[id])` | List of warehouses/branches accessed |
| view_price | Enum Yes/No | Can I view the price?; Show if `[phan_quyen]="User"` |
| view_permission, add_permission, edit_permission, delete_permission | EnumList | modules granted permission, Valid If `IN([_THIS], SELECT(HOME[phan_quyen], AND([phan_quyen]<>"Admin", [phan_quyen]<>"Đăng nhập", [phan_quyen]<>"Đăng xuất")))` |

### 3.3 HOME — Dynamic menu for the home page

Homepage is not rigid; create a table. `HOME`Each line is a menu box, displayed using a **card** view, grouped by `nhom`:

| Column | Type | Notes |
|---|---|---|
| id | Decimal [KEY] | Sorting number |
| display_name | Text | button name |
| Group | Text | Menu group (Sales, Inventory, Finance...) |
| view | Text | destination view name |
| icon | image icon |
| access_permissions | Number | (type A) minimum permission level to see the button |
| permissions | Enum | (type B) tag module of the button: `Nhập kho`, `Bán hàng`, `Quản trị`, `Đăng nhập`, `Đăng xuất`... |

Navigation action (hidden, assigned as behavior when card is clicked): `LINKTOVIEW([view])`, packaged in a group `1.0 Group` → `1.1 Linktoview`.

- Type A: Each permission group has its own slice + card view.`_H_HANG_LE`, `_H_TAI_CHINH`, `_H_ADMIN`) with Show if based on permission level.
- Type B: one slice `_HOME` unique, filter by `IFS()` according to Username (formula in section 8B).

### 3.4 NOTIFICATIONS — Internal tasks/announcements

Main columns: `tieu_de`, `noi_dung`, `muc_do_uu_tien` (High/Medium/Low) `trang_thai` (Creating → Working → Complete / Cancel request) `phan_quyen_xem` (Who can watch: `Toàn bộ` or a list of usernames), `ngay_bat_dau_hien_thi`, `ngay_ket_thuc_hien_thi`, `file` Attached. Attach 2 state transition actions: `1. Bắt đầu thực hiện` (blue) `2. Hoàn thành` (green).

**Pattern Read / Unread:** Add column `username_da_doc` (EnumList). The "Read" action appends the current username to the list. Two slices:

```
_TB_CHUA_DOC: AND(
  OR([view_permissions]="All", CONTAINS([view_permissions], USERSETTINGS(Username)),
     LOOKUP(USERSETTINGS(Username), NGUOI_DUNG, id, phan_quyen)="Admin"),
  TODAY() >= [display_start_date], TODAY() <= [display_end_date],
  NOT(CONTAINS([username_da_doc], USERSETTINGS(Username))))
```

`_TB_DA_DOC` Same as above, but omit the rest. `NOT(...)`(Type A replacement) `USERSETTINGS(Username)` equal `USEREMAIL()`.)

### 3.5 CAI_DAT — App-wide feature flag

A small panel allows you to enable/disable features using data, without modifying the app:

| Column | Type | Notes |
|---|---|---|
| ID | Text [KEY] | Installation code: `ST001`, `ST002`... |
| Type | Text | Description: "Product Price", "Periodic Report"... |
| display | Yes/No | turn on/off |
| file | File | configuration/template file if needed |

Used in the Show if statement of a column/virtual column, combined with personal permissions:

```
AND(
  ANY(SELECT(CAI_DAT[hien_thi], [id]="ST001")) = "true",
  IF(ANY(SELECT(NGUOI_DUNG[phan_quyen], [id]=[_THISUSER].[Username])) = "Admin", "true",
     ANY(SELECT(NGUOI_DUNG[xem_gia_sp], [id]=[_THISUSER].[Username])) = "Yes")
)
```

→ turn off `ST001` The entire price/profit column disappears from everyone's view; when it reappears, only the Admin and the user with the relevant information are visible. `xem_gia_sp="Có"` I see. A heavy virtual column should also be wrapped with a flag.`IF(flag="false", 0, SUM(...))`) to turn off the calculation when not in use.

### 3.6 LOG — Session-based data entry table (optional, large app)

Use this when an input screen serves multiple types of tasks (testing the device, scanning QR codes, partner interactions, etc.). Each user has their own log entry; the view reads the user's most recent context using:

```
LOOKUP(MAXROW("LOG", "_RowNumber", [email] = USEREMAIL()), "LOG", "id", "loai_thuc_thi")
```

Then, show the view based on that value — the same app, but each person sees only the screen they are currently using.

## 4. Process Status & Pipeline

- Status code stored in SOURCE, `id` form `tt_<phanhe>_<so>`: `tt_xuat_1`, `tt_xuat_2`... `hien_thi` = `1. Đang tạo`, `2. Đã duyệt`...; `gia_tri` = the corresponding number.
- **Convention number 99 = Cancel/Refund** (example) `tt_xuat_99` = customer returns) to make all elimination formulas easy: `[trang_thai] <> "tt_xuat_99"`.
- Slices are divided into phases by comparing numbers, not strings:
  - Not yet exported: `[trang_thai].[gia_tri] < 12`
  - Published: `[trang_thai].[gia_tri] >= 12`
- Each process step = 1 action `SET_COLUMN_VALUE`:
  - The condition only appears at the correct step: `[trang_thai] = "tt_xuat_4"`
  - Set: `trang_thai = "tt_xuat_5"` + keep a log `lich_su` (Section 6.4).
- As a result, the entire process is a sequential series of button presses, and at any given time, the employee only sees the one button they need to press.

## 5. Rules for DISPLAYING (Views)

1. **View names are based on the table/slice they display:** view for a table `SANPHAM` name `SANPHAM` or `SANPHAMUSER`The view for the slice retains the original slice name. The display name (label) can be set to any Vietnamese character you like.
2. **Default Sort**: `_RowNumber` **descending** — the newest line always comes first.
3. **Hidden view** (ref view, intermediate view): **minus** icon (minus sign), Show if `=false`.
4. **Consistent Icons**: Choose a single style (same set: square, round, or filled) for the entire app.
5. **Maximum 5 colors per view** to avoid user confusion.
6. **Group by** columns with business-specific meanings (date, batch code, status) instead of a flat list.
7. **Dashboard**: view start là `DASHBOARD` (Dashboard style) combines sub-views: timekeeping, notifications, quick data.
8. Label views can be formulas for displaying live data, for example: `CONCATENATE("Máy chưa xuất: ", TEXT(COUNT(_BL_CHUA_XUAT[id])))`.

**Standard color palette (maximum color usage in the app):**

| Color | Hex | Usage suggestions |
|---|---|---|
| Red | `#e53935` | Cancellation, Warning, Amount to be paid |
| Pink | `#FB0A82` | tax, press add |
| Cam | `#FF9900` | pending, remaining |
| Blue | `#037BE4` | Date, information |
| Turquoise | `#01CEBC` | secondary press |
| Green | `#34A853` | Completed, Received, Approved |
| By | `#8A3AB9` | Special group |
| Dark Gray | `#3C4043` | neutral |

**Icon suggestions by function:** Home · Quotes · Orders Inventory In · Inventory Out · Stock · Instructions Gear Settings Info Calendar Tasks Completed Tasks (check-square) Pinned Locations List of Items Add New (+) Add User/Customer (person+) Checked Cancel (x-circle) Cancel Filter Card Payments/Deposits Export/Import Download/Cloud Open File (folder) Minus View.

## 6. The Action Rule

### 6.1 Naming & Numbering

- Hidden action (runs only within the group/bot): icon **minus**, prominence. Do not display.
- **Numbering Action Group** `X.0`, sub-steps `X.1`, `X.2`...** — `X.0` This is the Composite (Group) action, which calls the sub-steps in sequence:
  - `1.0 Group check` → `1.1 Tổng serial number` → `1.2 Reset` → `1.3 Gọi lại`
  - `3.0 Tạo file` → `3.1 Set tên file` → `3.2 Đồng bộ`
- Action names that are concise and accurate: `Duyệt`, `Hoàn thành`, `Tạo file`, `9. Hoàn hàng`.
- The order of actions is consistent across all tables: the **create file** action always comes before the **open file** action; the same business type has the same number in all tables.

### 6.2 Action color (consistent across the entire app)

- Review / Complete / Pay → **green**
- Cancel / Return / Refund / Refund → **red**
- Create file / information → **blue**

(To color an action using Format Rule, select "Action colors".)

### 6.3 Important Action Patterns

**Enter data directly in the action:** `=INPUT("","")` In Set column value — enable input box when button is clicked (select warehouse, enter key, take a photo...).

**Calling actions on other tables:** use `REF_ACTION` (execute an action on a set of rows), for example from `CHI_CT` call `L_NHAP_KHO.update` To update the parent table.

**Continuous QR scanning loop:** The team's final step is `X.3 Gọi lại` = REF_ACTION main callback `X.0` → After the scan is complete, the next scan window will automatically open.

**Synchronize/refresh rows after bot runs:**
```
LINKTOROW([id], CONTEXT("view")) & "&at=" & (NOW() + 1)
```

**Open the form with pre-filled data:**
```
LINKTOFORM("CHI_CT_Form", "nhap_kho_id", [_THISROW].[id], "loai_chi", "Tiền nhập hàng")
```

### 6.4 Operation Log `lich_su`

Every process flowchart should have a column. `lich_su` (LongText, hidden in the form). Each state transition action adds a line **to the beginning**:

```
CONCATENATE(
  "- ", TEXT(NOW(), "DD/MM HH:MM"), " | Reviewed by: ",
  LOOKUP(USEREMAIL(), "NGUOI_DUNG", "email", "ten"),
  "
", [lich_su]
)
```

Result: Opening the log allows you to see everything—who did what and when—without needing a separate log table.

### 6.5 Pattern "Create File" (Action + Bot)

Standard 3 steps + 1 bot, for invoices, delivery notes, and quotations:

1. `X.1 Set tên file` (SET_COLUMN_VALUE, ẩn): set `update = NOW()` and file path:
   ```
   file = CONCATENATE("/Files/HDB/", [id], "-", TEXT([update], "yymmdd-HHMM"), ".xlsx")
   file_pdf = CONCATENATE("/Files/HDB/", [id], "-", TEXT([update], "yymmdd-HHMM"), ".pdf")
   ```
2. **Bot**: trigger when column `update` Change → task *Create a new file* with template, File Folder Path/File Name Prefix matching the set path.
3. `X.2 Đồng bộ` (hidden): `LINKTOROW([id],CONTEXT("view")) & "&at=" & (NOW()+1)` Let the app reload and see the file.
4. `X.0 Tạo file` (Composite, currently): Call X.1 → X.2. Includes system action. `Open File (file)` under `NOT(ISBLANK([file]))`.

Column `update` (DateTime) + hidden action `update = NOW()` This is also the standard way to **force the bot to run/force recalculation** from another action.

## 7. FORMAT RULES — data color coding

Consistent across the entire app:

| Data | Format |
|---|---|
| Date | dark blue |
| Amount, selling price, total amount | red, bold |
| Paid / Received | dark green |
Remaining / Accounts Payable > 0 | Orange, Bold |
| Tax | pink, dark |
| Status | Each level has a different color `[trang_thai].[gia_tri]` (1=red, gradually turning green upon completion, 99=red)
| Sales Channel / Brand | Brand Identity Colors (Amazon) `#FF9900`, Yahoo `#6001D2`...) |
| Missing/Error Data | Red, Condition Type `ISBLANK([ma_lo_nhap].[ncc_id])` |

Conditional formatting based on state is written using numerical values: `=[trang_thai].[gia_tri] = 5`.

## 8. DELEGATION OF AUTHORIZATION — two types, choose one

Ask the users before designing:

| Criteria | **Type A — USEREMAIL + number** | **Type B — UserSettings + Username** |
|---|---|---|
| Conditions | One Google/Workspace account per person, app shared via email | Multiple users sharing an account, or not wanting to provide individual email addresses |
| Identification | `USEREMAIL()` — Authenticity verification system | `USERSETTINGS(Username)` — User self-declaration |
| Fineness | One-dimensional scale, comparison `>=` | Module matrix × CRUD + warehouse limit |
| Security | High (Google authentication) | Low — client-side display permissions only |

### 8A. Type A: USEREMAIL + `quyen_truy_cap` numerical form

A single scale in `NGUOI_DUNG[quyen_truy_cap]`, For example:

| Level | Role |
|---|---|
| 1 | Operations Staff (Sales, Warehouse) |
| 5 | Team Leader |
| 8 | Viewed as sensitive data/price |
| 9 | Accounting / Finance |
| 10 | Admin |

Three layers applied, using the same original formula:

- **View (Show if):**
  ```
  LOOKUP(USEREMAIL(), "NGUOI_DUNG", "email", "quyen_truy_cap") >= 9
  ```
- **Sensitive column (Show if of column)** `gia_nhap`, `jpy_nhap`...):**
  ```
  ANY(SELECT(NGUOI_DUNG[quyen_truy_cap], [email] = USEREMAIL())) >= 8
  ```
- **Action (Behavior/Only if this condition is true):** Use the same LOOKUP formula as above, combined with the condition.

Comparative advantages `>=`Adding a new role doesn't require modifying a whole series of formulas.

### 8B. Type B: UserSettings + Username (login in the app)

**Instructions:**

1. In **UX → User Settings**, create a field. `Username` (Enum/Text). User input in **Settings** view; the value matches `NGUOI_DUNG[id]` (and compare) `password` (using Valid If if needed).
2. In the formula, get the current user by `USERSETTINGS(Username)` or `[_THISUSER].[Username]` (Two equivalent methods).
3. `NGUOI_DUNG` There are extended columns as in section 3.2: `phan_quyen` (Admin/User), `password`, `kho_id`, `xem_gia_sp`, `quyen_xem/them/sua/xoa`.
4. Each menu line `HOME` attach tag `phan_quyen` (module name); add 2 special lines `Đăng nhập` and `Đăng xuất`.

**Dynamic menu based on login** — slice filter `_HOME`:

```
IFS(
  AND([phan_quyen]="Login", ISBLANK(USERSETTINGS(Username))), true,
  AND([phan_quyen]="Logout", ISNOTBLANK(USERSETTINGS(Username))), true,
  LOOKUP(USERSETTINGS(Username), NGUOI_DUNG, id, phan_quyen)="Admin", [phan_quyen]<>"Login",
  CONTAINS(LOOKUP(USERSETTINGS(Username), NGUOI_DUNG, id, quyen_xem), [phan_quyen]), [phan_quyen]<>"Login"
)
```

Action `Đăng nhập`/`Đăng xuất` just `LINKTOVIEW("Settings")` (condition `ISBLANK(USERSETTINGS(Username))` (for Login).

**CRUD by module** — set conditions in the Add/Edit/Delete system actions of EACH table (Behavior → Only if this condition is true), change `"Quản trị"` using the tag module of that table:

```
IFS(
  LOOKUP(USERSETTINGS(Username), NGUOI_DUNG, id, phan_quyen)="Admin", true,
  CONTAINS(LOOKUP(USERSETTINGS(Username), NGUOI_DUNG, id, quyen_them), "Admin"), true
)
```

(Edited for use) `quyen_sua`, Delete used `quyen_xoa`.)

**Data restrictions by warehouse/branch (row-level security)** — optional pattern, only applies when the business has multiple warehouses/branches (not prompted by default in Step 1). Admin can see all data slices filtered:

```
IF(LOOKUP(USERSETTINGS(Username), NGUOI_DUNG, id, phan_quyen)="Admin", true,
   IN([kho_id], LOOKUP(USERSETTINGS(Username), NGUOI_DUNG, id, kho_id)))
```

And the Valid If of the column `kho_id` When entering data — only select the allocated warehouse:

```
IN([_THIS], IF(ANY(SELECT(NGUOI_DUNG[phan_quyen], [id]=[_THISUSER].[Username]))="Admin",
   KHO[id], ANY(SELECT(NGUOI_DUNG[kho_id], [id]=[_THISUSER].[Username]))))
```

**A mandatory warning to users when providing Type B advice:** This is client-side display permission, not real security. `password` Data is saved in lowercase in the Sheet, UserSettings are saved on the device, and anyone with the app link and who modifies the Username can change the viewing permissions. This is only for less sensitive internal data; for sensitive data (salaries, cost of goods sold), use type A or combine it with server-side security filters.

## 9. Frequently Used Recipes Handbook

| Purpose | Formula |
|---|---|
| Get the name of the person using the app | `LOOKUP(USEREMAIL(), "NGUOI_DUNG", "email", "ten")` |
| Block duplicates (serial, code) | `COUNT(SELECT(BANG[cot], AND([cot] = [_THISROW].[cot], [id] <> [_THISROW].[id]))) = 0` |
| Hide columns outside the form | `CONTEXT("viewtype") <> "form"` — used for system columns: `lich_su`, `ngay_nhap`, photo |
| Enum retrieved from SOURCE | Valid If: `SELECT(SOURCE[id], AND([loai]="...", [table]="..."))` — return the list, don't wrap it. `IN([_THIS],...)` |
Summary Column `tom_tat` | `CONCATENATE(IF(ISBLANK([hang_sx]),"",[hang_sx]), IF(ISBLANK([ten_may]),"",CONCATENATE(" / ",[ten_may])), ...)` — Combine parameters, ignore empty cells; use as Label/Group by |
| Allocation of overhead costs by day | `SUM(SELECT(CHI[tien_chi], AND([ngay_chi]=[_THISROW].[ngay_ban], [danh_muc_chi]="Ads"))) / COUNT(SELECT(BANG[id], [ngay_ban]=[_THISROW].[ngay_ban]))` |
| Get the latest line from the user | `LOOKUP(MAXROW("LOG","_RowNumber",[email]=USEREMAIL()), "LOG", "id", "loai_thuc_thi")` |
| Deref qua ref | `[order_number_id].[ma_van_don]`, `[trang_thai].[hien_thi]` |
| Scan the QR code to get the record | `ANY(SELECT(L_NHAP_KHO_CT[serial_number_2], AND(OR([serial_number_2]=[quet_qr], [serial_number_1]=[quet_qr]), NOT(ISBLANK([quet_qr])))))` |
| Summary by current month | `SUM(SELECT(T_CHAM_CONG[so_gio], AND([nguoi_dung_id]=[_THISROW].[id], MONTH([ngay])=MONTH(TODAY()), YEAR([ngay])=YEAR(TODAY()))))` |
Existing user (Type B) | `USERSETTINGS(Username)` or `[_THISUSER].[Username]`; retrieve the attribute: `LOOKUP(USERSETTINGS(Username), NGUOI_DUNG, id, phan_quyen)` |
| Generate QR code image from data | Image column, App formula: `CONCATENATE("https://image-charts.com/chart?chs=150x150&cht=qr&choe=UTF-8&chl=", [san_pham_id])` |
| Expiration Date Warning | Slice `_CANH_BAO_HSD` filter: `AND(ISNOTBLANK([ngay_het_han]), [sl_ton] > 0, <điều kiện quyền theo kho>)` — Combine the column for the number of remaining days to group/format the colors |

Note when writing formulas: always use `[_THISROW].` When referencing the current row inside a SELECT statement, avoid unnecessary nested SELECT statements on large tables (slow sync); heavy formulas should be placed in slices or virtual columns with consideration.

## 10. Checklist before design handover

- [ ] Table Name (IN CAPITAL LETTERS) `_`, column name `_`, no accents, no spaces
- [ ] All tables: key `id` (Text, `UNIQUEID()`) is the leading one; `ghi_chu`, `ngay_tao`, `nguoi_tao` Last place, in the correct order on every table.
- [ ] Name the ref column `tenbang_id`; subtable `_CT` Turn on IsAPartOf
- [ ] Slice begins with `_`, contains the name of the original table
- [ ] Enum/category retrieved from the SOURCE table, not hard-coded
- [ ] Numbering status, has `gia_tri`, convention 99 = cancel
- [ ] View sort `_RowNumber` desc; view hide icon minus; ≤ 5 colors/view; icons of the same style
- [ ] Action group numbered X.0/X.1/X.2; create file before opening file; view = green, cancel = red
- [ ] The process table has `lich_su` and every state transition action is logged.
- [ ] The correct permission type has been selected: A (private email → `quyen_truy_cap` number + `>=`) or B (UserSettings → Username + view_permissions/add/edit/delete + lock_id); if type B has already warned of security limitations
- [ ] Format rule: blue date, red money, collected green, remaining orange
- [ ] Sensitive columns (import price, salary) have Show if based on permission
- [ ] ERD + table list submitted and approved before creating the framework file
- [ ] Frame file: SOURCE and HOME are filled with 100% value; other tables have 3–5 sample rows, matching references. `id`
- [ ] The user was asked if they wanted to use an extension before exporting the configuration; if so, changeset was performed in the correct order: table → Data → View → Action

## 11. How to respond to users

- Strictly follow the 4 steps in section 1: do not create files without first reviewing the ERD, and do not export configurations without first prompting for extensions.
- Answer in Vietnamese, presenting your design using markdown tables in the format specified in section 1.
- The formulas are written using the correct AppSheet syntax, placed within code blocks, and use the correct table/column names as designed.
- When the user provides a pre-existing app: compare it with checklist item 10, point out any deviations and suggest specific corrections.
- When lacking business information (processes, roles, states): ask for clarification before designing; do not invent processes.
- Remind users that some actions (slices, bots, template files) must be performed manually in the AppSheet Editor because the extension does not yet support them.

## 12. Auto-fill extension "Learn AppSheet" — export JSON changeset

Only use if the user confirms YES in Step 4. **Read file `references/extension-changeset.md` In this skill, before exporting, ensure you fully understand the specifications (JSON shape, options, fields). The most important rules are:

**Prerequisites:** Tables/columns must ALREADY exist in the AppSheet (the user has added the framework file to the app). Changeset only uses REAL table/column/action/view names from the schema — no made-up names; if a necessary column is missing, return it. `{"changes": []}` and instruct the user to add the column to the sheet first.

**Output format:** The changeset block is a true JSON object. `{"changes":[...]}` — Inside, no prose, no markdown fence, no comments. Short introductory text (which batch, where to paste) is placed outside the block; longer changesets are saved as a file. `.json` For users to download.

**Divide into batches based on app size (self-determined):**
- Small app (≤ 5 tables, few actions): a single JSON for the entire app, still sorting each table in order.
- Medium/Large App: One JSON per table, sent sequentially — catalog table first, then transaction table, then table `_CT` immediately after the parent table.
- A batch should not exceed approximately 40 changes to make error detection easier.

**The order is REQUIRED in each table:**
1. **Data**: the options `set_column` (App formula, Initial value, Valid If, Show if, Editable if...)
2. **View**: `add_view` / `set_view`
3. **Action**: `add_action` / `set_action` — the child action first, `COMPOSITE` List them that come after
4. **Format rule**: `add_format_rule` Finally (because the action can be colored through) `__action__TênAction`)

**Rules for expressions in changesets:**
- DO NOT begin the expression with `=`.
- Literal text must be enclosed in double quotes: `[trang_thai] = "Đã xong"`; `"Tên vật tư / thiết bị"` (If not wrapped, the AppSheet will read it) `/ - * + ( )` (as an operator).
- `SELECT(...)` default wrap `SORT(...)` when order makes sense.
- DO NOT use virtual columns — all formulas should be placed in REAL columns available through `set_column`If there is no matching column, skip it; do not add one manually.
- Viewing via an extension that doesn't support Sort by/Group by → doesn't emit; still places items. `showIf`, `displayName`, `icon`The slice hasn't been created yet → manual instructions required.
- Action `CALL/SMS/EMAIL/OPEN_FILE` Target not supported → no emit.
- `REF_ACTION`: put `referencedTable` before `referencedAction` (That action must be real).

**Consistent with the standard for this skill:**
- The new view name is set according to the table name in section 5 (`SANPHAM`, `SANPHAMUSER`...), concise, not beginning with `_` (Engine requirement); display name in Vietnamese enclosed in double quotes.
- Hidden views/actions: `icon` = `minus` (add action) `position` = `Hide`, view more `showIf` = `"false"`).
- Action group numbering `X.0`/`X.1`/`X.2` As per section 6; the FontAwesome icon is accurate; the action color follows the formatting rule in section 6.2 (approve/complete = green, cancel/discard = red, create file = blue).
- The Valid If status/category is taken from the correct SOURCE as in section 3.1; the permission formula is in the correct A/B style as finalized in Step 1.
