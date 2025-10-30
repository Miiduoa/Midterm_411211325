"""
initial environment

本檔新增 CLI 後備模式：
  - 使用 `python Integration.py --nogui` 或環境變數 `NO_TK=1` 可避免載入 tkinter
  - 以便在 macOS 舊版或 Tk 不相容時仍可操作資料庫
"""

# import modules（延後載入 tkinter，避免在不相容環境直接崩潰）
import os
import sys
import sqlite3


# connect to database and build environment（共用於 GUI/CLI）
conn = sqlite3.connect('Student.db')
cursor = conn.cursor()


def run_gui() -> None:
    import tkinter as tk  # 僅在需要 GUI 時載入

    # basic GUI 
    root = tk.Tk()
    root.title('INTEGRATION')
    root.geometry('300x400')

    # new label and input
    # student ID label and entry
    label_id = tk.Label(root, text='Student ID')
    label_id.pack(pady=(15,5))
    entry_id = tk.Entry(root, width=25)
    entry_id.pack()

    # student name label and entry
    label_name = tk.Label(root, text='Student Name')
    label_name.pack(pady=(10,5))
    entry_name = tk.Entry(root, width=25)
    entry_name.pack()

    # setting print_student function
    def print_student():
        student_id = entry_id.get()
        student_name = entry_name.get()

        print('Student ID: {}'.format(student_id))
        print('Student Name: {}'.format(student_name))
        print('-'*30)

    # new a button: Print
    botton_print = tk.Button(root, text='Print', command=print_student)
    botton_print.pack(pady=15)

    # def a create_student()
    def create_student():
        student_id = entry_id.get()
        student_name = entry_name.get().lower()  # application layer

        cursor.execute('INSERT INTO DB_student (db_student_id, db_student_name) VALUES(?,?)', (student_id, student_name))
        conn.commit()

        print('Student ID: {}'.format(student_id))
        print('Student Name: {}'.format(student_name))
        print('-' * 30)

    button_create = tk.Button(root, text='Create', command=create_student)
    button_create.pack(pady=20)

    # delete a student by id
    def delete_student():
        student_id = entry_id.get()

        if not student_id:
            print('Please enter the Student ID to delete.')
            return

        cursor.execute('DELETE FROM DB_student WHERE db_student_id = ?', (student_id,))
        conn.commit()

        if cursor.rowcount:
            print(f'Student ID {student_id} deleted.')
        else:
            print(f'Student ID {student_id} not found.')

    button_delete = tk.Button(root, text='Delete', command=delete_student)
    button_delete.pack(pady=20)

    # def a overview_student()
    # show all records in sqlite
    def overview_student():
        cursor.execute('SELECT * from DB_student')
        overview = cursor.fetchall()
        print(overview)

    # new botton Overview
    botton_overview = tk.Button(root, text='Overview', command=overview_student)
    botton_overview.pack(pady=25)

    root.mainloop()  # must be put to the end of programming code


def run_cli() -> None:
    print('Running in CLI mode (tkinter disabled).')
    print('Commands: create <id> <name> | delete <id> | overview | print <id> <name> | exit')
    while True:
        try:
            raw = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nBye')
            break

        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()

        if cmd == 'exit':
            print('Bye')
            break
        elif cmd == 'create' and len(parts) >= 3:
            student_id = parts[1]
            student_name = ' '.join(parts[2:]).lower()
            cursor.execute('INSERT INTO DB_student (db_student_id, db_student_name) VALUES(?,?)', (student_id, student_name))
            conn.commit()
            print('Student ID: {}'.format(student_id))
            print('Student Name: {}'.format(student_name))
            print('-' * 30)
        elif cmd == 'delete' and len(parts) == 2:
            student_id = parts[1]
            cursor.execute('DELETE FROM DB_student WHERE db_student_id = ?', (student_id,))
            conn.commit()
            if cursor.rowcount:
                print(f'Student ID {student_id} deleted.')
            else:
                print(f'Student ID {student_id} not found.')
        elif cmd == 'overview':
            cursor.execute('SELECT * from DB_student')
            overview = cursor.fetchall()
            print(overview)
        elif cmd == 'print' and len(parts) >= 3:
            student_id = parts[1]
            student_name = ' '.join(parts[2:])
            print('Student ID: {}'.format(student_id))
            print('Student Name: {}'.format(student_name))
            print('-'*30)
        else:
            print('Invalid command')


if __name__ == '__main__':
    nogui = ('--nogui' in sys.argv) or (os.environ.get('NO_TK') == '1')
    if nogui:
        run_cli()
    else:
        try:
            run_gui()
        except Exception as e:
            # 若 GUI 啟動失敗，回落至 CLI
            print(f'GUI failed to start: {e}')
            run_cli()
