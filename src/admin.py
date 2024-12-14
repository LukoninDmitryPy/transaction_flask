from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from models import db, User, Transaction
from datetime import datetime, timedelta
from sqlalchemy import func

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
def dashboard():
    users_count = User.query.count()
    transactions_count = Transaction.query.count()
    today = datetime.now().date()
    today_transactions = Transaction.query.filter(
        func.date(Transaction.created_at) == today
    ).all()
    today_amount = sum(t.amount for t in today_transactions)
    recent_transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         users_count=users_count,
                         transactions_count=transactions_count,
                         today_amount=today_amount,
                         recent_transactions=recent_transactions)

@admin.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/create', methods=['POST'])
@login_required
def create_user():
    data = request.json
    user = User(
        username=data['username'],
        commission_rate=data['commission_rate'],
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@admin.route('/users/<int:user_id>', methods=['PUT', 'DELETE'])
@login_required
def manage_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    
    data = request.json
    user.username = data['username']
    user.commission_rate = data['commission_rate']
    user.role = data['role']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@admin.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.all()
    return render_template('admin/transactions.html', transactions=transactions)

@admin.route('/transactions/data')
@login_required
def transactions_data():
    transactions = Transaction.query.all()
    return jsonify([{
        'id': t.id,
        'amount': t.amount,
        'commission': t.commission,
        'status': t.status,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for t in transactions])

@admin.route('/transactions/<int:transaction_id>', methods=['GET', 'PUT'])
@login_required
def transaction_detail(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if request.method == 'PUT':
        data = request.json
        if transaction.status == 'pending':
            transaction.status = data['status']
            db.session.commit()
            return jsonify({'message': 'Transaction status updated'})
        return jsonify({'message': 'Cannot update non-pending transaction'}), 400
    
    return render_template('admin/transaction_detail.html', transaction=transaction)