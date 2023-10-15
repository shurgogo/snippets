import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Dialog


class FormDataEntry(Dialog):
    def __init__(self,
                 labels: list[str] = None,
                 title='Form Data Entry',
                 padding=(20, 20),
                 parent=None,
                 fns=None,
                 ):
        super().__init__(parent, title)
        self._valid_fns = [] if fns is None else fns
        if labels is not None:
            self._labels = labels
        else:
            raise Exception('labels should not be empty')
        self._padding = padding
        self._entries: list[ttk.Entry] = []

    def create_body(self, master):
        frame = ttk.Frame(master, padding=self._padding)
        frame.pack(fill=X, expand=True)

        for lbl in self._labels:
            self._create_entry(master=frame, label=lbl)

        self._initial_focus = self._entries[0]

    def _create_entry(self, master, label):
        entry_row = ttk.Frame(master)
        entry_row.pack(fill=X, expand=YES, pady=5)

        data_lbl = ttk.Label(master=entry_row, text=label.strip().title(), width=10)
        data_lbl.pack(side=LEFT, padx=5)

        data_entry = ttk.Entry(master=entry_row)
        data_entry.pack(side=LEFT, padx=5, fill=X, expand=YES)

        self._entries.append(data_entry)

    def create_buttonbox(self, master):
        bbx_frame = ttk.Frame(master, padding=(5, 10))

        submit_btn = ttk.Button(
            master=bbx_frame,
            bootstyle=PRIMARY,
            text='Confirm',
            command=self._on_submit,
        )
        submit_btn.pack(padx=5, side=RIGHT)
        submit_btn.lower()  # set focus traversal left-to-right

        cancel_btn = ttk.Button(
            master=bbx_frame,
            bootstyle=SECONDARY,
            text='Cancel',
            command=self._on_cancel,
        )
        cancel_btn.pack(padx=5, side=RIGHT)
        cancel_btn.lower()  # set focus traversal left-to-right

        ttk.Separator(self._toplevel).pack(fill=X)
        bbx_frame.pack(side=BOTTOM, fill=X, anchor=S)

    def _on_submit(self, *_):
        self._result = {}
        for i, e in enumerate(self._entries):
            self._result[self._labels[i]] = e.get()
        valid_result = self.validate()
        if not valid_result:
            self._result = None
            return
        self._toplevel.destroy()

    def _on_cancel(self, *_):
        self._toplevel.destroy()
        self._result = None

    def validate(self):
        for func in self._valid_fns:
            if not func(self._result):
                return False
        return True


class ConfigRow(ttk.Frame):
    def __init__(
            self,
            master,
            primary_key,
            name,
            all_data: dict,
            get_cur_fn,
            set_cur_fn,
            **kwargs,
    ):
        super().__init__(master, **kwargs)
        self._primary_key = primary_key
        self._name = name
        self._all: dict = all_data
        self._get_cur = get_cur_fn
        self._set_cur = set_cur_fn

        self.create_ui()

    def create_ui(self):
        # label
        lbl = ttk.Label(self, text=self._name, width=10)
        lbl.pack(side=LEFT, padx=(15, 0))

        # drop list
        values = [value for value in self._all.keys()]
        cbx = ttk.Combobox(
            master=self,
            values=values,
            bootstyle=PRIMARY,
            state=READONLY,
        )
        if self._get_cur() is not None:
            cbx.set(self._get_cur()[self._primary_key])
        cbx.pack(side=LEFT, fill=X, expand=YES, padx=5)

        def change(e):
            self._set_cur(self._all[cbx.get()])

        cbx.bind('<<ComboboxSelected>>', change)

        # add button
        add_btn = ttk.Button(
            master=self,
            text='Add',
            command=self._on_add(cbx=cbx, title=f'{self._name} Addition'),
            width=6,
            bootstyle='success-outline',
        )
        add_btn.pack(side=LEFT, padx=5)

        # delete button
        del_btn = ttk.Button(
            master=self,
            text='Delete',
            command=self._on_delete(cbx=cbx, title=f'{self._name} Addition'),
            width=6,
            bootstyle='danger-outline',
        )
        del_btn.pack(side=LEFT, padx=5)

    def _on_add(self, cbx: ttk.Combobox, title):
        def inner():
            entry = FormDataEntry(labels=list(self._get_cur().keys()), title=title, parent=self)
            entry.show()
            new_data = {}
            # cancel add
            if entry.result is None:
                return

            for k, v in entry.result.items():
                new_data[k] = v
            self._all[new_data[self._primary_key]] = new_data
            self._set_cur(new_data)
            values = [value for value in self._all.keys()]
            cbx['values'] = values
            cbx.set(self._get_cur()[self._primary_key])

        return inner

    def _on_delete(self, cbx: ttk.Combobox, title):
        def inner():
            # entry = FormDataEntry(labels=list(self._get_cur().keys()), title=title, parent=self)
            # entry.show()
            if len(self._all) > 1:
                self._all.pop(self._get_cur()[self._primary_key])
                values = [value for value in self._all.keys()]
                self._set_cur(self._all[values[0]])
                cbx['values'] = values
                cbx.set(values[0])
            elif len(self._all) == 1:
                self._all.pop(self._get_cur()[self._primary_key])
                self._set_cur(None)
                cbx['values'] = ''
                cbx.set('')

        return inner
