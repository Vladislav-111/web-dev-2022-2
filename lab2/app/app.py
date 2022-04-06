from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app


@app.route('/index')
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

