"""initial schema

Revision ID: c6a23e8ca55e
Revises:
Create Date: 2026-03-24 14:47:18.940874

"""

from alembic import op
import sqlalchemy as sa


revision = 'c6a23e8ca55e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'times',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('estado', sa.String(length=2), nullable=False),
        sa.UniqueConstraint('nome', name='uq_times_nome'),
    )

    op.create_table(
        'estadios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('cidade', sa.String(length=100), nullable=False),
        sa.Column('capacidade', sa.Integer(), nullable=False),
        sa.CheckConstraint(
            'capacidade > 0',
            name='ck_estadios_capacidade_positiva',
        ),
        sa.UniqueConstraint('nome', name='uq_estadios_nome'),
    )

    op.create_table(
        'jogadores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('posicao', sa.String(length=50), nullable=False),
        sa.Column('time_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['time_id'],
            ['times.id'],
            ondelete='CASCADE',
            name='fk_jogadores_time_id_times',
        ),
    )

    op.create_table(
        'partidas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('time_casa_id', sa.Integer(), nullable=False),
        sa.Column('time_fora_id', sa.Integer(), nullable=False),
        sa.Column('estadio_id', sa.Integer(), nullable=False),
        sa.Column('placar', sa.String(length=10), nullable=False),
        sa.CheckConstraint(
            'time_casa_id <> time_fora_id',
            name='ck_partidas_times_diferentes',
        ),
        sa.ForeignKeyConstraint(
            ['estadio_id'],
            ['estadios.id'],
            ondelete='CASCADE',
            name='fk_partidas_estadio_id_estadios',
        ),
        sa.ForeignKeyConstraint(
            ['time_casa_id'],
            ['times.id'],
            ondelete='CASCADE',
            name='fk_partidas_time_casa_id_times',
        ),
        sa.ForeignKeyConstraint(
            ['time_fora_id'],
            ['times.id'],
            ondelete='CASCADE',
            name='fk_partidas_time_fora_id_times',
        ),
    )


def downgrade():
    op.drop_table('partidas')
    op.drop_table('jogadores')
    op.drop_table('estadios')
    op.drop_table('times')