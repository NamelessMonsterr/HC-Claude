"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('phone_number', sa.String(20), nullable=False),
        sa.Column('name', sa.String(100)),
        sa.Column('age', sa.Integer()),
        sa.Column('gender', sa.String(20)),
        sa.Column('email', sa.String(100)),
        sa.Column('medical_conditions', postgresql.JSON()),
        sa.Column('current_medications', postgresql.JSON()),
        sa.Column('allergies', postgresql.JSON()),
        sa.Column('blood_type', sa.String(5)),
        sa.Column('preferred_language', sa.String(10), default='en'),
        sa.Column('notifications_enabled', sa.Boolean(), default=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_interaction', sa.DateTime()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('phone_number')
    )
    op.create_index('ix_users_phone_number', 'users', ['phone_number'])

    # Conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('direction', sa.String(10), nullable=False),
        sa.Column('message_sid', sa.String(100)),
        sa.Column('media_urls', postgresql.JSON()),
        sa.Column('intent', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Medical Reports table
    op.create_table(
        'medical_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('report_type', sa.String(50)),
        sa.Column('file_path', sa.String(500)),
        sa.Column('extracted_text', sa.Text()),
        sa.Column('analysis', postgresql.JSON()),
        sa.Column('report_date', sa.Date()),
        sa.Column('lab_name', sa.String(200)),
        sa.Column('doctor_name', sa.String(200)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Appointments table
    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('appointment_date', sa.DateTime(), nullable=False),
        sa.Column('appointment_type', sa.String(100)),
        sa.Column('doctor_name', sa.String(200)),
        sa.Column('clinic_name', sa.String(200)),
        sa.Column('reason', sa.Text()),
        sa.Column('notes', sa.Text()),
        sa.Column('status', sa.String(20), default='scheduled'),
        sa.Column('reminder_sent', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Medications table
    op.create_table(
        'medications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('dosage', sa.String(100)),
        sa.Column('frequency', sa.String(50)),
        sa.Column('times', postgresql.JSON()),
        sa.Column('start_date', sa.Date()),
        sa.Column('end_date', sa.Date()),
        sa.Column('instructions', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Symptom Logs table
    op.create_table(
        'symptom_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('symptoms', sa.Text(), nullable=False),
        sa.Column('severity', sa.String(20)),
        sa.Column('analysis', sa.Text()),
        sa.Column('recommendations', postgresql.JSON()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('symptom_logs')
    op.drop_table('medications')
    op.drop_table('appointments')
    op.drop_table('medical_reports')
    op.drop_table('conversations')
    op.drop_index('ix_users_phone_number')
    op.drop_table('users')