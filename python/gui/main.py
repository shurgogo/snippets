import csv
import logging
import os
from queue import Queue
from threading import Thread
import time

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
import yaml

import email_api, sys_api
import component
import util

logging.basicConfig(
    format='%(asctime)s:%(filename)s[line:%(lineno)d]:%(levelname)s:%(message)s',
    level=logging.DEBUG,
    encoding='utf-8',
    filename='forwarder.log',
    filemode='w'
)

CONFIG_PATH = 'config.yaml'
MESSAGE_PATH = 'messages.csv'
SYSTEM_NAME = 'sys'
EMAIL_NAME = 'email'

TITLE_TO_INDEX = {
    'Sent': 0,
    'Title': 1,
    'Content': 2,
    'From': 3,
    'Date': 4,
}

INDEX_TO_TITLE = {
    0: 'Sent',
    1: 'Title',
    2: 'Content',
    3: 'From',
    4: 'Date',
}


class EmailForwarder(ttk.Frame):
    thread_q = Queue()

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)
        self.images = [
            ttk.PhotoImage(
                name='refresh-small',
                file='./assets/refresh.png',
            ),
            ttk.PhotoImage(
                name='send-small',
                file='./assets/send.png'
            )
        ]

        self.email_addrs = {}
        self.cur_email_addr = None
        self.sys_addrs = {}
        self.cur_sys_addr = None
        self.msgs = {}
        self.action_result: util.Result = None
        self._secret_key = '1234123412341234abcdabcdabcdabcd'

        self.load_data()

        self._create_config()
        self._create_message_view()
        self._create_action()
        self._create_progress_bar()

    def load_data(self):
        # config
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = yaml.load(f.read(), Loader=yaml.FullLoader)
                if config.get(EMAIL_NAME):
                    for email in config[EMAIL_NAME]:
                        passwd = util.AESCipher(self._secret_key).decrypt(email['password'])
                        email['password'] = passwd
                        self.email_addrs[email['username']] = email
                    self.cur_email_addr = self.email_addrs[config[EMAIL_NAME][0]['username']]
                if config.get(SYSTEM_NAME):
                    for my_sys in config[SYSTEM_NAME]:
                        passwd = util.AESCipher(self._secret_key).decrypt(my_sys['password'])
                        my_sys['password'] = passwd
                        self.sys_addrs[my_sys['address']] = my_sys
                    self.cur_sys_addr = self.sys_addrs[config[SYSTEM_NAME][0]['address']]
        if len(self.email_addrs) == 0:
            # default value
            self.cur_email_addr = util.GET_DEFAULT[EMAIL_NAME]
            self.email_addrs[self.cur_email_addr['username']] = self.cur_email_addr
        if len(self.sys_addrs) == 0:
            self.cur_sys_addr = util.GET_DEFAULT[SYSTEM_NAME]
            self.sys_addrs[self.cur_sys_addr['address']] = self.cur_sys_addr

        # message
        if os.path.exists(MESSAGE_PATH):
            with open(MESSAGE_PATH, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                reader_list = list(reader)
                if len(reader_list) == 1:  # only title row
                    return
                for i in range(len(reader_list) - 1):
                    self.msgs[
                        reader_list[i + 1][TITLE_TO_INDEX['Title']] +
                        reader_list[i + 1][TITLE_TO_INDEX['From']] +
                        reader_list[i + 1][TITLE_TO_INDEX['Date']]
                        ] = reader_list[i + 1]

    def save_data(self):
        def _encrypt(data_list):
            for i in range(len(data_list)):
                passwd = data_list[i]['password']
                passwd = util.AESCipher(self._secret_key).encrypt(passwd)
                data_list[i]['password'] = passwd

        # config
        email_list = list(self.email_addrs.values())
        _encrypt(email_list)

        my_sys_list = list(self.sys_addrs.values())
        _encrypt(my_sys_list)

        config = {
            EMAIL_NAME: email_list,
            SYSTEM_NAME: my_sys_list
        }
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, encoding='utf-8', allow_unicode=True)

        # message
        with open(MESSAGE_PATH, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Sent', 'Title', 'Content', 'From', 'Date'])
            for msg in self.msgs.values():
                writer.writerow(msg)

    def _create_config(self):
        # header and labelframe container
        config_lf = ttk.Labelframe(self, text='Complete the form to begin your work', padding=15)
        config_lf.pack(fill=X, expand=NO, anchor=N)

        email_row = component.ConfigRow(
            master=config_lf,
            primary_key='username',
            name=EMAIL_NAME.title(),
            all_data=self.email_addrs,
            get_cur_fn=self._get_cur_fn(EMAIL_NAME),
            set_cur_fn=self._set_cur_fn(EMAIL_NAME),
        )
        email_row.pack(fill=X, expand=YES)

        sys_row = component.ConfigRow(
            master=config_lf,
            primary_key='address',
            name=SYSTEM_NAME.title(),
            all_data=self.sys_addrs,
            get_cur_fn=self._get_cur_fn(SYSTEM_NAME),
            set_cur_fn=self._set_cur_fn(SYSTEM_NAME),
        )
        sys_row.pack(fill=X, expand=YES, pady=(15, 5))

    def _get_cur_fn(self, name):
        def my_sys():
            return self.cur_sys_addr

        def email():
            return self.cur_email_addr

        fns = {
            SYSTEM_NAME: my_sys,
            EMAIL_NAME: email,
        }
        return fns[name]

    def _set_cur_fn(self, name):
        def my_sys(new_sys_addr):
            self.cur_sys_addr = new_sys_addr

        def email(new_email_addr):
            self.cur_email_addr = new_email_addr

        fns = {
            SYSTEM_NAME: my_sys,
            EMAIL_NAME: email,
        }
        return fns[name]

    def _create_message_view(self):
        columns = [
            {'text': 'Sent', 'stretch': False, 'width': 60},
            {'text': 'Title', 'stretch': True, 'width': 300},
            {'text': 'Content', 'stretch': False, 'width': 300},
            {'text': 'From', 'stretch': False, 'width': 100},
            {'text': 'Date', 'stretch': False, 'width': 100},
        ]
        self.tv = Tableview(
            master=self,
            coldata=columns,
            rowdata=list(self.msgs.values()),
            paginated=True,
            searchable=True,
            autoalign=True,
            stripecolor=('#f0f0ed', None),
            bootstyle=PRIMARY,
        )
        self.tv.pack(fill=BOTH, expand=YES, pady=10)

    def _create_action(self):
        action_row = ttk.Frame(self)
        action_row.pack(fill=X, expand=NO, pady=5)
        self.send_btn = ttk.Button(
            master=action_row,
            text='Send',
            image='send-small',
            compound=RIGHT,
            command=self._on_send,
            bootstyle=SUCCESS,
        )
        self.send_btn.pack(side=RIGHT, padx=5)

        self.fetch_btn = ttk.Button(
            master=action_row,
            text='Fetch',
            image='refresh-small',
            compound=LEFT,
            command=self._on_fetch,
            bootstyle=DANGER,
        )
        self.fetch_btn.pack(side=RIGHT, padx=5)

    def _on_fetch(self):
        self.progressbar.start()
        self.fetch_btn.config(state=DISABLED)

        def _fetch_and_update():
            addr = self.cur_email_addr['address']
            user = self.cur_email_addr['username']
            passwd = self.cur_email_addr['password']
            mailbox = self.cur_email_addr['mailbox']
            if self.cur_email_addr['protocol'] == 'pop3':
                client = email_api.POP3Client(addr=addr, user=user, passwd=passwd, mailbox=mailbox)
            else:  # self.cur_email_addr['protocol'] == 'imap':
                client = email_api.IMAPClient(addr=addr, user=user, passwd=passwd, mailbox=mailbox)
            login_success = client.login()
            if not login_success:
                self.action_result = util.Result(action='Login', result=False, msg='Login %s failed' % user)
                time.sleep(0.1)
            else:
                emails = client.fetch()
                client.close()
                # update Tableview
                for e in emails:
                    title = e.get('Title')
                    from_ = e.get('From')
                    date = e.get('Date')
                    content = e.get('Content')
                    if self.msgs.get(title + from_ + date):
                        continue
                    new_msg = ['FALSE', title, content, from_, date]
                    self.msgs[title + from_ + date] = new_msg
                    self.tv.insert_row(END, new_msg)
                self.tv.load_table_data()
                self.action_result = util.Result(action='Fetch', result=True, msg='Fetch emails from %s success' % user)

            # close task
            EmailForwarder.thread_q.task_done()

        thread = Thread(
            target=_fetch_and_update,
            daemon=True
        )
        EmailForwarder.thread_q.put(thread.start())
        self.listen_for_complete_btn_task(self.fetch_btn)

    def listen_for_complete_btn_task(self, btn: ttk.Button):
        if EmailForwarder.thread_q.unfinished_tasks == 0:
            self.progressbar.stop()
            if self.action_result.result:
                Messagebox.ok(
                    title=self.action_result.action,
                    message=self.action_result.msg,
                    position=(int(scr_width / 2) - 150, int(scr_height / 2) - 100)
                )
            else:
                Messagebox.show_error(
                    title=self.action_result.action,
                    message=self.action_result.msg,
                    position=(int(scr_width / 2) - 150, int(scr_height / 2) - 100)
                )
            btn.configure(state=NORMAL)
            return
        self.after(1, lambda: self.listen_for_complete_btn_task(btn))

    def _on_send(self):
        self.progressbar.start()
        self.send_btn.config(state=DISABLED)

        def _send_and_update():
            # build body
            ip = self.cur_sys_addr['address']
            port = self.cur_sys_addr['port']
            username = self.cur_sys_addr['username']
            password = self.cur_sys_addr['password']
            client = sys_api.Sys(
                user=username,
                passwd=password,
                ip=ip,
                port=port,
            )

            # send and update
            self.action_result = util.Result(
                action='Send',
                result=True,
                msg='Nothing sended to sys %s' % self.cur_sys_addr['address']
            )
            for iid in self.tv.view.selection():
                row = self.tv.get_row(iid=iid)
                body = row.values[TITLE_TO_INDEX['Title']]
                success = client.send(body)
                if success:
                    row.values[TITLE_TO_INDEX['Sent']] = 'TRUE'
                    row.refresh()
                    self.msgs[
                        row.values[TITLE_TO_INDEX['Title']] +
                        row.values[TITLE_TO_INDEX['From']] +
                        row.values[TITLE_TO_INDEX['Date']]
                        ] = row.values
                    self.action_result = util.Result(
                        action='Send',
                        result=True,
                        msg='Send %s to sys %s success' % (body, self.cur_sys_addr['address'])
                    )
                else:
                    self.action_result = util.Result(
                        action='Send',
                        result=False,
                        msg='Send %s to sys %s failed' % (body, self.cur_sys_addr['address'])
                    )

            # close task
            EmailForwarder.thread_q.task_done()

        thread = Thread(
            target=_send_and_update,
            daemon=True
        )

        EmailForwarder.thread_q.put(thread.start())
        self.listen_for_complete_btn_task(self.send_btn)

    def _create_progress_bar(self):
        self.progressbar = ttk.Progressbar(
            master=self,
            mode=INDETERMINATE,
            bootstyle=(STRIPED, SUCCESS),
        )
        self.progressbar.pack(fill=X, expand=NO)


if __name__ == '__main__':
    root = ttk.Window('Email Forwarder', 'litera')
    root.tk.eval('::msgcat::mclocale en_us')

    scr_width = root.winfo_screenwidth()
    scr_height = root.winfo_screenheight()
    width = 800
    height = 600
    left = (scr_width - width) / 2
    top = (scr_height - height) / 2

    root.geometry('%dx%d+%d+%d' % (width, height, left, top))
    app = EmailForwarder(root)


    def close_app():
        app.save_data()
        root.destroy()


    root.protocol('WM_DELETE_WINDOW', close_app)
    root.mainloop()
