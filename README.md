# Setting up migrations using Alembic

Alembic Note¶
Normally you would probably initialize your database (create tables, etc) with [Alembic](https://alembic.sqlalchemy.org/en/latest/).

And you would also use Alembic for "migrations" (that's its main job).

A "migration" is the set of steps needed whenever you change the structure of your SQLAlchemy models, add a new attribute, etc. to replicate those changes in the database, add a new column, a new table, etc.

You can find an example of Alembic in a FastAPI project in the templates from [Project Generation - Template](https://fastapi.tiangolo.com/project-generation/). Specifically in [the `alembic` directory in the source code.](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/alembic/)

## Steps
- Install dependency
- Install dependency

    ```commandline
    pip install alembic
    ```
  
- Initialize Alembic

    ```commandline
    alembic init app/alembic
    ```
  
- Modify `alembic.ini` 

  ```
  # modify the following contents
  script_location = app/alembic
  prepend_sys_path = app
  sqlalchemy.url = postgresql+psycopg2://postgres:sTr0ngPass1234@localhost:5432/cloudlevel
  ```
  
- Modify `app/alembic/env.py`

  ```python
  # custom import of Models
  from app.db.db_setup import Base
  from app.db.models import user, course
  
  target_metadata = Base.metadata
  ```
  
- Run the following command to create a revision

  ```commandline
  alembic revision --autogenerate
  ```
- This would have created a revision file under `app/alembic/versions`
- Go to that file and fix if any missing dependency or errors. In our example we had to import missing library
  ```python
  import sqlalchemy_utils
  ```
- Run live migrations

  ```commandline
  alembic upgrade head
  ```
- You might encounter the following error
  ```commandline
  sqlalchemy.exc.ProgrammingError: (psycopg2.errors.DuplicateObject) type "role" already exists
  
  [SQL: CREATE TYPE role AS ENUM ('teacher', 'student')]
  ```
- The issue is with the conflicting name `role` under the revision file. In our case we need to comment out this line which is having issue and add additional code.

  Issue:
  ```python
  sa.Column('role', sa.Enum('teacher', 'student', name='role'), nullable=True),
  ```
  
  Fix:
  ```python
  def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=False),
        # we commented this line
                    # sa.Column('role', sa.Enum('teacher', 'student', name='role'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
  
    # we added these lines of code
    op.add_column(
        "users",
        sa.Column('role', sa.Enum('teacher', 'student', name='role'), nullable=True),
    )
  
  # rest of the codes
  op.create_table('content_blocks',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=200), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
        # we commenet the below line of code
                    # sa.Column('type', sa.Enum('lesson', 'quiz', 'assignment', name='contenttype'), nullable=True),
                    sa.Column('url', sqlalchemy_utils.types.url.URLType(), nullable=True),
                    sa.Column('content', sa.Text(), nullable=True),
                    sa.Column('section_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # we added the following lines of code
    op.add_column(
        'content_blocks',
        sa.Column('type', sa.Enum('lesson', 'quiz', 'assignment', name='contenttype'), nullable=True),
    )
  # rest of the code
  ```

- Create a folder `data` under alembic and create a file `students.json` with the following contents

  ```json
  [
      {
          "email": "bosco@example.com",
          "role": 2,
          "password": "testing123",
          "created_at": "2021-10-03 01:00:00-06",
          "updated_at": "2021-10-03 01:00:00-06"
      },
      {
          "email": "fish@example.com",
          "role": 2,
          "password": "testing123",
          "created_at": "2021-10-03 01:00:00-06",
          "updated_at": "2021-10-03 01:00:00-06"
      },
      {
          "email": "kitkat@example.com",
          "role": 2,
          "password": "testing123",
          "created_at": "2021-10-03 01:00:00-06",
          "updated_at": "2021-10-03 01:00:00-06"
      }
  ]
  ```
- Add the following code to the revision file under the `upgrade()` block

  ```python
  # add some imports
  import json
  import os
  
  def upgrade() -> None:
    # add users = op.create_table method
    users = op.create_table('users',
                            sa.Column('created_at', sa.DateTime(), nullable=False),
                            sa.Column('updated_at', sa.DateTime(), nullable=False),
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('email', sa.String(length=100), nullable=False),
            # we had commented this earlier
                            # sa.Column('role', sa.Enum('teacher', 'student', name='role'), nullable=True),
                            sa.PrimaryKeyConstraint('id')
                            )
    # we had added these lines of code earlier
    op.add_column(
        "users",
        sa.Column('role', sa.Enum('teacher', 'student', name='role'), nullable=True),
    )
    
  # Add these lines of code
    with open(os.path.join(os.path.dirname(__file__), "../data/students.json")) as f:
        student_data = f.read()
    op.bulk_insert(users, json.loads(student_data))
  
  # rest of the code remains as it is
  ```
- Now run the live migration again `alembic upgrade head`, and this should be successful this time


## Important Commands

- `alembic downgrade base`
  This will downgrade the schema of the databases to the base level ie remove all schemas
- After the schema change
  Suppose you have modified the schema of the table(s), in that scenario you can run the following command

  ```commandline
  alembic revision --autogenerate -m "moving is_active to user table"
  ```
- Now to make the changes run `alembic upgrade head`