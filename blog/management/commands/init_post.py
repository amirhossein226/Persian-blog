from blog.models import Post
from account.models import Profile
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
import random
from unidecode import unidecode
from django.db.utils import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Initializing some Posts!'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int,
                            help="=====number of objects====")

    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.NOTICE(
            "=======================================I am initializingggggggg ======================================="))
        faker_fa = Faker("fa_IR")
        faker_en = Faker()
        post_count = kwargs.get('count', 30)

        user_names = ['Ali', 'Faeze', "Setayesh"]

        for u in range(len(user_names)):
            username = random.choice(user_names)
            email = f"{username.lower()}@gmail.com"
            password = f"{username.lower()}1234"

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                )
                user.set_password(password)
            except Exception as e:
                print(e)
                continue
            Profile.objects.create(user=user)

        all_authors = User.objects.all()
        for _ in range(post_count):
            title = faker_fa.text(30)[:-1]
            body = faker_fa.paragraph(50)

            description = " ".join(body.split()[:30])
            status = random.choice(Post.Status.values)
            authors = random.choices(all_authors, k=random.randint(1, 3))
            tags = random.choices(title.split(), k=random.randint(1, 3))

            post = Post.objects.create(
                title=title,
                description=description,
                body=body,
                status=status
            )
            for author in authors:
                if author not in post.authors.all():
                    post.authors.add(author)
            for tag in tags:
                if tag not in post.tags.all():
                    post.tags.add(tag)

        self.stdout.write(self.style.SUCCESS(
            "=======================================Initialization completed======================================="))
