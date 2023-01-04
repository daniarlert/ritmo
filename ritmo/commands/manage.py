import datetime

import click

from ritmo.models import models
from ritmo.session import session


@click.command(name="done", help="Mark a habit as done.")
@click.argument("name", nargs=1, type=str)
def mark_done(name: str):
    """
    Mark a habit as done.
    """

    Session = session.create_session("sqlite:///habit.db")
    with Session.begin() as sess:
        habit: models.Habit = (
            sess.query(models.Habit).filter(models.Habit.name == name).first()
        )

        if habit:
            habit_day: models.HabitDay = (
                sess.query(models.HabitDay)
                .filter(
                    models.HabitDay.habit_id == habit.id
                    and models.HabitDay.date == datetime.datetime.utcnow().date
                )
                .first()
            )

            if habit_day:
                habit_day.completed = True

                if habit.type == "numerical":
                    habit_day.completed_num += 1
            else:
                habit_day = models.HabitDay(
                    habit_id=habit.id, completed=True, completed_num=1
                )
                sess.add(habit_day)

            sess.commit()
        else:
            click.echo(f"Habit '{name}' not found.")


@click.command(name="undo", help="Mark a habit as undone.")
@click.argument("name", nargs=1, type=str)
def mark_undone(name: str):
    """
    Mark a habit as undone.
    """

    Session = session.create_session("sqlite:///habit.db")
    with Session.begin() as sess:
        habit: models.Habit = (
            sess.query(models.Habit).filter(models.Habit.name == name).first()
        )

        if habit:
            habit_day: models.HabitDay = (
                sess.query(models.HabitDay)
                .filter(
                    models.HabitDay.habit_id == habit.id
                    and models.HabitDay.date == datetime.datetime.utcnow().date
                )
                .first()
            )

            if habit_day:
                habit_day.completed = False

                if habit.type == "numerical" and habit_day.completed_num > 0:
                    habit_day.completed_num -= 1

            sess.commit()
        else:
            click.echo(f"Habit '{name}' not found.")
