from bin.analysis.find_inactive_users import find_inactive_users
from bin.debug.common import purge_entries_for_user

import argparse
import datetime
import logging
import logging.handlers

handler = logging.handlers.TimedRotatingFileHandler(
	filename='/var/log/emission/inactive_user/delete_inactive_user.log',
	backupCount=10, when='midnight', encoding='UTF-8'
)
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s',
	handlers=[handler])

TEST = True
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Delete inactive user script')
	parser.add_argument('-d', '--days', type=int, required=False, help='number of inactive days.')

	args = parser.parse_args()
	if args.days is None:
		nbdays = 30
		logging.info(f'No number of days, get default value: {nbdays}')
	else:
		nbdays = args.days

	date = datetime.datetime.now() - datetime.timedelta(days=nbdays)
	logging.info(f"Getting inactive user since {date.strftime('%Y-%m-%d')} ({nbdays} days){' [TEST MODE]' if TEST else ''}")
	users = find_inactive_users(nbdays=nbdays, with_uuid=True, test=TEST)

	nb_users = len(users)
	logging.info(f"{nb_users} inactive user to delete")
	for index, (email, lastSignUpDate, lastUsercacheCall, uuid) in enumerate(users):
		logging.info(f"Deleting user {index + 1}/{nb_users} ({email} | {uuid})")
		purge_entries_for_user(uuid, True)
		logging.info(f"User deleted")
