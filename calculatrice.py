import tkinter as tk
from tkinter import messagebox
import math


_NS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'sqrt': math.sqrt,
    'exp': math.exp,
    'factorial': math.factorial,
    'pi': math.pi,
    'e': math.e,
    'abs': abs
}


def evaluate(expr: str, deg: bool = False):
    if not isinstance(expr, str):
        raise TypeError('expression must be a string')
    s = expr.strip()
    s = s.replace('^', '**')
    s = s.replace('fact(', 'factorial(')
    
    ns = dict(_NS)
    if deg:
        ns['sin'] = lambda x: math.sin(math.radians(x))
        ns['cos'] = lambda x: math.cos(math.radians(x))
        ns['tan'] = lambda x: math.tan(math.radians(x))
    else:
        ns['sin'] = math.sin
        ns['cos'] = math.cos
        ns['tan'] = math.tan

    try:
        return eval(s, {'__builtins__': None}, ns)
    except Exception:
        raise


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Calculatrice scientifique')
        self.geometry('420x520')
        self.resizable(False, False)

        
        self.configure(bg='black')

        self._font = ('Segoe UI', 16)
        self._btn_font = ('Segoe UI', 12)

        self.display_var = tk.StringVar()
        self.display = tk.Entry(self, textvariable=self.display_var, font=self._font, bd=6, relief='ridge', justify='right', bg='#111', fg='white', insertbackground='white')
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=12, sticky='we')
    
        self.display.bind('<Key>', lambda e: 'break')
        self.display.bind('<<Paste>>', lambda e: 'break')
        self.display.bind('<Control-v>', lambda e: 'break')
        self.display.bind('<Button-2>', lambda e: 'break')
        self.display.focus_set()

        
        toolbar_frame = tk.Frame(self, bg='black')
        toolbar_frame.grid(row=1, column=0, columnspan=5, sticky='we', padx=6)
        self._mode_btn = tk.Button(toolbar_frame, text='RAD', width=6, command=self._toggle_mode, bg='#333', fg='white', bd=0, activebackground='#555')
        self._mode_btn.pack(side='right', padx=4)

        self._deg = False

        buttons = [
            ['7', '8', '9', '/', '^'],
            ['4', '5', '6', '*', 'π'],
            ['1', '2', '3', '-', '('],
            ['0', '.', '=', '+', ')'],
            ['sin', 'cos', 'tan', 'log', 'exp'],
            ['√', 'fact', 'C', 'CE', 'Ans']
        ]

    
        self.bg_btn = '#333333'   
        self.op_btn = '#ff9500'   
        self.func_btn = '#007aff' 

        for r, row in enumerate(buttons, start=2):
            for c, label in enumerate(row):
                style = {'bg': self.bg_btn, 'fg': 'white'}
                if label in ('/', '*', '-', '+', '=', '^'):
                    style['bg'] = self.op_btn
                if label in ('sin', 'cos', 'tan', 'log', 'exp', '√', 'fact'):
                    style['bg'] = self.func_btn

                if label == '':
                    
                    spacer = tk.Label(self, text='', bg=self.bg_btn)
                    spacer.grid(row=r, column=c, padx=6, pady=6, sticky='nsew')
                else:
                    btn = tk.Button(self, text=label, font=self._btn_font, bd=0, relief='flat',
                                    bg=style['bg'], fg=style['fg'], activebackground='#555555', command=lambda L=label: self._on_click(L))
                    btn.grid(row=r, column=c, padx=6, pady=6, sticky='nsew')

        
        for i in range(5):
            self.grid_columnconfigure(i, weight=1, uniform='a')
        for i in range(2, 8):
            self.grid_rowconfigure(i, weight=1)

        self._last = None

    def _set_text(self, text: str):
        self.display_var.set(text)
        try:
            self.display.icursor(tk.END)
            self.display.focus_set()
        except Exception:
            pass

    def _insert(self, text: str):
        self._set_text(self.display_var.get() + text)

    def _toggle_mode(self):
        self._deg = not self._deg
        self._mode_btn.config(text='DEG' if self._deg else 'RAD')

    def _on_click(self, label: str):
        if label == 'C':
            self.display_var.set('')
            return
        if label == 'CE':
            self.display_var.set(self.display_var.get()[:-1])
            return
        if label == '=':
            expr = self.display_var.get()
            try:
                res = evaluate(expr, deg=self._deg)
                self._last = res
                self._set_text(str(res))
            except Exception as exc:
                messagebox.showerror('Error', str(exc))
            return
        if label == 'Ans':
            if self._last is not None:
                self._set_text(self.display_var.get() + str(self._last))
            return

        if label == 'sqrt':
            self._set_text(self.display_var.get() + 'sqrt(')
            return
        if label in ('sin', 'cos', 'tan', 'log', 'exp'):
            self._set_text(self.display_var.get() + f'{label}(')
            return
        if label == 'fact':
            self._set_text(self.display_var.get() + 'factorial(')
            return

        if label == '√':
            self._set_text(self.display_var.get() + 'sqrt(')
            return
        if label == 'π' or label == 'pi':
            self._set_text(self.display_var.get() + 'pi')
            return

        self._set_text(self.display_var.get() + label)



if __name__ == '__main__':
    app = CalculatorApp()
    app.mainloop()
