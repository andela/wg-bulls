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


from wger.core.models import User
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.contrib.auth import authenticate


class Command(BaseCommand):
    '''
    Allow user to create other users via the API
    '''

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    help = 'Gives authorization to a user so they can create users via the API'

    option_list = BaseCommand.option_list + (

        make_option(
            '--username',
            action='store_true',
            dest='username',
            default=False,
            help='Username of the user to give permissions'
        ),

        make_option(
            '--password',
            action='store_true',
            dest='username',
            default=False,
            help='Password of the admin'
        )
    )

    def handle(self, *args, **options):
        self.stdout.write('** Updating this user\'s permissions')
        if (options.get('username') or options.get('password')) is False:
            self.stdout.write('Please add both --username and --password')
            return
        try:
            username = options.get('username')
            username = str(args[0])
            password = options.get('password')
            password = str(args[1])
        except IndexError:
            self.stdout.write(
                'Please provide both the username and the admin password')
            return
        # authenticate admin
        admin = authenticate(username='admin', password=password)
        if not admin:
            raise CommandError('Password provided for admin is incorrect')

        try:
            user = User.objects.get(username=username)
            if not user.userprofile.can_create_users:
                self.stdout.write(self.style.SUCCESS(
                'User {0} does not have API permissions'.format(
                    username)))
                return
            user.userprofile.can_create_users = False
            user.userprofile.save()
            self.stdout.write(self.style.SUCCESS(
                'User permissions for {0} revoked successfully'.format(
                    username)))
            return
        except User.DoesNotExist:
            raise CommandError("User {0} does not exist".format(
                username))
