from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/args')
def args():
    return render_template('args.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html'))
    if request.cookies.get('name') is None:
        response.set_cookie('name', 'qq')
    else:
         response.set_cookie('name', 'qq', expires=0)
    return response

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = None
    error_msg = None
    if request.method == 'POST':
        try:
            operand1 = float(request.form.get('operand1'))
            operand2 = float(request.form.get('operand2'))
            operation = request.form.get('operation')
            if operation == '+':
                result = operand1 + operand2
            elif operation == '-':
                result = operand1 - operand2
            elif operation == '*':
                result = operand1 * operand2
            elif operation == '/':
                result = operand1 / operand2
        except ValueError:
            error_msg = 'Пожалуйста вводите только числа.'
        except ZeroDivisionError:
            error_msg = 'На ноль делить нельзя.'
    response = make_response(render_template('calc.html', result=result, error_msg=error_msg))
    return response

@app.route('/tnum', methods=['GET', 'POST'])
def tnum():
    telephon = None
    msg = None
    msg_color = None
    form_color = None
    if request.method == 'POST':
        telephon = request.form.get('telephon')
        telephon = telephon.replace('+','')
        telephon = telephon.replace(' ','')
        telephon = telephon.replace('(','')
        telephon = telephon.replace(')','')
        telephon = telephon.replace('-','')
        telephon = telephon.replace('.','')
        try:
            telephon = int(telephon)
            telephon = str(telephon)
            if len(telephon) not in range(10,12):
                msg = 'Недопустимый ввод. Неверное количество цифр.'
                msg_color = 'invalid-feedback'
                form_color = 'is-invalid'
            else:
                msg = 'Номер телефона верный!'
                msg_color = 'valid-feedback'
                form_color = 'is-valid'
        except ValueError:
            if not telephon:
                msg = 'Введите номер телефона.'
                msg_color = 'invalid-feedback'
                form_color = 'is-invalid'
            else:
                msg = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
                msg_color = 'invalid-feedback'
                form_color = 'is-invalid'
    
    return render_template('tnum.html', msg=msg, msg_color=msg_color, form_color=form_color)