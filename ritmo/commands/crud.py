import datetime

import click

from ritmo.models import models
from ritmo.session import session


@click.command(name="add", help="Add a new habit.")
@click.argument("name", nargs=1, type=str, required=True)
@click.option(
    "--description",
    "-d",
    prompt="Habit description",
    prompt_required=False,
    help="Description of the habit.",
)
@click.option(
    "--type",
    "-t",
    prompt="Type of tracking system",
    prompt_required=False,
    default="boolean",
    type=click.Choice(["boolean", "numerical"], case_sensitive=False),
    help="Type of tracking system.",
)
@click.option(
    "--start-date",
    prompt="Start date",
    prompt_required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date in 'Y-m-d' format.",
)
@click.option(
    "--end-date",
    prompt="End date",
    prompt_required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="End date in 'Y-m-d' format.",
)
def add_habit(
    name: str,
    description: str,
    type: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    """
    Add a new habit to the tracking system.

    Args:
        name: The name of the habit.
        description: A description of the habit.
        type: The type of tracking system to use.
        start_date: The date the habit starts.
        end_date: The date the habit ends.
    """

    if end_date and start_date and end_date < start_date:
        click.echo("End date must be after start date.")
        return

    Session = session.create_local_session()
    with Session.begin() as sess:
        habit = sess.query(models.Habit).filter(models.Habit.name == name).first()

        if habit:
            return
        else:
            sess.add(models.Habit(name=name, description=description, type=type))
            sess.commit()


@click.command(name="list", help="List habits.")
def list_habits():
    """
    List all habits.
    """

    Session = session.create_local_session()
    with Session.begin() as sess:
        habits = sess.query(models.Habit).all()
        for habit in habits:
            click.echo(
                f"Name: {habit.name}, Description: {habit.description}, "
                f"Type: {habit.type}, Start date: {habit.start_date}, "
                f"End date: {habit.end_date}"
            )


@click.command(name="update", help="Update an existing habit.")
@click.argument("name", nargs=1, type=str)
@click.option(
    "--new-name",
    "-n",
    prompt="Habit name",
    prompt_required=False,
    help="Name of the habit.",
)
@click.option(
    "--description",
    "-d",
    prompt="Habit description",
    prompt_required=False,
    help="Description of the habit",
)
@click.option(
    "--type",
    "-t",
    prompt="Type of tracking system",
    prompt_required=False,
    default="boolean",
    type=click.Choice(["boolean", "numerical"], case_sensitive=False),
    help="Type of tracking system",
)
@click.option(
    "--start-date",
    prompt="Start date",
    prompt_required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date in UTC format",
)
@click.option(
    "--end-date",
    prompt="End date",
    prompt_required=False,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="End date in UTC format",
)
def update_habit(
    name: str,
    new_name: str,
    description: str,
    type: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    """
    Update a habit.

    Args:
        name: The name of the habit.
        new_name: The new name of the habit.
        description: A description of the habit.
        type: The type of tracking system to use.
        start_date: The date the habit starts.
        end_date: The date the habit ends.
    """

    if not name:
        click.echo("Habit name must be provided.")
        return

    if end_date and start_date and end_date < start_date:
        click.echo("End date must be after start date.")
        return

    Session = session.create_local_session()
    with Session.begin() as sess:
        habit = sess.query(models.Habit).filter(models.Habit.name == name).first()
        if habit:
            if new_name:
                habit.name = new_name
            if description:
                habit.description = description
            if type:
                habit.type = type
            if start_date:
                habit.start_date = start_date
            if end_date:
                habit.end_date = end_date
            sess.commit()
        else:
            click.echo(f"Habit '{name}' not found.")


@click.command(name="delete", help="Delete a habit.")
@click.argument("name", nargs=1, type=str, required=True)
def delete_habit(name: str):
    """
    Delete a habit.

    Args:
        name: The name of the habit.
    """

    Session = session.create_local_session()
    with Session.begin() as sess:
        habit = sess.query(models.Habit).filter(models.Habit.name == name).first()

        if habit:
            sess.delete(habit)
            sess.commit()
        else:
            click.echo(f"Habit '{name}' not found.")
