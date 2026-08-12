"""Add per-user ownership to categories.

Revision ID: a1b2c3d4e5f6
Revises: 34e9667f8143
Create Date: 2026-08-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "34e9667f8143"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "categories",
        sa.Column("owner_id", sa.Integer(), nullable=True),
    )

    # Assign any existing shared categories to the earliest user, if present.
    op.execute(
        """
        UPDATE categories
        SET owner_id = (
            SELECT id FROM users ORDER BY id ASC LIMIT 1
        )
        WHERE owner_id IS NULL
        """
    )

    # If there are categories but no users, remove them so the NOT NULL
    # constraint can be applied safely.
    op.execute("DELETE FROM categories WHERE owner_id IS NULL")

    op.alter_column(
        "categories",
        "owner_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.drop_constraint(
        "categories_name_key",
        "categories",
        type_="unique",
    )

    op.create_foreign_key(
        "fk_categories_owner_id_users",
        "categories",
        "users",
        ["owner_id"],
        ["id"],
    )

    op.create_index(
        "ix_categories_owner_id",
        "categories",
        ["owner_id"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_categories_owner_name",
        "categories",
        ["owner_id", "name"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_categories_owner_name",
        "categories",
        type_="unique",
    )
    op.drop_index("ix_categories_owner_id", table_name="categories")
    op.drop_constraint(
        "fk_categories_owner_id_users",
        "categories",
        type_="foreignkey",
    )
    op.create_unique_constraint(
        "categories_name_key",
        "categories",
        ["name"],
    )
    op.drop_column("categories", "owner_id")
