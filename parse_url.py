import re
from paramiko import SSHClient
from scp import SCPClient

def get_url():
	log_file = open('/home/pi/Desktop/MidtermProject/temp_files/cloudflared.log', 'r')
	line = log_file.readlines()[4]
	
	url = re.findall("((https:\/\/)([\w-])+(\.trycloudflare\.com))", line)[0][0]

	log_file.close()
	
	return url

def create_url_file(url):
	url_file = open('/home/pi/Desktop/MidtermProject/temp_files/url.js', 'w')
	#text = 'document.getElementById("redirect").url="' + url + '";'
	text = 'window.location.href = "' + url + '";'
	url_file.write(text)
	url_file.close()
	
def upload_url():
	remote_dir = '/home/ben_sirota/ben.sirota.org/mae6291'
	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.connect('ben.sirota.org', username='ben_sirota')
	
	scp = SCPClient(ssh.get_transport())
	
	scp.put('/home/pi/Desktop/MidtermProject/temp_files/url.js', remote_path=remote_dir)
	
	scp.close()
	

if __name__ == '__main__':
	url = get_url()
	print("Cloudflare URL: " + str(url))
	create_url_file(url)
	upload_url()
