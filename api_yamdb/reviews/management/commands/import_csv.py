import csv
import datetime
from django.core.management.base import BaseCommand
from reviews.models import User, Category, Genre, Title, Review, Comment


def parse_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")


class Command(BaseCommand):
    help = "Import CSV data to database"

    def handle(self, *args, **options):
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

        with open(
            "static/data/Category.csv", mode="r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Category.objects.get_or_create(
                    id=row["id"], name=row["name"], slug=row["slug"]
                )

        with open("static/data/Genre.csv", mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Genre.objects.get_or_create(
                    id=row["id"], name=row["name"], slug=row["slug"]
                )

        with open(
            "static/data/titles.csv", mode="r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = Title.objects.create(
                    id=row["id"],
                    name=row["name"],
                    year=int(row["year"]),
                    category_id=row["category_id"],
                )

        with open(
            "static/data/genre_title.csv", mode="r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = Title.objects.get(id=row["title"])
                genre = Genre.objects.get(id=row["genre"])
                title.genre.add(genre)

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
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))

        

"""import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

TABLES = {
    User: "users.csv",
    Category: "category.csv",
    Title: "titles.csv",
    Genre: "genre.csv",




    # Review: "review.csv",
    Genre: "genre.csv",
    Comment: "comments.csv",
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            with open(
                "static/data/users.csv", newline="", encoding="utf-8"
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user, created = User.objects.update_or_create(
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
            with open("static/data/review.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user = User.objects.get(
                        id=int(row["author"])
                    )  # Fetch the User instance with the provided id
                    review = Review(
                        title_id=row["title"],
                        text=row["text"],
                        author=user,  # Assign the User instance to the author field
                        score=row["score"],
                        pub_date=row["pub_date"],
                    )
                    review.save()

            with open(
                f"{settings.BASE_DIR}/static/data/{csv_f}",
                "r",
                encoding="utf-8",
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS("Все данные загружены"))
"""