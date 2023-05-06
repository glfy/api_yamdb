import csv
import datetime

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


def parse_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")


class Command(BaseCommand):
    help = "Import CSV data to database"

    def load_users(self):
        with open(
            "static/data/users.csv", newline="", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                user, created = User.objects.get_or_create(
                    id=row["id"],
                    defaults={
                        "username": row["username"],
                        "email": row["email"],
                        "role": row["role"],
                        "bio": row["bio"],
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                    },
                )
                if not created:
                    self.stdout.write(
                        self.style.WARNING(
                            f"""User with id {row['id']} already exists.
                            Skipping."""
                        )
                    )

    def load_category(self):
        with open(
            "static/data/Category.csv", mode="r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Category.objects.get_or_create(
                    id=row["id"], name=row["name"], slug=row["slug"]
                )

    def load_genre(self):
        with open("static/data/Genre.csv", mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Genre.objects.get_or_create(
                    id=row["id"], name=row["name"], slug=row["slug"]
                )

    def load_titles(self):
        with open(
            "static/data/titles.csv", mode="r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Title.objects.create(
                    id=row["id"],
                    name=row["name"],
                    year=int(row["year"]),
                    category_id=row["category_id"],
                )

    def load_genre_title(self):
        with open(
            "static/data/genre_title.csv", mode="r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = Title.objects.get(id=row["title"])
                genre = Genre.objects.get(id=row["genre"])
                title.genre.add(genre)

    def load_review(self):
        with open(
            "static/data/Review.csv", mode="r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Review.objects.get_or_create(
                    id=row["id"],
                    title_id=row["title"],
                    text=row["text"],
                    author_id=row["author"],
                    score=int(row["score"]),
                    pub_date=parse_date(row["pub_date"]),
                )

    def load_comments(self):
        with open(
            "static/data/comments.csv", mode="r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Comment.objects.get_or_create(
                    id=row["id"],
                    review_id=row["review"],
                    text=row["text"],
                    author_id=row["author"],
                    pub_date=parse_date(row["pub_date"]),
                )

    def handle(self, *args, **options):
        self.load_users()
        self.load_category()
        self.load_genre()
        self.load_titles()
        self.load_genre_title()
        self.load_review()
        self.load_comments()
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
