"""add email verification fields

Revision ID: add_email_verification
Revises: 4927cedb7907
Create Date: 2024-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_email_verification'
down_revision = '4927cedb7907'
branch_labels = None
depends_on = None


def upgrade():
    # Add email verification fields (idempotent - check if columns exist first)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('users')]
    
    if 'email_verified' not in existing_columns:
        op.add_column('users', sa.Column('email_verified', sa.Boolean(), server_default='false', nullable=False))
    
    if 'email_verification_token' not in existing_columns:
        op.add_column('users', sa.Column('email_verification_token', sa.String(), nullable=True))
    
    if 'email_verification_sent_at' not in existing_columns:
        op.add_column('users', sa.Column('email_verification_sent_at', sa.DateTime(timezone=True), nullable=True))
    
    # Create index on verification token for faster lookups (if it doesn't exist)
    existing_indexes = [idx['name'] for idx in inspector.get_indexes('users')]
    if 'ix_users_email_verification_token' not in existing_indexes:
        op.create_index(op.f('ix_users_email_verification_token'), 'users', ['email_verification_token'], unique=False)


def downgrade():
    # Remove index
    op.drop_index(op.f('ix_users_email_verification_token'), table_name='users')
    
    # Remove columns
    op.drop_column('users', 'email_verification_sent_at')
    op.drop_column('users', 'email_verification_token')
    op.drop_column('users', 'email_verified')

