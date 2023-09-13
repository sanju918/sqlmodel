"""empty message

Revision ID: 023b8afe1c1b
Revises:
Create Date: 2023-09-12 17:11:51.194217

"""
import json
import os
from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "023b8afe1c1b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users = op.create_table(
        "users",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        # sa.Column('role', sa.Enum('teacher', 'student', name='role'), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "users",
        sa.Column("role", sa.Enum("teacher", "student", name="role"), nullable=True),
    )

    with open(os.path.join(os.path.dirname(__file__), "../data/students.json")) as f:
        student_data = f.read()
    op.bulk_insert(users, json.loads(student_data))

    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "courses",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_courses_id"), "courses", ["id"], unique=False)
    op.create_table(
        "profiles",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_profiles_id"), "profiles", ["id"], unique=False)
    op.create_table(
        "sections",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sections_id"), "sections", ["id"], unique=False)
    op.create_table(
        "student_courses",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_student_courses_id"), "student_courses", ["id"], unique=False
    )
    op.create_table(
        "content_blocks",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        # sa.Column('type', sa.Enum('lesson', 'quiz', 'assignment', name='contenttype'), nullable=True),
        sa.Column("url", sqlalchemy_utils.types.url.URLType(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["sections.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "content_blocks",
        sa.Column(
            "type",
            sa.Enum("lesson", "quiz", "assignment", name="contenttype"),
            nullable=True,
        ),
    )
    op.create_index(
        op.f("ix_content_blocks_id"), "content_blocks", ["id"], unique=False
    )
    op.create_table(
        "completed_content_blocks",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("content_block_id", sa.Integer(), nullable=False),
        sa.Column("url", sqlalchemy_utils.types.url.URLType(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("grade", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["content_block_id"],
            ["content_blocks.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_completed_content_blocks_id"),
        "completed_content_blocks",
        ["id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_completed_content_blocks_id"), table_name="completed_content_blocks"
    )
    op.drop_table("completed_content_blocks")
    op.drop_index(op.f("ix_content_blocks_id"), table_name="content_blocks")
    op.drop_table("content_blocks")
    op.drop_index(op.f("ix_student_courses_id"), table_name="student_courses")
    op.drop_table("student_courses")
    op.drop_index(op.f("ix_sections_id"), table_name="sections")
    op.drop_table("sections")
    op.drop_index(op.f("ix_profiles_id"), table_name="profiles")
    op.drop_table("profiles")
    op.drop_index(op.f("ix_courses_id"), table_name="courses")
    op.drop_table("courses")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
