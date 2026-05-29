import random
from io import BytesIO
from pathlib import Path

import PIL
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker
from wagtail.images import get_image_model
from wagtail.models import Site

from home.models import (
    CVPage,
    EducationItem,
    JobItem,
    PortfolioItem,
    PortfolioPage,
    SkillDescriptionItem,
    SkillSubDescriptionItem,
    SkillSubSubDescriptionItem,
)

RED_PIXEL_JPG = PIL.Image.new("RGB", (1, 1), color=(255, 0, 0))

Image = get_image_model()
User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Create mock database"

    def handle(self, *args: tuple[str], **options: dict[str, str]) -> None:  # noqa: ARG002
        self._create_mock_portfolio_items(10)

        self._create_mock_skill_items(10)

        self._create_mock_education_items(random.randint(3, 6))  # noqa: S311

        self._create_mock_job_items(random.randint(3, 6))  # noqa: S311

        self._create_superuser()

        self._create_pages()


    def _create_mock_portfolio_items(self, count: int) -> None:

        mock_images = self._create_mock_images(count)

        for _ in range(count):
            item = PortfolioItem(
                project_title=" ".join(fake.unique.words(random.randint(1, 5))),  # noqa: S311
                show_title=bool(random.randint(0, 1)),  # noqa: S311
                image=random.choice(mock_images),  # noqa: S311
                description=fake.paragraph(nb_sentences=10),
                github_link=(fake.unique.url() if random.randint(0, 1) else ""),  # noqa: S311
            )

            item.tags.set([fake.word() for _ in range(random.randint(1, 3))])  # noqa: S311
            item.save()


    def _create_mock_skill_items(self, count: int) -> None:
        for _ in range(count):
            item = SkillDescriptionItem(
                title=" ".join(fake.unique.words(random.randint(1, 5))),  # noqa: S311
                description=fake.unique.text(max_nb_chars=random.randint(300, 600)),  # noqa: S311
                sort_order=random.randint(0, 1000),  # noqa: S311
            )

            item.save()

            for _ in range(random.randint(0, 4)):  # noqa: S311
                sub_item = SkillSubDescriptionItem(
                    title=" ".join(fake.unique.words(random.randint(1, 5))),  # noqa: S311
                    description=fake.unique.text(max_nb_chars=random.randint(300, 600)),  # noqa: S311
                    skill_item=item,
                    sort_order=random.randint(0, 1000),  # noqa: S311
                )

                sub_item.save()

                for _ in range(random.randint(0, 4)):  # noqa: S311
                    sub_sub_item = SkillSubSubDescriptionItem(
                        title=" ".join(fake.unique.words(random.randint(1, 5))),  # noqa: S311
                        description=fake.unique.text(max_nb_chars=random.randint(300, 600)),  # noqa: S311
                        skill_item=sub_item,
                        sort_order=random.randint(0, 1000),  # noqa: S311
                    )

                    sub_sub_item.save()


    def _create_mock_education_items(self, count: int) -> None:
        def generate_fake_grade() -> float:
            return (random.random() * 3) + 1  # noqa: S311

        items = [EducationItem(
                        institution=f"University of {fake.unique.city()}",
                        title=f"Bachelor of {fake.unique.job()}",
                        grade=f"{generate_fake_grade():.1f}",
                    )
                 for _ in range(count)]

        EducationItem.objects.bulk_create(items)


    def _create_mock_job_items(self, count: int) -> None:
        items = [JobItem(
                        company=fake.unique.company(),
                        employment_date=fake.date_between(start_date="-30y", end_date="now"),
                        termination_date=(fake.date_between(start_date="-30y", end_date="now")),
                        role=fake.unique.job(),
                        role_description=fake.text(max_nb_chars=random.randint(100, 200)),  # noqa: S311
                    )
                 for _ in range(count)]

        JobItem.objects.bulk_create(items)


    def _create_pages(self) -> None:
        avatar = self._load_mock_images([Path("mock/img/avatar.jpg")])[0]

        cv_page = CVPage(title="CV",
               slug="cv",
               show_in_menus=True,
               menu_icon="person-circle",
               github_link=fake.unique.url(),
               linkedin_link=fake.unique.url(),
               avatar=avatar,
        )

        portfolio_page = PortfolioPage(title="Portfolio",
                      slug="portfolio",
                      show_in_menus=True,
                      menu_icon="briefcase-fill",
                      avatar=avatar,
        )

        root = Site.objects.get(hostname="localhost").root_page
        root.add_child(instance=cv_page)
        root.add_child(instance=portfolio_page)
        cv_page.save_revision().publish()
        portfolio_page.save_revision().publish()


    def _create_superuser(self) -> None:


        user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",  # noqa: S106
        )

        user.first_name = fake.first_name()
        user.last_name = fake.last_name()

        user.save()


    def _create_mock_images(self,
                            count: int,
                            width: int = 1280,
                            height: int = 720,
                            img_format: str = "jpeg") -> list:
        images = []

        for _ in range(count):
            image_file = ContentFile(fake.image(size=(width, height), image_format=img_format),
                                     name=fake.unique.file_name(extension="jpeg"))
            images.append(
                Image(
                    title=" ".join(fake.unique.words(random.randint(1, 5))),  # noqa: S311
                    file=image_file,
                ),
            )

        Image.objects.bulk_create(images)

        return images


    def _load_mock_images(self, img_paths: list[Path]) -> list:
        images = []

        for img_path in img_paths:
            img_title = fake.unique.words(random.randint(1, 5))  # noqa: S311

            if Image.objects.filter(title=img_title).exists():
                return Image.objects.get(title=img_title)


            file_data = None
            try:
                with Path.open(img_path, "rb") as file:
                    file_data = file.read()
                self.stdout.write(self.style.ERROR(
                    f"Successfully loaded image file from: {img_path}"),
                )
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(
                    f"Failed to load image file from: {img_path}"),
                )
                buffer = BytesIO()
                RED_PIXEL_JPG.save(buffer, format="jpeg")
                buffer.seek(0)
                file_data = buffer.read()


            if not file_data:
                continue


            try:
                image_file = ContentFile(file_data, name=img_path.name)

                images.append(
                    Image(
                        title=img_title,
                        file=image_file,
                    ),
                )
            except Exception as e:  # noqa: BLE001
                self.stderr.write(self.style.ERROR(
                        "Could not save Wagtail Image object"
                        f"'{img_title}' with path '{img_path}': {e}",
                    ),
                )

        Image.objects.bulk_create(images)

        return images
