from djcelery import celery
import signal
import os
import time
import sys
from account.models import Account, TorrentEntries, TorrentGlobalEntries
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from utils.func import *
import shutil

TorrentStorage_PATH = settings.DOWNLOAD_DIR
download_flag=True

#TODO: more effecient method?...
def receive_signal(signum, stack):
	global download_flag	
	download_flag=False

@celery.task(name='tasks.TorrentDownload')
def TorrentDownload(account, data):
	import libtorrent as lt
	import time

	# Update queued entries priority
	queued_entries = TorrentEntries.objects.filter(status="queued")
	for entry in queued_entries:
		if entry.priority != 0:
			entry.priority -= 1
			entry.save()

	#TODO: We have to support Three mode, URL, magnet, File
	# register signal
	signal.signal(signal.SIGINT, receive_signal)
	
	global download_flag	
	download_flag=True

	ses = lt.session()
	ses.listen_on(6881, 6891)
	e = lt.bdecode(data)
	info = lt.torrent_info(e)
	torrent_hash = str(info.info_hash())

	# Add torrent
	h = ses.add_torrent({'ti': info, 'save_path': TorrentStorage_PATH})
	
	# Torrent validation check
	if h.is_valid() is not True:
		print "[ERROR] Not valid torrent!"
		return

	# Save progress and torrent download status into DB
	try:
		torrent_entry = TorrentEntries.objects.get(owner=account, hash_value=torrent_hash)
	except:
		print "[ERROR] Someting goes wrong! Maybe there exist bugs..."
		return

	torrent_entry.worker_pid = os.getpid() 
	while (not h.is_seed() and download_flag is True):
		s = h.status()
		torrent_entry.progress=int("%d" % (s.progress * 100))
		torrent_entry.download_rate=s.download_rate
		torrent_entry.downloaded_size=s.total_done
		torrent_entry.peers=s.num_peers
		torrent_entry.status="downloading"
		torrent_entry.save()
		time.sleep(1);

	filePath = os.path.join(TorrentStorage_PATH,torrent_entry.name)

	# User cancel torrent download during downloading...
	if download_flag is False:
		torrent_entry.delete()
	else:
		if os.path.isdir(filePath):
			# make folder to zip file
			torrent_entry.progress=100
			torrent_entry.downloaded_size = torrent_entry.file_size
			torrent_entry.download_rate = 0
			torrent_entry.peers = 0
			torrent_entry.status="compressing"
			torrent_entry.save()
			compress_data(TorrentStorage_PATH, torrent_entry.name)
			
			# remove original directory
			shutil.rmtree(filePath)	
			torrent_entry.name = torrent_entry.name + ".zip"

		print "[INFO] Done: " + str(h.name())
		torrent_entry.progress=100
		torrent_entry.downloaded_size = torrent_entry.file_size
		torrent_entry.download_rate = 0
		torrent_entry.peers = 0
		torrent_entry.status="finished"
		torrent_entry.save()

	# TorrentGlobalEntries store all downloaded torrent entry
	# It is used for duplication check, search torrent, etc...
	global_entry=TorrentGlobalEntries(name=torrent_entry.name,
					hash_value=torrent_entry.hash_value,
					progress=torrent_entry.progress,
					file_size=torrent_entry.file_size,
					downloaded_size=torrent_entry.downloaded_size,
					peers=torrent_entry.peers,
					status=torrent_entry.status)
	global_entry.save()


