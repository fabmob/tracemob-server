import sys
import os
import argparse
import time
import logging
import subprocess
import datetime

logging.basicConfig(filename="/var/log/emission/emission_backup.log",
					level=logging.DEBUG,
					format="%(asctime)s:%(levelname)s:%(message)s")

if __name__ == '__main__':
	now = datetime.datetime.now()

	parser = argparse.ArgumentParser(description = 'Backup script for MongoDB')
	parser.add_argument('-o', '--output_dir', type = str, required = False,
		help = 'Output directory for the backup.')
	parser.add_argument('-d', '--database', type = str, required = False,
		help = 'Database to backup')
	parser.add_argument('-n', '--nb_backup', type = int, required = False,
		help = 'Number max if backup')
	parser.add_argument('-p', '--password', type = str, required = False,
		help = 'Encryption password')
	args = parser.parse_args()

	date = now.strftime('%Y-%m-%d')
	logging.info(f"Going to backup MongoDB database of {date}")

	if args.output_dir is None:
		out_path = '/var/emission/backup/'
		logging.info(f'No output dir, I will save the DB in {out_path}')
	else:
		out_path = args.output_dir

	if args.database is None:
		db = 'Stage_database'
		logging.info(f'No database dir, I will backup {db}')
	else:
		db = args.database

	if args.nb_backup is None:
		nb_backup = 30
		logging.info(f'No max backup, max default value is {nb_backup}')
	else:
		nb_backup = args.nb_backup

	if args.password is None:
		logging.info('No encryption password, backup will be not encrypted')
		password = None
	else:
		password = args.password

	filename = f'{out_path}{db}-{date}.gzip'
	p = subprocess.run(['mongodump', '-d', db, '--gzip', f'--archive={filename}'])
	if p.returncode != 0:
		logging.info(f'Backup ERROR: args={p.args} | returncode={p.returncode} | stdout={p.stdout} | stderr={p.stderr}')
	logging.info('Backup done')

	if p.returncode == 0 and password is not None:
		logging.info('Start encryption')
		# Encrypt: openssl enc -e -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -in $FILE.gzip -out $FILE.gzip.enc -pass pass:$PASSWORD
		# Decrypt: openssl enc -d -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -in $FILE.gzip.enc -out $FILE-dec.gzip -pass pass:$PASSWORD
		p = subprocess.run([
			'openssl', 'enc', '-e', '-aes-256-cbc', '-md', 'sha512', '-pbkdf2', '-iter', '100000',
			'-salt', '-in', f'{filename}', '-out', f'{filename}.enc', '-pass', f'pass:{password}'
		])
		if p.returncode != 0:
			logging.info(f'Encryption ERROR: args={p.args} | returncode={p.returncode} | stdout={p.stdout} | stderr={p.stderr}')
		else:
			try:
				os.remove(filename)
			except Exception as e:
				logging.info(f'Delete ERROR: {e}')
				pass
		logging.info('Encryption done')

	with open('/var/log/emission/elapsedtime.log', 'a+') as f:
		now2 = datetime.datetime.now()
		f.write(f'{str(now2)} mongo_backup {str(now2 - now)}\n')
