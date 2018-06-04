# -*- coding: utf-8 *-*

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License


from wger.core.models import UserProfile, User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    '''
    Lists all users created by this user
    '''

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    help = 'Lists all the users created by this user via the REST API'

    def handle(self, *args, **options):
        '''
        Process the options
        '''
        username = options['username']

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError("User {0} does not exist".format(username))
        else:
            raise CommandError("Provide a valid username")

        if user:
            try:
                profiles = UserProfile.objects.filter(created_by=str(username))
                self.stdout.write(self.style.SUCCESS(
                "These are the users created by: {0}".format(
                    username)))
                for profile in profiles:
                    self.stdout.write("User: {0}".format(profile.user.username))
            except UserProfile.DoesNotExist:
                self.stdout.write(self.style.SUCCESS(
                "No users created by this user"))   
