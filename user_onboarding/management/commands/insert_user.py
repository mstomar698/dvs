from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from user_onboarding.models import PhoneNumber, Request_User
import json


class Command(BaseCommand):
    help = 'Insert data into the database'

    def handle(self, *args, **kwargs):
        data = []
        with open('user_onboarding/management/commands/csvjson.json') as users_file:
            data = json.load(users_file)

        for row in data:
            try:
                username = row["username"]
                email = row["email"]
                password = row["password"]
                re_password = row["password"]
                for_post = row["for_post"]
                phone_number = row["phone"]

                username_match = User.objects.filter(username=username)
                email_match = User.objects.filter(email=email)
                user_name_space = username.replace(" ", "")

                if len(user_name_space) == 0:
                    raise KeyError("Please enter any text in the Username field")

                username_split = username.split(" ")
                if len(username_split) >= 2:
                    raise KeyError("Username can only contain alphanumeric characters (a-z, A-Z, 0-9)")

                username_split_at_the_rate = username.split("@")
                if len(username_split_at_the_rate) >= 2:
                    raise KeyError("Username can only contain alphanumeric characters (a-z, A-Z, 0-9)")

                username_split_excla = username.split("!")
                if len(username_split_excla) >= 2:
                    raise KeyError("Username can only contain alphanumeric characters (a-z, A-Z, 0-9)")

                username_split_percentage = username.split("%")
                if len(username_split_percentage) >= 2:
                    raise KeyError("Username can only contain alphanumeric characters (a-z, A-Z, 0-9)")

                username_split_and = username.split("&")
                if len(username_split_and) >= 2:
                    raise KeyError("Username can only contain alphanumeric characters (a-z, A-Z, 0-9)")

                if username_match:
                    raise KeyError("Username already taken")

                elif email_match:
                    raise KeyError("Email already taken")

                elif password != re_password:
                    raise KeyError("Passwords do not match")
                else:
                    user_detail = Request_User(
                        user_name=username,
                        user_password=password,
                        user_email=email,
                        for_post=for_post
                    )
                    user_detail.save()
                    

                    phone = PhoneNumber.objects.create(
                        user=user_detail,
                        mobile_number=phone_number
                    )
                    
                    user_id = user_detail.id
                    print(f"User ID: {user_id}")
                    print(f"User phone details and linked user: {phone}")
                    print(f"User phone details and linked user: {phone.user}")

                    user = Request_User.objects.get(id=user_id)
                    approved = True

                    if approved:
                        user.approved = True
                        user.seen = True
                        user.save()
                        password = make_password(user.user_password)
                        create_user = User(
                            username=user.user_name,
                            email=user.user_email,
                            password=password,
                        )
                        create_user.save()

                        if user.for_post == "Moderator":
                            my_group, _ = Group.objects.get_or_create(name='Moderator')
                            create_user.groups.add(my_group)

                        elif user.for_post == "Railway Admin":
                            my_group, _ = Group.objects.get_or_create(name='Railway Admin')
                            moderator_group = Group.objects.get(name='Moderator')
                            create_user.groups.add(moderator_group)
                            create_user.groups.add(my_group)

                        elif user.for_post == "Normal User":
                            pass

                        create_user.save()

            except Exception as e:
                print(e)

        self.stdout.write(self.style.SUCCESS('Users inserted successfully'))
