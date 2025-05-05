# This repository holds the code for a Baja SAE Speedometer
## This project was completed for the GWU course MAE 6291 in Spring 2025

The goal of this project was to create an IoT Thing that can read the speed of two encoder wheels connected to the primary and secondary of a CVT and publish the information to the internet for easy viewing and analysis.

---

### To Use:
This code is designed to be used with a Raspberry Pi and 2 [IR Speed Sensors](https://www.robotshop.com/products/ir-speed-sensor-module).
1. Clone this repository to your Raspberry Pi.
2. Install necessary Python modules and [cloudflared](https://pkg.cloudflare.com/index.html) tool
```
pip install RPi.GPIO flask numpy plotly scp
```
```
# Add cloudflare gpg key
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

# Add this repo to your apt repositories
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list

# install cloudflared
sudo apt-get update && sudo apt-get install cloudflared
```
3. Set up SSH keys to your web server using ssh-keygen and ssh-copy-id
4. Set `parse_url.py` to upload to the correct server
    - Change `remote_dir` to the directory on the remote server you want to upload to
    - Update the `ssh.connect()` function call to the correct host and username
5. Connect your speed sensors to your Raspberry Pi
    - `VCC` pin on each module connects to `5V` on the Pi
    - `GND` pin on each module connects to `GND` on the Pi
    - `D0` on Sensor 1 connects to Board Pin `16` on the Pi
    - `D0` on Sensor 2 connects to Board pin `18` on the Pi
6. Run the `tunnel.sh` script to automatically start the web server, tunnel it to the internet, and read the data from the sensors