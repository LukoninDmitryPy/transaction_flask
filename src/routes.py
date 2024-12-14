# routes.py
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, flash, current_app, render_template, redirect, url_for
from models import db, User, Transaction
from forms import TransactionForm
from flask_wtf.csrf import CSRFProtect
import logging
logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)
csrf = CSRFProtect()

@api.route('/create_transaction', methods=['POST'])
@login_required
@csrf.exempt
def create_transaction():
    """
    Создание новой транзакции
    ---
    tags:
      - transactions
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - amount
          properties:
            amount:
              type: number
              description: Сумма транзакции
    responses:
      201:
        description: Транзакция создана успешно
        schema:
          type: object
          properties:
            id:
              type: integer
            status:
              type: string
      400:
        description: Ошибка валидации данных
    """
    form = TransactionForm()
    if form.validate_on_submit():
        amount = form.amount.data
        commission = amount * current_user.commission_rate # Пример расчета комиссии
        transaction = Transaction(amount=amount, commission=commission, user_id=current_user.id)
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'id': transaction.id, 'status': transaction.status}), 201
    return jsonify({'message': 'Invalid data'}), 400

@api.route('/cancel_transaction/<int:transaction_id>', methods=['POST'])
def cancel_transaction(transaction_id):
    """
    Отмена транзакции
    ---
    tags:
      - transactions
    parameters:
      - name: transaction_id
        in: path
        type: integer
        required: true
        description: ID транзакции
    responses:
      200:
        description: Транзация отменена
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Транзакция не найдена
    """
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.status == 'pending':
        transaction.status = 'canceled'
        db.session.commit()
        return jsonify({'message': 'Transaction canceled successfully'}), 200
    else:
        return jsonify({'message': 'Cannot cancel non-pending transaction'}), 400

@api.route('/check_transaction/<int:transaction_id>', methods=['GET'])
@login_required
def check_transaction(transaction_id):
    """
    Получение информации о транзакции
    ---
    tags:
      - transactions
    parameters:
      - name: transaction_id
        in: path
        type: integer
        required: true
        description: ID транзакции
    responses:
      200:
        description: Информация о транзакции
        schema:
          type: object
          properties:
            id:
              type: integer
            amount:
              type: number
            commission:
              type: number
            status:
              type: string
            created_at:
              type: string
      404:
        description: Транзакция не найдена
    """
    transaction = Transaction.query.get_or_404(transaction_id)
    return jsonify({
        'id': transaction.id,
        'amount': transaction.amount,
        'commission': transaction.commission,
        'status': transaction.status,
        'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

@api.route('/transactions/<int:transaction_id>')
@login_required
def transaction_detail(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    status_colors = {
        'pending': 'warning',
        'confirmed': 'success',
        'canceled': 'danger',
        'expired': 'secondary'
    }
    return render_template('transactions/detail.html', 
                         transaction=transaction,
                         status_colors=status_colors)

@api.route('/transactions/create')
@login_required
def create_transaction_page():
    return render_template('transactions/create.html')

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('api.login_page'))


@api.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    webhook = data.get('webhook')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=generate_password_hash(password), webhook_url=webhook)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@api.route('/loginn', methods=['GET'])
def login_page():
    return render_template('auth/login.html')

@api.route('/registerr', methods=['GET'])
def register_page():
    return render_template('auth/register.html')
