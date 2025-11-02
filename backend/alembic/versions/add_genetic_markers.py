"""add genetic markers

Revision ID: add_genetic_markers
Revises: add_email_verification
Create Date: 2024-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_genetic_markers'
down_revision = 'add_email_verification'
branch_labels = None
depends_on = None


def upgrade():
    # Create genetic_markers table
    op.create_table(
        'genetic_markers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('target_id', sa.String(), nullable=False),
        sa.Column('chromosome', sa.String(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('variant_type', sa.String(), nullable=False),
        sa.Column('ref_base', sa.String(), nullable=False),
        sa.Column('mut_base', sa.String(), nullable=False),
        sa.Column('gene_name', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_genetic_markers_id', 'genetic_markers', ['id'], unique=False)
    op.create_index('ix_genetic_markers_user_id', 'genetic_markers', ['user_id'], unique=False)
    op.create_index('ix_genetic_markers_user_target', 'genetic_markers', ['user_id', 'target_id'], unique=True)
    
    # Create ctdna_test_results table
    op.create_table(
        'ctdna_test_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('test_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('test_lab', sa.String(), nullable=True),
        sa.Column('result_file_name', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ctdna_test_results_id', 'ctdna_test_results', ['id'], unique=False)
    op.create_index('ix_ctdna_test_results_user_id', 'ctdna_test_results', ['user_id'], unique=False)
    op.create_index('ix_ctdna_test_results_test_date', 'ctdna_test_results', ['test_date'], unique=False)
    
    # Create detected_markers table
    op.create_table(
        'detected_markers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_result_id', sa.Integer(), nullable=False),
        sa.Column('marker_id', sa.Integer(), nullable=False),
        sa.Column('detected', sa.Boolean(), nullable=False),
        sa.Column('variant_allele_frequency', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['test_result_id'], ['ctdna_test_results.id'], ),
        sa.ForeignKeyConstraint(['marker_id'], ['genetic_markers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_detected_markers_id', 'detected_markers', ['id'], unique=False)
    op.create_index('ix_detected_markers_test_result_id', 'detected_markers', ['test_result_id'], unique=False)
    op.create_index('ix_detected_markers_marker_id', 'detected_markers', ['marker_id'], unique=False)
    
    # Add targeted_markers to foods table
    op.add_column('foods', sa.Column('targeted_markers', sa.JSON(), nullable=True))
    
    # Add related_markers to research_studies table
    op.add_column('research_studies', sa.Column('related_markers', sa.JSON(), nullable=True))


def downgrade():
    # Remove columns
    op.drop_column('research_studies', 'related_markers')
    op.drop_column('foods', 'targeted_markers')
    
    # Drop tables
    op.drop_index('ix_detected_markers_marker_id', table_name='detected_markers')
    op.drop_index('ix_detected_markers_test_result_id', table_name='detected_markers')
    op.drop_index('ix_detected_markers_id', table_name='detected_markers')
    op.drop_table('detected_markers')
    
    op.drop_index('ix_ctdna_test_results_test_date', table_name='ctdna_test_results')
    op.drop_index('ix_ctdna_test_results_user_id', table_name='ctdna_test_results')
    op.drop_index('ix_ctdna_test_results_id', table_name='ctdna_test_results')
    op.drop_table('ctdna_test_results')
    
    op.drop_index('ix_genetic_markers_user_target', table_name='genetic_markers')
    op.drop_index('ix_genetic_markers_user_id', table_name='genetic_markers')
    op.drop_index('ix_genetic_markers_id', table_name='genetic_markers')
    op.drop_table('genetic_markers')

