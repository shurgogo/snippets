import csv

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import yaml

import component
import api

CONFIG_PATH = './config.yaml'
MESSAGE_PATH = './messages.csv'

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
    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        self.email_addrs = {}
        self.cur_email_addr = None
        self.ume_addrs = {}
        self.cur_ume_addr = None
        self.msgs = {}

        self.load_data()

        self._create_config()
        self._create_message_view()
        self._create_action()
        self._create_progress_bar()

    def load_data(self):
        # config
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
            if config.get('email'):
                for email in config['email']:
                    self.email_addrs[email['address']] = email
                self.cur_email_addr = self.email_addrs[config['email'][0]['address']]
            if config.get('ume'):
                for ume in config['ume']:
                    self.ume_addrs[ume['address']] = ume
                self.cur_ume_addr = self.ume_addrs[config['ume'][0]['address']]

        # message
        with open(MESSAGE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            reader_list = list(reader)
            print(len(reader_list))
            print(len(reader_list[0]))
            for i in range(len(reader_list) - 1):
                self.msgs[
                    reader_list[i + 1][TITLE_TO_INDEX['Title']] +
                    reader_list[i + 1][TITLE_TO_INDEX['From']] +
                    reader_list[i + 1][TITLE_TO_INDEX['Date']]
                    ] = reader_list[i + 1]

    def _create_config(self):
        # header and labelframe container
        config_lf = ttk.Labelframe(self, text='Complete the form to begin your work', padding=15)
        config_lf.pack(fill=X, expand=NO, anchor=N)

        email_row = component.ConfigRow(
            master=config_lf,
            primary_key='address',
            name='Email',
            all_data=self.email_addrs,
            get_cur_fn=self._get_cur_fn('email'),
            set_cur_fn=self._set_cur_fn('email'),
        )
        email_row.pack(fill=X, expand=YES)

        ume_row = component.ConfigRow(
            master=config_lf,
            primary_key='address',
            name='UME',
            all_data=self.ume_addrs,
            get_cur_fn=self._get_cur_fn('ume'),
            set_cur_fn=self._set_cur_fn('ume'),
        )
        ume_row.pack(fill=X, expand=YES, pady=(15, 5))

    def _get_cur_fn(self, name):
        def ume():
            return self.cur_ume_addr

        def email():
            return self.cur_email_addr

        fns = {
            'ume': ume,
            'email': email,
        }
        return fns[name]

    def _set_cur_fn(self, name):
        def ume(new_ume_addr):
            self.cur_ume_addr = new_ume_addr

        def email(new_email_addr):
            self.cur_email_addr = new_email_addr

        fns = {
            'ume': ume,
            'email': email,
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
            pass

        def _create_progress_bar(self):
            pass

    def _create_action(self):
        action_row = ttk.Frame(self)
        action_row.pack(fill=X, expand=NO, pady=5)
        self.send_btn = ttk.Button(
            master=action_row,
            text='Send',
            command=self._on_send,
            width=6,
            bootstyle=SUCCESS,
        )
        self.send_btn.pack(side=RIGHT, padx=5)
        self.fetch_btn = ttk.Button(
            master=action_row,
            text='Fetch',
            command=self._on_fetch,
            width=6,
            bootstyle=DANGER,
        )
        self.fetch_btn.pack(side=RIGHT, padx=5)

    def _on_fetch(self):
        self.progressbar.start()
        self.fetch_btn.config(state=DISABLED)

        addr = self.cur_email_addr['address']
        user = self.cur_email_addr['username']
        passwd = self.cur_email_addr['password']
        mailbox = self.cur_email_addr['mailbox']
        if self.cur_email_addr['protocol'] == 'pop3':
            client = api.POP3Client(addr=addr, user=user, passwd=passwd, mailbox=mailbox)
        else:  # self.cur_email_addr['protocol'] == 'imap':
            client = api.IMAPClient(addr=addr, user=user, passwd=passwd, mailbox=mailbox)
        login_success = client.login()
        if not login_success:
            return []
        emails = client.fetch()
        client.close()
        self._update_msgs(emails)

        self.progressbar.stop()
        self.fetch_btn.configure(state=NORMAL)

    def _update_msgs(self, emails):
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

    def _on_send(self):
        ip = self.cur_ume_addr['address']
        port = self.cur_ume_addr['port']
        username = self.cur_ume_addr['username']
        password = self.cur_ume_addr['password']
        client = api.UME(
            user=username,
            passwd=password,
            ip=ip,
            port=port,
        )

        for iid in self.tv.view.selection():
            row = self.tv.get_row(iid=iid)
            body = row.values[TITLE_TO_INDEX['Title']]
            print('send %s to ume %s' % (body, self.cur_ume_addr['address']))
            result = client.send(body)
            if result == 'success':
                print('send success')
                row.values[TITLE_TO_INDEX['Sent']] = 'TRUE'
                row.refresh()
                self.msgs[
                    row.values[TITLE_TO_INDEX['Title']] +
                    row.values[TITLE_TO_INDEX['From']] +
                    row.values[TITLE_TO_INDEX['Date']]
                    ] = row.values

    def _create_progress_bar(self):
        self.progressbar = ttk.Progressbar(
            master=self,
            mode=INDETERMINATE,
            bootstyle=(STRIPED, SUCCESS),
        )
        self.progressbar.pack(fill=X, expand=NO)



if __name__ == '__main__':
    app = ttk.Window('Email Forwarder', 'litera')

    scr_width = app.winfo_screenwidth()
    scr_height = app.winfo_screenheight()
    width = 800
    height = 600
    left = (scr_width - width) / 2
    top = (scr_height - height) / 2

    app.geometry('%dx%d+%d+%d' % (width, height, left, top))
    EmailForwarder(app)
    app.mainloop()
